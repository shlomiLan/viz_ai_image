import io

from viz_ai_image.app import BASEDIR


def test_face(client):
    rv = client.get('/upload')
    assert rv.status_code == 200


def test_post_image(client):
    image_path = '{}/tests/images/image1.jpeg'.format(BASEDIR)
    image_data = open(image_path, 'rb').read()
    data = dict(file=(io.BytesIO(image_data), 'image1.jpeg'))
    # data = dict(file=image_path)
    rv = client.post('/face', data=data, content_type='multipart/form-data')
    assert rv.status_code == 200
