import io
from unittest import mock

from viz_ai_image.app import BASEDIR


def test_image(client):
    image_path = '{}/tests/images/image1.jpeg'.format(BASEDIR)
    image_data = open(image_path, 'rb').read()
    data = dict(file=(io.BytesIO(image_data), 'image1.jpeg'))
    rv = client.post('/face', data=data, content_type='multipart/form-data')
    assert rv.status_code == 200


def test_image_no_name(client):
    image_path = '{}/tests/images/image1.jpeg'.format(BASEDIR)
    image_data = open(image_path, 'rb').read()
    data = dict(file=(io.BytesIO(image_data), ''))
    rv = client.post('/face', data=data, content_type='multipart/form-data')
    assert rv.json.get('err_msg') == 'No file part'


def test_image_no_file(client):
    data = dict()
    rv = client.post('/face', data=data, content_type='multipart/form-data')
    assert rv.json.get('err_msg') == 'No file part'


def test_error_in_emotion(client):
    with mock.patch.dict('os.environ', {'SUBSCRIPTION_KEY': ''}):
        image_path = '{}/tests/images/image1.jpeg'.format(BASEDIR)
        image_data = open(image_path, 'rb').read()
        data = dict(file=(io.BytesIO(image_data), 'image1.jpeg'))
        rv = client.post('/face', data=data, content_type='multipart/form-data')
        assert rv.json.get('err_msg') == 'Access denied due to invalid subscription key. Make sure you are subscribed to an API you are trying to call and provide the right key.'  # noqa
