import requests
import json
import base64
from io import BytesIO
import os


API_DEV_ENDPOINT = 'https://listmyfurniture.com/version-test/api/1.1/'
API_LIVE_ENDPOINT = 'https://listmyfurniture.com/api/1.1/'

HEADER = {}


def load_authorization_token():
    home_dir = os.path.expanduser("~")
    token_file_path = os.path.join(home_dir, ".lmf")
    with open(token_file_path, "r") as token_file:
        token = token_file.read().strip()
    return token


def load_request_function(call_type):
    if call_type == "POST":
        return requests.post
    if call_type == "PUT":
        return requests.put
    if call_type == "GET":
        return requests.get
    return requests.post

def load_image_file_encoded(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = str(base64.b64encode(image_file.read()))[2:-1]
    return encoded_string

def encode_image(image):
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue())
    encoded_string = str(img_str)[2:-1]
    return encoded_string

def workflow_request(workflow, call_type=None, data=None, live=None):
    header = HEADER
    header['Content-type'] = 'application/json'
    token = load_authorization_token()
    header['Authorization'] = 'Bearer {0}'.format(token)
    if not live:
        base_url = API_DEV_ENDPOINT
    else:
        base_url = API_LIVE_ENDPOINT

    url_endpoint = base_url + "wf/" + workflow

    request_func = load_request_function(call_type)

    response = request_func(url_endpoint, json=data, headers=header)

    if response.status_code != 200:
        raise Exception("Failed Request!")

    return response

def make_property(cover_image, street_name, city, state, zipcode, live=None):
    workflow = "new_property"

    data = dict()
    data['cover_shot'] = dict()
    
    if type(cover_image) is str:
        encoded_image = load_image_file_encoded(cover_image)
    else:
        encoded_image = encode_image(cover_image)

    data['cover_shot']['filename'] = 'test.jpg'
    data['cover_shot']['contents'] = encoded_image
    data['cover_shot']['private'] = False

    data['street_name'] = street_name
    data['city'] = city
    data['state'] = state
    data['zip'] = zipcode

    return workflow_request(workflow, "POST", data, live)

if __name__ == '__main__':
    img = 'input/7.jpg'
    street = '1611 memorial parkway'
    city = 'portland'
    state = 'TX'
    zipcode = "78374"
    live = False
    response = make_property(img, street, city, state, zipcode, live=None)
    print(response)
    print(response.text)

