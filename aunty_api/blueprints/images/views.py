from models.user import User
from models.image import Image
from flask import Blueprint, jsonify, request
from helpers import decode_auth_token
from sightengine.client import SightengineClient

images_api_blueprint = Blueprint('images_api', __name__, template_folder='templates')

# @images_api_blueprint.route('/', methods=['POST'])
# def create():
#     pass

@images_api_blueprint.route('/')
def update():
    # image = Image.get(Image.id == image_id)
    client = SightengineClient('112720407', 'SY6rzumjz42j4PG2nKGw')
    output = client.check('nudity','wad','offensive','faces','scam','face-attributes').set_url('https://d3m9459r9kwism.cloudfront.net/img/examples/example7.jpg')
    return output
