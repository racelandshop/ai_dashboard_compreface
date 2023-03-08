"""Helper function used in AI dashboard"""
from __future__ import annotations

import requests
from io import BytesIO


def get_image_by_url(url: str): 
    """Get an image url from homeassistant after the upload"""
    response = requests.get(url)
    return response.content

def create_notify_message(name, pictures_single_face, pictures_no_face, pictures_multiple_face): 
    """Create a notification message to send to the frontend.

    Args:
        name (str): The name of the individual whose face is in the pictures.
        pictures_single_face (int): The number of pictures with only one face.
        pictures_no_face (int): The number of pictures with no faces.
        pictures_multiple_face (int): The number of pictures with multiple faces.

    Returns:
        str: The notification message to send to the frontend.

    Raises:
        None.

    This function creates a notification message based on the number of pictures uploaded for a particular individual. The message includes information on the success or failure of the face recognition training, the number of pictures used, and any issues encountered during the process.

    The message will be different depending on the number of pictures with one face, no faces, and multiple faces. If all the pictures have only one face, the message will state that the face of the individual has been learned. If there are multiple faces in some pictures, the message will indicate that only a certain number of pictures were used for training, and provide additional information on the images with multiple faces. If no faces were detected in any of the pictures, the message will state that it was not possible to learn the individual's face and provide guidance on possible reasons why.
    """
    
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