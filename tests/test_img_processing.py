"""Test the normal start of the dashboard AI image processing entity"""
import json
import pytest

from . import generate_dummy_image

from unittest.mock import patch
from pathlib import Path
from PIL import Image

from homeassistant.const import CONF_IP_ADDRESS, CONF_PORT

from pytest_homeassistant_custom_component.common import (
    MockConfigEntry,
    load_fixture
)

from .conftest import mock_requests_get

from custom_components.ai_dashboard.image_processing import FaceClassifyEntity
from custom_components.ai_dashboard.image_processing import setup_face_classify_entity
from custom_components.ai_dashboard.const import (
    DOMAIN,
    CONF_DEV_MODE,
    CONF_API_RECOGNITION_KEY,
    CONF_API_DETECTION_KEY,
    CONF_TIMEOUT,
    CONF_MIN_CONFIDANCE,
    CONF_DETECT_ONLY,
    CONF_SAVE_FILE_FOLDER,
    CONF_SAVE_FACES_FOLDER,
    CONF_SHOW_BOXES,
    CONF_SAVE_TIMESTAMPTED_FILE, 
    CONF_SAVE_FACES
)

from custom_components.ai_dashboard.exceptions import NoUsablePhotoException

FIXTURES_CONFIG_FLOW = json.loads(load_fixture("config_flow_fixture.json"))
FIXTURES_FACIAL_RECOGNITION_RESULTS = json.loads(load_fixture("image_processing_recognize.json"))

@pytest.mark.asyncio
async def test_image_processing(hass):
    """Tests that the image processing entity is correctly setup"""
    fixture_test = FIXTURES_CONFIG_FLOW["default"]["config_flow_data"]

    config_entry = MockConfigEntry(
        domain=DOMAIN,
        source="user",
        data={
            CONF_DEV_MODE: fixture_test[CONF_DEV_MODE],
            CONF_IP_ADDRESS: fixture_test[CONF_IP_ADDRESS],
            CONF_PORT: fixture_test[CONF_PORT],
            CONF_API_RECOGNITION_KEY: fixture_test[CONF_API_RECOGNITION_KEY],
            CONF_API_DETECTION_KEY: fixture_test[CONF_API_DETECTION_KEY],
            CONF_TIMEOUT: fixture_test[CONF_TIMEOUT], 
            CONF_MIN_CONFIDANCE: fixture_test[CONF_MIN_CONFIDANCE],
            CONF_DETECT_ONLY : fixture_test[CONF_DETECT_ONLY], 
            CONF_SAVE_FILE_FOLDER: fixture_test[CONF_SAVE_FILE_FOLDER],
            CONF_SAVE_FACES_FOLDER: fixture_test[CONF_SAVE_FACES_FOLDER],
            CONF_SHOW_BOXES: fixture_test[CONF_SHOW_BOXES], 
            CONF_SAVE_TIMESTAMPTED_FILE: fixture_test[CONF_SHOW_BOXES],
            CONF_SAVE_FACES: fixture_test[CONF_SAVE_FACES],
        },
        unique_id="config_flow",
        options={},
        entry_id="1"
    )
    config_entry.add_to_hass(hass)
    await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()

    fixture_test = FIXTURES_CONFIG_FLOW["default"]["config_flow_data"]

    mock_image_processing_entity = setup_face_classify_entity(hass, config_entry.data)

    assert mock_image_processing_entity.ip_address == fixture_test["ip_address"]
    assert mock_image_processing_entity._save_file_folder == Path(fixture_test["save_file_folder"])
    assert mock_image_processing_entity._save_faces_folder == Path(fixture_test["save_faces_folder"])
    assert mock_image_processing_entity.ip_address == fixture_test["ip_address"]
    assert mock_image_processing_entity.port == fixture_test["port"]
    assert mock_image_processing_entity.recognition_api_key == fixture_test["api_recognition_key"]
    assert mock_image_processing_entity.detection_api_key == fixture_test["api_detetion_key"]
    assert mock_image_processing_entity._timeout == fixture_test["timeout"]
    assert mock_image_processing_entity.confidence == fixture_test["min_confidance"]
    assert mock_image_processing_entity._detect_only == fixture_test["detect_only"]
    assert mock_image_processing_entity._show_boxes == fixture_test["show_boxes"]
    assert mock_image_processing_entity._save_timestamped_file == fixture_test["save_timestamped_file"]
    assert mock_image_processing_entity._save_faces == fixture_test["save_faces"]
    assert mock_image_processing_entity._name == "face_recognition_central"
    assert mock_image_processing_entity._predictions == []
    assert mock_image_processing_entity._matched == {}
    assert mock_image_processing_entity._registered_faces == {}
    assert mock_image_processing_entity.total_faces == None

@pytest.mark.asyncio
async def test_image_processing_teach_identify_single_photo(hass, mock_requests_get):
    """Test teach using a single photo with a single face"""
    fixture_test = FIXTURES_CONFIG_FLOW["default"]["config_flow_data"]
    mock_image_processing_entity = setup_face_classify_entity(hass, fixture_test)
    mock_get = mock_requests_get("test_image.jpeg")

    with patch('requests.get', mock_get
    ), patch("compreface.collections.face_collections.FaceCollection.add"
    ), patch("compreface.service.detection_service.DetectionService.detect", return_value = {"result": ["Foo"]}):
        assert await hass.async_add_executor_job(
            mock_image_processing_entity.teach, "John", ["http://mock.com/my_image.jpg"])

@pytest.mark.asyncio
async def test_image_processing_teach_identify_multi_face_photo(hass, mock_requests_get):
    """Test teach using a single photo with more than one face"""
    fixture_test = FIXTURES_CONFIG_FLOW["default"]["config_flow_data"]
    mock_image_processing_entity = setup_face_classify_entity(hass, fixture_test)
    mock_get = mock_requests_get("test_image.jpeg")

    with patch('requests.get', mock_get
    ), patch("compreface.collections.face_collections.FaceCollection.add"
    ), patch("compreface.service.detection_service.DetectionService.detect", return_value = {"result": ["Foo", "Bar"]}, 
    ), pytest.raises(NoUsablePhotoException):
        assert await hass.async_add_executor_job(
            mock_image_processing_entity.teach, "John", ["http://mock.com/my_image.jpg"])

@pytest.mark.asyncio
async def test_image_processing_teach_identify_no_face_photo(hass, mock_requests_get):
    """Test teach using a single photo with no face"""
    fixture_test = FIXTURES_CONFIG_FLOW["default"]["config_flow_data"]
    mock_image_processing_entity = setup_face_classify_entity(hass, fixture_test)
    mock_get = mock_requests_get("test_image.jpeg")

    with patch('requests.get', mock_get
    ), patch("compreface.collections.face_collections.FaceCollection.add"
    ), patch("compreface.service.detection_service.DetectionService.detect", return_value = {"result": []}, 
    ), pytest.raises(NoUsablePhotoException):
        assert await hass.async_add_executor_job(
            mock_image_processing_entity.teach, "John", ["http://mock.com/my_image.jpg"])

@pytest.mark.asyncio
async def test_image_processing_teach_identify_multiple_photos(hass, mock_requests_get):
    """Test using multiple photos, each one of one face"""
    fixture_test = FIXTURES_CONFIG_FLOW["default"]["config_flow_data"]
    mock_image_processing_entity = setup_face_classify_entity(hass, fixture_test)
    mock_get = mock_requests_get("test_image.jpeg")

    with patch('requests.get', mock_get
    ), patch("compreface.collections.face_collections.FaceCollection.add"
    ), patch("compreface.service.detection_service.DetectionService.detect", return_value = {"result": ["Foo"]}):
        assert await hass.async_add_executor_job(
            mock_image_processing_entity.teach, "John", ["http://mock.com/my_image.jpg", "http://mock.com/my_image.jpg"])

@pytest.mark.asyncio
async def test_image_processing_faces_in_picture(hass, mock_requests_get):
    """Test the return of faces_in_picture function"""
    fixture_test = FIXTURES_CONFIG_FLOW["default"]["config_flow_data"]
    mock_image_processing_entity = setup_face_classify_entity(hass, fixture_test)

    with patch("compreface.collections.face_collections.FaceCollection.add"
    ), patch("compreface.service.detection_service.DetectionService.detect", return_value = {"result": ["Foo"]}):
        assert mock_image_processing_entity.faces_in_picture(b"mock_image") == 1

@pytest.mark.asyncio
async def test_image_processing_no_faces_in_picture(hass):
    """Test the return of faces_in_picture function"""
    fixture_test = FIXTURES_CONFIG_FLOW["default"]["config_flow_data"]
    mock_image_processing_entity = setup_face_classify_entity(hass, fixture_test)

    with patch("compreface.collections.face_collections.FaceCollection.add"
    ), patch("compreface.service.detection_service.DetectionService.detect", return_value = {"result": []}):
        assert mock_image_processing_entity.faces_in_picture(b"mock_image") == 0

@pytest.mark.asyncio
async def test_image_processing_multiple_faces_in_picture(hass):
    """Test the return of faces_in_picture function"""
    fixture_test = FIXTURES_CONFIG_FLOW["default"]["config_flow_data"]
    mock_image_processing_entity = setup_face_classify_entity(hass, fixture_test)

    with patch("compreface.collections.face_collections.FaceCollection.add"
    ), patch("compreface.service.detection_service.DetectionService.detect", return_value = {"result": ["foo", "bar"]}):
        assert mock_image_processing_entity.faces_in_picture(b"mock_image") == 2

@pytest.mark.asyncio
async def test_image_facial_recognition_single_face(hass):
    """Test the return of faces_in_picture function with only one face"""
    fixture_test = FIXTURES_CONFIG_FLOW["default"]["config_flow_data"]
    mock_image_processing_entity = setup_face_classify_entity(hass, fixture_test)
    image_bytes = generate_dummy_image()
    recognition_output = FIXTURES_FACIAL_RECOGNITION_RESULTS["single_face"]["prediction"]
    with patch("compreface.service.recognition_service.RecognitionService.recognize", return_value = recognition_output
    ), patch("PIL.Image.Image.save"
    ), patch("custom_components.ai_dashboard.image_processing.FaceClassifyEntity.schedule_update_ha_state"): #I need to patch this since the entity does not have a entity_id
        await hass.async_add_executor_job(
            mock_image_processing_entity.process_image,image_bytes)
        
        assert mock_image_processing_entity._predictions == FIXTURES_FACIAL_RECOGNITION_RESULTS["single_face"]["prediction"]["result"]
        assert mock_image_processing_entity._matched == ["owner"]
        assert mock_image_processing_entity.total_faces == 1
        assert mock_image_processing_entity.faces == FIXTURES_FACIAL_RECOGNITION_RESULTS["single_face"]["results"]["faces"]

@pytest.mark.asyncio
async def test_image_facial_recognition_multiple_faces(hass):
    """Test the return of faces_in_picture function with multiple faces, both passing the similarity treshold"""
    fixture_test = FIXTURES_CONFIG_FLOW["default"]["config_flow_data"]
    mock_image_processing_entity = setup_face_classify_entity(hass, fixture_test)
    image_bytes = generate_dummy_image()
    recognition_output = FIXTURES_FACIAL_RECOGNITION_RESULTS["multiple_faces"]["prediction"]
    with patch("compreface.service.recognition_service.RecognitionService.recognize", return_value = recognition_output
    ), patch("PIL.Image.Image.save"
    ), patch("custom_components.ai_dashboard.image_processing.FaceClassifyEntity.schedule_update_ha_state"): #I need to patch this since the entity does not have a entity_id
        await hass.async_add_executor_job(
            mock_image_processing_entity.process_image,image_bytes)
        
        assert mock_image_processing_entity._predictions == FIXTURES_FACIAL_RECOGNITION_RESULTS["multiple_faces"]["prediction"]["result"]
        assert mock_image_processing_entity._matched == ["owner", "ownerWife"]
        assert mock_image_processing_entity.total_faces == 2
        assert mock_image_processing_entity.faces == FIXTURES_FACIAL_RECOGNITION_RESULTS["multiple_faces"]["results"]["faces"]

@pytest.mark.asyncio
async def test_image_facial_recognition_multiple_faces_2(hass):
    """Test the return of faces_in_picture function with multiple faces, with one of the not passing the similarity treshold"""
    fixture_test = FIXTURES_CONFIG_FLOW["default"]["config_flow_data"]
    mock_image_processing_entity = setup_face_classify_entity(hass, fixture_test)
    image_bytes = generate_dummy_image()
    recognition_output = FIXTURES_FACIAL_RECOGNITION_RESULTS["multiple_faces2"]["prediction"]
    with patch("compreface.service.recognition_service.RecognitionService.recognize", return_value = recognition_output
    ), patch("PIL.Image.Image.save"
    ), patch("custom_components.ai_dashboard.image_processing.FaceClassifyEntity.schedule_update_ha_state"): #I need to patch this since the entity does not have a entity_id
        await hass.async_add_executor_job(
            mock_image_processing_entity.process_image,image_bytes)
        
        assert mock_image_processing_entity._predictions == FIXTURES_FACIAL_RECOGNITION_RESULTS["multiple_faces2"]["prediction"]["result"]
        assert mock_image_processing_entity._matched == ["owner"]
        assert mock_image_processing_entity.total_faces == 2
        assert mock_image_processing_entity.faces == FIXTURES_FACIAL_RECOGNITION_RESULTS["multiple_faces2"]["results"]["faces"]

@pytest.mark.asyncio
async def test_image_facial_recognition_single_face(hass):
    """Test the return of faces_in_picture function with only one face"""
    fixture_test = FIXTURES_CONFIG_FLOW["default"]["config_flow_data"]
    mock_image_processing_entity = setup_face_classify_entity(hass, fixture_test)
    image_bytes = generate_dummy_image()
    recognition_output = FIXTURES_FACIAL_RECOGNITION_RESULTS["single_face"]["prediction"]
    with patch("compreface.service.recognition_service.RecognitionService.recognize", return_value = recognition_output
    ), patch("PIL.Image.Image.save"
    ), patch("custom_components.ai_dashboard.image_processing.FaceClassifyEntity.schedule_update_ha_state"): #I need to patch this since the entity does not have a entity_id
        await hass.async_add_executor_job(
            mock_image_processing_entity.process_image,image_bytes)
        
        assert mock_image_processing_entity._predictions == FIXTURES_FACIAL_RECOGNITION_RESULTS["single_face"]["prediction"]["result"]
        assert mock_image_processing_entity._matched == ["owner"]
        assert mock_image_processing_entity.total_faces == 1
        assert mock_image_processing_entity.faces == FIXTURES_FACIAL_RECOGNITION_RESULTS["single_face"]["results"]["faces"]

@pytest.mark.asyncio
async def test_image_facial_detection_single_face(hass):
    """Test facial detection in a single face"""
    test_setup = "single_face_detection"

    fixture_test = FIXTURES_CONFIG_FLOW["detection_setup"]["config_flow_data"]
    mock_image_processing_entity = setup_face_classify_entity(hass, fixture_test)
    image_bytes = generate_dummy_image()
    detection_output = FIXTURES_FACIAL_RECOGNITION_RESULTS[test_setup]["prediction"]
    with patch("PIL.Image.Image.save"
    ), patch("compreface.service.detection_service.DetectionService.detect", return_value = detection_output
    ), patch("custom_components.ai_dashboard.image_processing.FaceClassifyEntity.schedule_update_ha_state"): #I need to patch this since the entity does not have a entity_id
        await hass.async_add_executor_job(
            mock_image_processing_entity.process_image,image_bytes)
        
        assert mock_image_processing_entity._predictions == FIXTURES_FACIAL_RECOGNITION_RESULTS[test_setup]["prediction"]["result"]
        assert mock_image_processing_entity._matched == []
        assert mock_image_processing_entity.total_faces == 1
        assert mock_image_processing_entity.faces == FIXTURES_FACIAL_RECOGNITION_RESULTS[test_setup]["results"]["faces"]

# @pytest.mark.asyncio
# async def test_image_facial_recognition_no_faces(hass):
#     """Test the return of faces_in_picture function with no face"""
#     fixture_test = FIXTURES_CONFIG_FLOW["default"]["config_flow_data"]
#     mock_image_processing_entity = setup_face_classify_entity(hass, fixture_test)
#     image_bytes = generate_dummy_image()
#     recognition_output = FIXTURES_FACIAL_RECOGNITION_RESULTS["no_face"]["prediction"]
#     with patch("compreface.service.recognition_service.RecognitionService.recognize", return_value = recognition_output
#     ), patch("custom_components.ai_dashboard.image_processing.FaceClassifyEntity.schedule_update_ha_state"): #I need to patch this since the entity does not have a entity_id
#         await hass.async_add_executor_job(
#             mock_image_processing_entity.process_image,image_bytes)
        
#         assert mock_image_processing_entity._predictions == FIXTURES_FACIAL_RECOGNITION_RESULTS["no_face"]["prediction"]
#         assert mock_image_processing_entity._matched == []
#         assert mock_image_processing_entity.total_faces == None

@pytest.mark.asyncio
async def test_save_image_call(hass):
    """Test if the if the save function are being called."""
    fixture_test = FIXTURES_CONFIG_FLOW["default"]["config_flow_data"]
    image_bytes = generate_dummy_image()
    mock_image_processing_entity = setup_face_classify_entity(hass, fixture_test)
    recognition_output = FIXTURES_FACIAL_RECOGNITION_RESULTS["single_face"]["prediction"]
    with patch("compreface.service.recognition_service.RecognitionService.recognize", return_value = recognition_output
    ), patch("custom_components.ai_dashboard.image_processing.FaceClassifyEntity.schedule_update_ha_state"
    ), patch.object(FaceClassifyEntity, "save_faces"
    ) as mock_save_faces, patch.object(FaceClassifyEntity, "save_image") as mock_save_file_latest:
        await hass.async_add_executor_job(
            mock_image_processing_entity.process_image, image_bytes)

        assert mock_save_file_latest.call_count == 1
        assert mock_save_faces.call_count == 1

@pytest.mark.asyncio
async def test_save_image_call_no_save_folders(hass):
    """Test if the if the save function are being called when no save folders are defined"""
    fixture_test = FIXTURES_CONFIG_FLOW["no_save_folder"]["config_flow_data"]
    image_bytes = generate_dummy_image()
    mock_image_processing_entity = setup_face_classify_entity(hass, fixture_test)
    recognition_output = FIXTURES_FACIAL_RECOGNITION_RESULTS["single_face"]["prediction"]
    with patch("compreface.service.recognition_service.RecognitionService.recognize", return_value = recognition_output
    ), patch("custom_components.ai_dashboard.image_processing.FaceClassifyEntity.schedule_update_ha_state"
    ), patch.object(FaceClassifyEntity, "save_faces"
    ) as mock_save_faces, patch.object(FaceClassifyEntity, "save_image") as mock_save_file_latest:
        await hass.async_add_executor_job(
            mock_image_processing_entity.process_image, image_bytes)

        assert mock_save_file_latest.call_count == 0
        assert mock_save_faces.call_count == 0

@pytest.mark.asyncio
async def test_save_images_single_face(hass):
    """Test how many times the PIL.Image.save is being called"""
    fixture_test = FIXTURES_CONFIG_FLOW["default"]["config_flow_data"]
    image_bytes = generate_dummy_image()
    mock_image_processing_entity = setup_face_classify_entity(hass, fixture_test)
    recognition_output = FIXTURES_FACIAL_RECOGNITION_RESULTS["single_face"]["prediction"]
    with patch("compreface.service.recognition_service.RecognitionService.recognize", return_value = recognition_output
    ), patch("custom_components.ai_dashboard.image_processing.FaceClassifyEntity.schedule_update_ha_state"
    ), patch.object(Image.Image, "save") as mock_save_file: 
        await hass.async_add_executor_job(
            mock_image_processing_entity.process_image, image_bytes)
        
        # Image.save is called 3 times: 1 to save the face, 1 to save the image with timestamp and one to save as the latest
        assert mock_save_file.call_count == 3

@pytest.mark.asyncio
async def test_save_images_multiple_faces(hass):
    """Test how many times the PIL.Image.save is being called"""
    fixture_test = FIXTURES_CONFIG_FLOW["default"]["config_flow_data"]
    image_bytes = generate_dummy_image()
    mock_image_processing_entity = setup_face_classify_entity(hass, fixture_test)
    recognition_output = FIXTURES_FACIAL_RECOGNITION_RESULTS["multiple_faces"]["prediction"]
    with patch("compreface.service.recognition_service.RecognitionService.recognize", return_value = recognition_output
    ), patch("custom_components.ai_dashboard.image_processing.FaceClassifyEntity.schedule_update_ha_state"
    ), patch.object(Image.Image, "save") as mock_save_file: 
        await hass.async_add_executor_job(
            mock_image_processing_entity.process_image, image_bytes)

        assert mock_save_file.call_count == 4

@pytest.mark.asyncio
async def test_save_images_single_face_no_face_folder(hass):
    """Test how many times the PIL.Image.save is being called"""
    fixture_test = FIXTURES_CONFIG_FLOW["save_image_folder_no_save_face_folder"]["config_flow_data"]
    image_bytes = generate_dummy_image()
    mock_image_processing_entity = setup_face_classify_entity(hass, fixture_test)
    recognition_output = FIXTURES_FACIAL_RECOGNITION_RESULTS["single_face"]["prediction"]
    with patch("compreface.service.recognition_service.RecognitionService.recognize", return_value = recognition_output
    ), patch("custom_components.ai_dashboard.image_processing.FaceClassifyEntity.schedule_update_ha_state"
    ), patch.object(Image.Image, "save") as mock_save_file: 
        await hass.async_add_executor_job(
            mock_image_processing_entity.process_image, image_bytes)
    
        assert mock_save_file.call_count == 2

@pytest.mark.asyncio
async def test_save_images_single_face_no_save_image_folder(hass):
    """Test how many times the PIL.Image.save is being called"""
    fixture_test = FIXTURES_CONFIG_FLOW["save_face_folder_no_save_file_folder"]["config_flow_data"]
    image_bytes = generate_dummy_image()
    mock_image_processing_entity = setup_face_classify_entity(hass, fixture_test)
    recognition_output = FIXTURES_FACIAL_RECOGNITION_RESULTS["single_face"]["prediction"]
    with patch("compreface.service.recognition_service.RecognitionService.recognize", return_value = recognition_output
    ), patch("custom_components.ai_dashboard.image_processing.FaceClassifyEntity.schedule_update_ha_state"
    ), patch.object(Image.Image, "save") as mock_save_file: 
        await hass.async_add_executor_job(
            mock_image_processing_entity.process_image, image_bytes)
    
        assert mock_save_file.call_count == 1

@pytest.mark.asyncio
async def test_save_images_multiple_face_no_face_folder(hass):
    """Test how many times the PIL.Image.save is being called"""
    fixture_test = FIXTURES_CONFIG_FLOW["save_image_folder_no_save_face_folder"]["config_flow_data"]
    image_bytes = generate_dummy_image()
    mock_image_processing_entity = setup_face_classify_entity(hass, fixture_test)
    recognition_output = FIXTURES_FACIAL_RECOGNITION_RESULTS["multiple_faces"]["prediction"]
    with patch("compreface.service.recognition_service.RecognitionService.recognize", return_value = recognition_output
    ), patch("custom_components.ai_dashboard.image_processing.FaceClassifyEntity.schedule_update_ha_state"
    ), patch.object(Image.Image, "save") as mock_save_file: 
        await hass.async_add_executor_job(
            mock_image_processing_entity.process_image, image_bytes)
    
        assert mock_save_file.call_count == 2

@pytest.mark.asyncio
async def test_save_images_multiple_face_no_save_image_folder(hass):
    """Test how many times the PIL.Image.save is being called"""
    fixture_test = FIXTURES_CONFIG_FLOW["save_face_folder_no_save_file_folder"]["config_flow_data"]
    image_bytes = generate_dummy_image()
    mock_image_processing_entity = setup_face_classify_entity(hass, fixture_test)
    recognition_output = FIXTURES_FACIAL_RECOGNITION_RESULTS["multiple_faces"]["prediction"]
    with patch("compreface.service.recognition_service.RecognitionService.recognize", return_value = recognition_output
    ), patch("custom_components.ai_dashboard.image_processing.FaceClassifyEntity.schedule_update_ha_state"
    ), patch.object(Image.Image, "save") as mock_save_file: 
        await hass.async_add_executor_job(
            mock_image_processing_entity.process_image, image_bytes)
    
        assert mock_save_file.call_count == 2


