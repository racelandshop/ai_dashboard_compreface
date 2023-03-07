"""Helper function used in AI dashboard"""
from __future__ import annotations

import requests
from io import BytesIO


def get_image_by_url(url: str): 
    """Get an image url from homeassistant after the upload"""
    response = requests.get(url)
    return response.content

def create_notify_message(name, pictures_single_face, pictures_no_face, pictures_multiple_face): 
    """Create a notification message to send to the frontend."""
    total = pictures_multiple_face + pictures_single_face + pictures_no_face
    if total == pictures_single_face: 
        message = f"Cara de {name} aprendida com {total} imagem(s)"

    else: 
        message = f"Tentativa de aprender cara de {name} com {total}"
        if (total == 1): 
            message += " imagem\n"
        else: 
            message += " imagens\n"

        if pictures_single_face != 0: 
            message += f"Apenas foi possivel treinar com {pictures_single_face} imagens:\n"
        else: 
            message += f"Não foi possivel aprender a cara de {name}. Verifique se as imagens usadas contem apenas uma cara e se têm boa iluminação.\n"
        
        message += f"\t- Em {pictures_no_face} imagem(s) não foi encontrada qualquer cara\n\t- Em {pictures_multiple_face} imagem(s) foram encontradas várias caras"
    return message