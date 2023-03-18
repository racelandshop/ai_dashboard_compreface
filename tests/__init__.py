"""Tests for the AI dashboard component."""

import numpy as np
import io
from PIL import Image

def generate_dummy_image(): 
    """Genera a dummy image to be used as input in the process_image function"""
    image_array = np.random.randint(0, 255, size=(100, 100, 3), dtype=np.uint8)
    image = Image.fromarray(image_array)
    with io.BytesIO() as output:
        image.save(output, format="PNG")
        image_bytes = output.getvalue()
        return image_bytes