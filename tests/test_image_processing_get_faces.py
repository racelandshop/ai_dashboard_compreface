"""Test get face function from image_processing"""

from custom_components.ai_dashboard.image_processing import get_faces

import unittest

class TestGetFaces(unittest.TestCase):
    def test_detect_only(self):
        predictions = [
            {
                "box": {
                    "x_min": 200,
                    "x_max": 300,
                    "y_min": 100,
                    "y_max": 200,
                    "probability": 0.9
                },
                "subjects": []
            }
        ]
        img_width = 640
        img_height = 480
        detect_only = True
        expected_result = [
            {
                "name": "unknown",
                "confidence": 90.0,
                "bounding_box": {
                    "height": 0.208,
                    "width": 0.156,
                    "y_min": 0.208,
                    "x_min": 0.312,
                    "y_max": 0.417,
                    "x_max": 0.469,
                }
            }
        ]
        result = get_faces(predictions, img_width, img_height, detect_only)
        self.assertEqual(result, expected_result)

    def test_with_subjects(self):
        predictions = [
            {
                "box": {
                    "x_min": 200,
                    "x_max": 300,
                    "y_min": 100,
                    "y_max": 200,
                    "probability": 0.9
                },
                "subjects": [
                    {
                        "subject": "John Doe",
                        "similarity": 0.8
                    }
                ]
            }
        ]
        img_width = 640
        img_height = 480
        detect_only = False
        expected_result = [
            {
                "name": "John Doe",
                "confidence": 80.0,
                "bounding_box": {
                    "height": 0.208,
                    "width": 0.156,
                    "y_min": 0.208,
                    "x_min": 0.312,
                    "y_max": 0.417,
                    "x_max": 0.469,
                }
            }
        ]
        result = get_faces(predictions, img_width, img_height, detect_only)
        self.assertEqual(result, expected_result)

    def test_multiple_subjects_in_prediction(self):
        predictions = [
            {
                "box": {
                    "x_min": 200,
                    "x_max": 300,
                    "y_min": 100,
                    "y_max": 200,
                    "probability": 0.9
                },
                "subjects": [
                    {
                        "subject": "John Doe",
                        "similarity": 0.8
                    },
                    {
                        "subject": "Jane Doe",
                        "similarity": 0.7
                    }
                ]
            }
        ]
        img_width = 640
        img_height = 480
        detect_only = False
        expected_result = [
            {
                "name": "John Doe",
                "confidence": 80.0,
                "bounding_box": {
                    "height": 0.208,
                    "width": 0.156,
                    "y_min": 0.208,
                    "x_min": 0.312,
                    "y_max": 0.417,
                    "x_max": 0.469,
                }
            }
        ]
        result = get_faces(predictions, img_width, img_height, detect_only)
        self.assertEqual(result, expected_result)


    def test_multiple_subjects(self):
        predictions = [
        {
        "box": {
            "x_min": 200,
            "x_max": 300,
            "y_min": 100,
            "y_max": 200,
            "probability": 0.9
        },
          "subjects": [
            {
              "subject": "Jon Doe",
              "similarity": 0.85
            }
          ],
        },
        {
          "box": {
            "probability": 0.99671,
            "x_max": 587,
            "y_max": 634,
            "x_min": 293,
            "y_min": 315
          },
          "subjects": [
            {
              "subject": "Joan Doe",
              "similarity": 0.9
            }
          ]
        }]
        
        img_width = 640
        img_height = 480
        detect_only = False
        expected_result = [
        {
            "name": "Jon Doe",
            "confidence": 85.0,
            "bounding_box": {
                "height": 0.208,
                "width": 0.156,
                "y_min": 0.208,
                "x_min": 0.312,
                "y_max": 0.417,
                "x_max": 0.469,
            }
        },
        {
            "name": "Joan Doe",
            "confidence": 90.0,
            "bounding_box": {
                "height": 0.665,
                "width": 0.459,
                "y_min": 0.656,
                "x_min": 0.458,
                "y_max": 1.321,
                "x_max": 0.917,
            }
        }]
    
        result = get_faces(predictions, img_width, img_height, detect_only)
        self.assertEqual(result, expected_result)