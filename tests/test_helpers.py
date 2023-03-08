"""Test the dashboard AI helper functions"""

import unittest
from custom_components.ai_dashboard.helper import create_notify_message

class TestCreateNotifyMessage(unittest.TestCase):

    def test_single_face(self):
        name = "John"
        pictures_single_face = 5
        pictures_no_face = 0
        pictures_multiple_face = 0
        expected_output = "Cara de John aprendida com 5 imagem(s)"
        self.assertEqual(create_notify_message(name, pictures_single_face, pictures_no_face, pictures_multiple_face), expected_output)

    def test_multiple_faces(self):
        name = "Mary"
        pictures_single_face = 2
        pictures_no_face = 0
        pictures_multiple_face = 3
        expected_output = "Tentativa de aprender cara de Mary com 5 imagens\nApenas foi possivel treinar com 2 imagens:\n\t- Em 0 imagem(s) não foi encontrada qualquer cara\n\t- Em 3 imagem(s) foram encontradas várias caras"
        self.assertEqual(create_notify_message(name, pictures_single_face, pictures_no_face, pictures_multiple_face), expected_output)

    def test_no_face(self):
        name = "Peter"
        pictures_single_face = 0
        pictures_no_face = 5
        pictures_multiple_face = 0
        expected_output = "Tentativa de aprender cara de Peter com 5 imagens\nNão foi possivel aprender a cara de Peter. Verifique se as imagens usadas contem apenas uma cara e se têm boa iluminação.\n\t- Em 5 imagem(s) não foi encontrada qualquer cara\n\t- Em 0 imagem(s) foram encontradas várias caras"
        self.assertEqual(create_notify_message(name, pictures_single_face, pictures_no_face, pictures_multiple_face), expected_output)

if __name__ == '__main__':
    unittest.main()
