"""
Component that will perform facial recognition via CompreFace
"""
from typing import Any

import io
import logging
import re
import voluptuous as vol
import hashlib

import homeassistant.util.dt as dt_util
import homeassistant.helpers.config_validation as cv

from pathlib import Path
from PIL import Image, ImageDraw

from compreface import CompreFace
from compreface.service import RecognitionService, DetectionService
from compreface.collections import FaceCollection
from compreface.collections.face_collections import Subjects

from homeassistant.core import callback
from homeassistant.util.pil import draw_box
from homeassistant.exceptions import HomeAssistantError


from homeassistant.components.image_processing import (
    ImageProcessingFaceEntity,
)
from homeassistant.const import (
    ATTR_ENTITY_ID,
    ATTR_NAME,
    CONF_IP_ADDRESS,
    CONF_PORT,
)

from .const import (
    DOMAIN,
    CONF_API_RECOGNITION_KEY,
    CONF_API_DETECTION_KEY,
    CONF_TIMEOUT,
    CONF_DETECT_ONLY,
    CONF_SAVE_FILE_FOLDER,
    CONF_SAVE_TIMESTAMPTED_FILE,
    CONF_SAVE_FACES_FOLDER,
    CONF_SAVE_FACES,
    CONF_SHOW_BOXES,
    CONF_MIN_CONFIDANCE,
    DATETIME_FORMAT,
    FILE_PATH,
    CAMERA_SCAN_ENTITY_ID,
    COMPREFACE_CONNECT_ERROR_MESSAGE
)
from .exceptions import (    
    NoUsablePhotoException
)

from .services import (
    setup_services
)
from .helper import (
    get_image_by_url,
    create_notify_message
)

_LOGGER = logging.getLogger(__name__)


# rgb(red, green, blue)
RED = (255, 0, 0)  # For objects within the ROI

SERVICE_TEACH_SCHEMA = vol.Schema(
    {
        vol.Optional(ATTR_ENTITY_ID): cv.entity_ids,
        vol.Required(ATTR_NAME): cv.string,
        vol.Required(FILE_PATH): cv.string,
    }
)

SERVICE_SCAN_SCHEMA = vol.Schema(
    {
        vol.Required(CAMERA_SCAN_ENTITY_ID): cv.entity_ids,
    }
)


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the image processing entity from a config entry."""
    await async_setup_platform(hass, {}, async_add_entities)

async def async_setup_platform(hass, config, async_add_devices, discovery_info=None):
    """Set up the generic image_processing platform."""
    await setup_services(hass)
    return setup_entity(hass, async_add_devices) 

def setup_entity(hass, async_add_entities, discovery_info=None):
    """Set up the image processing classifier."""
    ai_facial_base = hass.data[DOMAIN]
    config = ai_facial_base.configuration.config_entry.data
    
    image_processing_face_entity = setup_face_classify_entity(hass, config)

    ai_facial_base  = hass.data[DOMAIN]
    ai_facial_base.image_processing_entity = image_processing_face_entity
    async_add_entities([image_processing_face_entity])
    return True

def setup_face_classify_entity(hass, config): 
    """Takes as input the config (map with config flow values) and outputs the image processing entity"""
    save_file_folder = config.get(CONF_SAVE_FILE_FOLDER)
    if save_file_folder:
        save_file_folder = Path(save_file_folder)

    save_faces_folder = config.get(CONF_SAVE_FACES_FOLDER)
    if save_faces_folder:
        save_faces_folder = Path(save_faces_folder)

    
    image_processing_face_entity = FaceClassifyEntity(
        hass, 
        config[CONF_IP_ADDRESS],
        config[CONF_PORT],
        config.get(CONF_API_RECOGNITION_KEY),
        config.get(CONF_API_DETECTION_KEY),
        config[CONF_TIMEOUT],
        config[CONF_MIN_CONFIDANCE], 
        config[CONF_DETECT_ONLY],
        save_file_folder,
        config[CONF_SAVE_TIMESTAMPTED_FILE],
        save_faces_folder,
        config[CONF_SAVE_FACES],
        config[CONF_SHOW_BOXES],
        name = "face_recognition_central"
    )

    return image_processing_face_entity

class FaceClassifyEntity(ImageProcessingFaceEntity):
    """Face classification image processing entity."""

    def __init__(
        self,
        hass, 
        ip_address,
        port,
        api_key_recognition,
        api_key_detection, 
        timeout,
        min_confidance,
        detect_only,
        save_file_folder,
        save_timestamped_file,
        save_faces_folder,
        save_faces,
        show_boxes,
        name
    ):
        """Init with the API key and model id."""
        super().__init__()
        self.hass = hass
        self.compre_face: CompreFace = CompreFace(ip_address, port)
        self.recognition: RecognitionService = self.compre_face.init_face_recognition(api_key_recognition)
        self.detection: DetectionService = self.compre_face.init_face_detection(api_key_detection)
        self.face_collection: FaceCollection = self.recognition.get_face_collection()
        self.subjects: Subjects = self.recognition.get_subjects()

        self.ip_address = ip_address
        self.port = port
        self.recognition_api_key = api_key_recognition
        self.detection_api_key = api_key_detection
        
        self.camera_timeout = 10
        self._timeout = timeout
        self._confidence = min_confidance
        self._detect_only = detect_only
        self._show_boxes = show_boxes
        self._last_detection = None
        self._save_file_folder = save_file_folder
        self._save_timestamped_file = save_timestamped_file
        self._save_faces_folder = save_faces_folder
        self._save_faces = save_faces
        self._name = name
        self._predictions = []       
        self._matched = {}
        self._registered_faces = {}
        self.total_faces = None

        m = hashlib.sha256()
        m.update(b"face_recognition_central")
        self._attr_unique_id = m.hexdigest()
        
    async def async_process_image(self, camera_scan_entity_id):
        """Process an image. The image is fecthed from camera_entity id.""" 
        camera = self.hass.components.camera
        try:
            image = await camera.async_get_image(
                camera_scan_entity_id, timeout=self.camera_timeout
            )
            await self.hass.async_add_executor_job(self.process_image, image.content)
        except HomeAssistantError as err:
            _LOGGER.error("Error on receive image from entity: %s", err)
            return
    
    def process_image(self, image): 
        self._predictions = []
        self._matched = []
        self.total_faces = None   
        pil_image = Image.open(io.BytesIO(bytearray(image))).convert("RGB")
        image_width, image_height =  pil_image.size

        try: 
            if self._detect_only:
                self._predictions = self.detection.detect(image_path = image)
            else:
                self._predictions = self.recognition.recognize(image_path = image)
        except ConnectionError: 
            _LOGGER.error(COMPREFACE_CONNECT_ERROR_MESSAGE.format(self.ip_address, self.port))

        if self._predictions.get("message") == "No face is found in the given image": 
            self.schedule_update_ha_state()
            return
    
        self._predictions = self._predictions["result"]
    
        if len(self._predictions) > 0:
            self._last_detection = dt_util.now().strftime(DATETIME_FORMAT)
            self.total_faces = len(self._predictions)
            self.faces = get_faces(self._predictions, image_width, image_height)
            self._matched = get_matched_faces(self.faces, self.confidence)
            self.process_faces(
                self.faces, self.total_faces,
            ) #Fires an event for each matched face.
            
            if not self._detect_only:
                if self._save_faces and self._save_faces_folder:
                    self.save_faces(
                        pil_image, self._save_faces_folder
                    )

            if self._save_file_folder:
                self.save_image(
                    pil_image, self._save_file_folder,
                )
        else:
            self.total_faces = None
            self._matched = {}    

        self.schedule_update_ha_state()


    def teach(self, name: str, url_list: str):
        """Teach classifier a face."""
        image_list = [get_image_by_url(url) for url in url_list] 
        pictures_single_face = 0 
        pictures_multiple_face = 0
        pictures_no_face = 0
        picture_indexes_to_remove = []
    
        for i in range(len(image_list)):
            n_faces = self.faces_in_picture(image_list[i]) 
            if n_faces == 1: 
                pictures_single_face += 1
            elif n_faces == 0:
                pictures_no_face += 1
                picture_indexes_to_remove.append(i)       
            else:
                pictures_multiple_face += 1
                picture_indexes_to_remove.append(i)

        #Remove pictures with no faces or with more than one face
        image_list = [i for j, i in enumerate(image_list) if j not in picture_indexes_to_remove] 
        notify_message = create_notify_message(name, pictures_single_face, pictures_no_face, pictures_multiple_face)
        if pictures_single_face == 0: 
            self.hass.components.persistent_notification.async_create(
                notify_message,
                title="Aprender caras",
                notification_id="teach_face_result",
                )
            raise NoUsablePhotoException(f"Homeland raised an error registering faces: {notify_message}")
            
        try: 
            for img in image_list: 
                self.face_collection.add(image_path=img, subject=name)
        except ConnectionError: 
            _LOGGER.error(COMPREFACE_CONNECT_ERROR_MESSAGE.format(self.ip_address, self.port))
            return False
        
        self.hass.components.persistent_notification.async_create(
            notify_message,
            title="Aprender caras",
            notification_id="teach_face_result",
            ) 
        
        self.hass.bus.async_fire(
            f"{DOMAIN}_teach_face", 
            event_data = {
                "person_name": name, 
                "image_number": len(image_list)
            })

        return True


    def faces_in_picture(self, image): 
        """Returns the number of face in a picture"""
        return len(self.detection.detect(image).get("result", []))

    def get_stored_faces(self): 
        """Wrapper function to get the stored faces in compreFace"""
        try: 
            self._registered_faces  = self.subjects.list()["subjects"]
            return True
        except ConnectionRefusedError: 
            _LOGGER.error(COMPREFACE_CONNECT_ERROR_MESSAGE.format(self.ip_address, self.port))
            return False

    def delete_stored_faces(self, name):
        if name in self._registered_faces: 
            try: 
                self.subjects.delete(name)
                self._registered_faces.remove(name)
            except ConnectionRefusedError: 
               _LOGGER.error(COMPREFACE_CONNECT_ERROR_MESSAGE.format(self.ip_address, self.port))
        else: 
            _LOGGER.error(f"Error, no face ith for the user {name} is registered")
    
    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property 
    def confidence(self) -> float | None:
        return self._confidence
    
    @property
    def registered_faces(self): 
        """Return registered faces """
        return self._registered_faces

    @property
    def state(self):
        """Ensure consistent state."""
        return self.total_faces

    @property
    def should_poll(self):
        """Return the polling state."""
        return False

    @property
    def force_update(self):
        """Force update to fire state events even if state has not changed."""
        return True

    @property
    def extra_state_attributes(self):
        """Return the classifier attributes."""
        attr = {}
        if self._detect_only:
            attr[CONF_DETECT_ONLY] = self._detect_only
        if not self._detect_only:
            attr["total_matched_faces"] = len(self._matched)
            attr["matched_faces"] = self._matched
        if self._last_detection:
            attr["last_detection"] = self._last_detection
        return attr


    def save_faces(self, pil_image: Image, directory: Path):
        """Saves recognized faces."""
        for face in self.faces:
            box = face["bounding_box"]
            confidence = face["confidence"]
            face_name = face["name"]

            cropped_image = pil_image.crop(
                (box["x_min"], box["y_min"], box["x_max"], box["y_max"])
            )

            timestamp_save_path = directory / f"{face_name}_{confidence:.1f}_{self._last_detection}.jpg"
            cropped_image.save(timestamp_save_path)
            _LOGGER.info("Saved face %s", timestamp_save_path)

    def save_image(self, pil_image: Image, directory: Path):
        """Draws the actual bounding box of the detected objects."""
        image_width, image_height = pil_image.size
        draw = ImageDraw.Draw(pil_image)
        for face in self.faces:
            if not self._show_boxes:
                break
            name = face["name"]
            confidence = face["confidence"]
            box = face["bounding_box"]
            box_label = f"{name}: {confidence:.1f}%"

            draw_box(
                draw,
                (box["y_min"], box["x_min"], box["y_max"], box["x_max"]),
                image_width,
                image_height,
                text=box_label,
                color=RED,
            )

        latest_save_path = (
            directory / f"{get_valid_filename(self._name).lower()}_latest.jpg"
        )
        pil_image.save(latest_save_path)

        if self._save_timestamped_file:
            timestamp_save_path = directory / f"{self._name}_{self._last_detection}.jpg"
            pil_image.save(timestamp_save_path)
            _LOGGER.info("Deepstack saved file %s", timestamp_save_path)
    
    @callback
    def _update(self) -> None:
        """Update the image processing entity."""
        _LOGGER.warn("Updating sensor")

def get_valid_filename(name: str) -> str:
    return re.sub(r"(?u)[^-\w.]", "", str(name).strip().replace(" ", "_"))


def get_faces(predictions: list, img_width: int, img_height: int):
    """Return faces with formatting for annotating images. Matches that do not meet the treshold are removed"""
    #TODO: Make a lot of tests for this function
    faces = []
    decimal_places = 3
    #name, max_confidance = get_max_confidance_subject()
    for pred in predictions:
        if pred["subjects"] == []:
            name = "unknown"
        else:
            max_confidance = 0
            name = ""
            for subject in pred["subjects"]: 
                if subject["similarity"] > max_confidance: 
                    name = subject["subject"] 
                    max_confidance = subject["similarity"]

        confidence = round(max_confidance * 100, decimal_places)
        box = pred["box"]
        box_width = box["x_max"] - box["x_min"]
        box_height = box["y_max"] - box["y_min"]
        box = {
            "height": round(box_height / img_height, decimal_places),
            "width": round(box_width / img_width, decimal_places),
            "y_min": round(box["y_min"] / img_height, decimal_places),
            "x_min": round(box["x_min"] / img_width, decimal_places),
            "y_max": round(box["y_max"] / img_height, decimal_places),
            "x_max": round(box["x_max"] / img_width, decimal_places),
        }
        faces.append(
            {"name": name, "confidence": confidence, "bounding_box": box}
        )
    return faces

def get_matched_faces(faces, min_confidence_treshold): 
    """Check number of mached faces"""
    return [face["name"] for face in faces if face["name"] != "unknown" and face["confidence"] >= min_confidence_treshold] 