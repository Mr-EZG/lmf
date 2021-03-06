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
    call_type = call_type.upper()
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
        print(response.text)
        raise Exception("Failed Request!")

    return response


def object_request(object, call_type=None, data=None, live=None):
    header = HEADER
    header['Content-type'] = 'application/json'
    token = load_authorization_token()
    header['Authorization'] = 'Bearer {0}'.format(token)
    if not live:
        base_url = API_DEV_ENDPOINT
    else:
        base_url = API_LIVE_ENDPOINT

    url_endpoint = base_url + "obj/" + object

    request_func = load_request_function(call_type)

    response = request_func(url_endpoint, json=data, headers=header)

    if response.status_code != 200:
        print(response.text)
        raise Exception("Failed Request!")

    return response


def make_property(cover_image, street_name, city, state, zipcode, agent=None, live=None):
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
    data['agent'] = agent

    return workflow_request(workflow, "POST", data, live)


def create_image(product_id, img, live=None, original_img=None):
    workflow = "new_image"
    data = {}
    data['image'] = {}
    data['original_image'] = {}

    if type(img) is str:
        encoded_image = load_image_file_encoded(img)
    else:
        encoded_image = encode_image(img)
    if original_img:
        if type(img) is str:
            encoded_orig_img = load_image_file_encoded(original_img)
        else:
            encoded_orig_img = encode_image(original_img)

    data['image']['filename'] = 'test.jpg'
    data['image']['contents'] = encoded_image
    data['original_image']['filename'] = 'test.jpg'
    data['original_image']['contents'] = encoded_orig_img
    data['image']['private'] = False
    data['product'] = product_id

    return workflow_request(workflow, "POST", data, live)

def create_product(name, category, sub_cat, property, property_slug, in_stock, live=None, sub_img = None):
    workflow = "new_product"
    data = {}

    data['category'] = category
    data['sub_category'] = sub_cat
    data['property'] = property
    data['property_slug'] = property_slug
    data['in_stock'] = in_stock
    data['name'] = name

    return workflow_request(workflow, "POST", data, live)

def create_agent(name=None, email=None, phone=None, firm=None, property_id=None, live=None):
    workflow = "new_agent"
    data = {}

    data['name'] = name
    data['email'] = email
    data['phone'] = phone
    data['firm'] = firm
    data['property_id'] = property_id

    return workflow_request(workflow, "POST", data, live)


def get_categories(live=None):
    workflow = "category_details"
    data = {}

    return workflow_request(workflow, "POST", data, live)


if __name__ == '__main__':
    img = 'blah.jpg'
    street = '418 Pinehurst Ave'
    city = 'portland'
    state = 'TX'
    zipcode = "78374"
    live = False

    #Create a property
    response = make_property(img, street, city, state, zipcode, live=None)
    property_id = response.json()['response']['id']
    property_slug = response.json()['response']['slug']

    #Create a product without image information
    product_response = create_product("Product name", "Indoor Furniture", "Couch", property_id, property_slug, 12, live=None)
    product_id = product_response.json()['response']['id']

    #Create image with image content and product id
    #Update the product with Image object in same API Workflow
    image_response = create_image(product_id, img, live = None)
    print(image_response)
    print(image_response.text)
