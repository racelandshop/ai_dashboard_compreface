"""Test image processing helper functions"""

import unittest

from custom_components.ai_dashboard.image_processing import get_matched_faces

class TestGetMatchedFaces(unittest.TestCase):
    def test_no_matches(self):
        faces = [
            {'name': 'owner', 'similarity': 0.0, 'bounding_box': {'height': 0.678, 'width': 0.342, 'y_min': 0.089, 'x_min': 0.0, 'y_max': 0.767, 'x_max': 0.342}},
            {'name': 'testeSubject', 'similarity': 0.0, 'bounding_box': {'height': 0.678, 'width': 0.342, 'y_min': 0.089, 'x_min': 0.0, 'y_max': 0.767, 'x_max': 0.342}},
        ]
        min_confidence_treshold = 80
        self.assertEqual(get_matched_faces(faces, min_confidence_treshold), [])
        
    def test_one_match(self):
        faces = [
            {'name': 'owner', 'similarity': 90, 'bounding_box': {'height': 0.678, 'width': 0.342, 'y_min': 0.089, 'x_min': 0.0, 'y_max': 0.767, 'x_max': 0.342}},
            {'name': 'testeSubject', 'similarity': 0.0, 'bounding_box': {'height': 0.678, 'width': 0.342, 'y_min': 0.089, 'x_min': 0.0, 'y_max': 0.767, 'x_max': 0.342}},
        ]
        min_confidence_treshold = 80
        self.assertEqual(get_matched_faces(faces, min_confidence_treshold), ['owner'])
        
    def test_multiple_matches(self):
        faces = [
            {'name': 'owner', 'similarity': 90, 'bounding_box': {'height': 0.678, 'width': 0.342, 'y_min': 0.089, 'x_min': 0.0, 'y_max': 0.767, 'x_max': 0.342}},
            {'name': 'testeSubject', 'similarity': 0.0, 'bounding_box': {'height': 0.678, 'width': 0.342, 'y_min': 0.089, 'x_min': 0.0, 'y_max': 0.767, 'x_max': 0.342}},
            {'name': 'foo', 'similarity': 85, 'bounding_box': {'height': 0.678, 'width': 0.342, 'y_min': 0.089, 'x_min': 0.0, 'y_max': 0.767, 'x_max': 0.342}},
          ]
        min_confidence_treshold = 80
        self.assertEqual(get_matched_faces(faces, min_confidence_treshold), ['owner', 'foo'])

    def test_equal_match(self):
        faces = [
            {'name': 'owner', 'similarity': 90, 'bounding_box': {'height': 0.678, 'width': 0.342, 'y_min': 0.089, 'x_min': 0.0, 'y_max': 0.767, 'x_max': 0.342}},
            {'name': 'testeSubject', 'similarity': 90, 'bounding_box': {'height': 0.678, 'width': 0.342, 'y_min': 0.089, 'x_min': 0.0, 'y_max': 0.767, 'x_max': 0.342}},
            {'name': 'foo', 'similarity': 89.9, 'bounding_box': {'height': 0.678, 'width': 0.342, 'y_min': 0.089, 'x_min': 0.0, 'y_max': 0.767, 'x_max': 0.342}},
          ]
        min_confidence_treshold = 90
        self.assertEqual(get_matched_faces(faces, min_confidence_treshold), ['owner', 'testeSubject'])

    def test_empty_faces_list(self):
        faces = []
        min_confidence_treshold = 80
        self.assertEqual(get_matched_faces(faces, min_confidence_treshold), [])

    def test_unknown_face_list(self):
        faces = [
            {'name': 'owner', 'similarity': 90, 'bounding_box': {'height': 0.678, 'width': 0.342, 'y_min': 0.089, 'x_min': 0.0, 'y_max': 0.767, 'x_max': 0.342}},
            {'name': 'unknown', 'similarity': 90, 'bounding_box': {'height': 0.678, 'width': 0.342, 'y_min': 0.089, 'x_min': 0.0, 'y_max': 0.767, 'x_max': 0.342}},
        ]
        min_confidence_treshold = 80
        self.assertEqual(get_matched_faces(faces, min_confidence_treshold), ["owner"])

        
if __name__ == '__main__':
    unittest.main()