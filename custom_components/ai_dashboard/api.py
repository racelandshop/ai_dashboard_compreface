"""Helper function for the camera dashboard AI. These function should be in the deepstack-python API (in the future). For now I can place them here"""
import requests

from typing import Union, List, Set, Dict
from deepstack.core import DeepstackException

import logging

_LOGGER = logging.Logger(__name__)

## HTTP codes. Keep these there and do not move to the .const file and this functions should go to the API
HTTP_OK = 200
BAD_URL = 404

def delete_stored_faces(url, api_key, timeout, name):
    """Posts a request to delete a stored face
    Note: The request does not perform a check if the name is registered in the deepstack database. I have to perform the check myself"""
    data = {"userid": name, "api_key": api_key}
    try:
        requests.post(url, timeout=timeout, data=data)
    except requests.exceptions.Timeout:
        raise DeepstackException(
            f"Timeout connecting to Deepstack, the current timeout is {timeout} seconds, try increasing this value"
        )
    except requests.exceptions.ConnectionError or requests.exceptions.MissingSchema as exc:
        raise DeepstackException(
            f"Deepstack connection error, check your IP and port: {exc}"
        )
    return True

