import operator
import os
import cognitive_face as cf


def detect_faces_and_emotion(file_path):
    key = os.environ.get('SUBSCRIPTION_KEY')
    cf.Key.set(key)

    base_url = 'https://westcentralus.api.cognitive.microsoft.com/face/v1.0'
    cf.BaseUrl.set(base_url)

    faces = cf.face.detect(file_path, attributes='emotion')

    return faces


def find_max_feeling(data_obj):
    data_obj['feeling'] = max(data_obj.get('faceAttributes').get('emotion').items(), key=operator.itemgetter(1))[0]


def clean_data(data_obj):
    del data_obj['faceId']
    del data_obj['faceAttributes']


def add_image_data(data_obj, image_path):
    image_data = open(image_path, 'rb').read()
    data_obj['image_data'] = image_data
