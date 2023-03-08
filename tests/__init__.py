"""Tests for the AI dashboard component."""

from custom_components.ai_dashboard.image_processing import FaceClassifyEntity

async def create_mock_image_processing_entity(hass, image_processing_data):
    """Create a mock image processing entity"""
    return FaceClassifyEntity(hass, **image_processing_data)
