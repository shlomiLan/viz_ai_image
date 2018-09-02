import os

from tasks import load_yaml_from_file
from viz_ai_image.logic import detect_faces_and_emotion

BASEDIR = os.path.abspath(os.path.dirname(__file__))


def test_one():
    test_data_path = '{}/data.yml'.format(BASEDIR)
    expected_data = load_yaml_from_file(test_data_path)

    # Image 1
    image_path = "/Users/shlomilanton/workscpace/jobs/viz_ai_image/resources/images/image1.jpeg"
    result = detect_faces_and_emotion(image_path)
    clean_faces_data(result)
    assert result == expected_data.get('image1')

    # Image 2
    image_path = "/Users/shlomilanton/workscpace/jobs/viz_ai_image/resources/images/image2.jpg"
    result = detect_faces_and_emotion(image_path)
    clean_faces_data(result)
    assert result == expected_data.get('image2')


def clean_faces_data(faces_data):
    for face in faces_data:
        del face['faceId']
