import os
import cognitive_face as cf


def detect_faces_and_emotion(image_data):
    key = os.environ.get('SUBSCRIPTION_KEY')
    cf.Key.set(key)

    base_url = 'https://westcentralus.api.cognitive.microsoft.com/face/v1.0'
    cf.BaseUrl.set(base_url)

    faces = cf.face.detect(image_data, attributes='emotion')

    return faces
