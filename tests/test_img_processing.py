"""Test the normal start of the dashboard AI image processing entity"""
import json
import pytest

from unittest.mock import PropertyMock, patch
from pathlib import Path

from homeassistant.const import CONF_IP_ADDRESS, CONF_PORT
from homeassistant.setup import async_setup_component

from pytest_homeassistant_custom_component.common import (
    MockConfigEntry,
    load_fixture
)

from .conftest import mock_requests_get

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

from custom_components.ai_dashboard.helper import get_image_by_url

FIXTURES_TEST = json.loads(load_fixture("config_flow_fixture.json"))

@pytest.mark.asyncio
async def test_image_processing(hass):
    """Tests that the image processing entity is correctly setup"""
    fixture_test = FIXTURES_TEST["default"]["config_flow_data"]

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

    fixture_test = FIXTURES_TEST["default"]["config_flow_data"]

    mock_image_processing_entity = setup_face_classify_entity(hass, config_entry.data)

    assert mock_image_processing_entity.ip_address == fixture_test["ip_address"]
    assert mock_image_processing_entity._save_file_folder == Path(fixture_test["save_file_folder"])
    assert mock_image_processing_entity._save_faces_folder == Path(fixture_test["save_faces_folder"])
    assert mock_image_processing_entity.ip_address == fixture_test["ip_address"]
    assert mock_image_processing_entity.port == fixture_test["port"]
    assert mock_image_processing_entity.recognition_api_key == fixture_test["api_recognition_key"]
    assert mock_image_processing_entity.detection_api_key == fixture_test["api_detetion_key"]
    assert mock_image_processing_entity._timeout == fixture_test["timeout"]
    assert mock_image_processing_entity._min_confidance == fixture_test["min_confidance"]
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
    fixture_test = FIXTURES_TEST["default"]["config_flow_data"]
    mock_image_processing_entity = setup_face_classify_entity(hass, fixture_test)

    image = "img/single_face_stock_photo"
    mock_get = mock_requests_get(image)

    with patch('requests.get', mock_get
    ), patch("compreface.collections.face_collections.FaceCollection.add"
    ), patch("compreface.service.detection_service.DetectionService.detect", return_value = {"result": ["Foo"]}):
        assert await hass.async_add_executor_job(
            mock_image_processing_entity.teach, "John", ["http://mock.com/my_image.jpg"])

        