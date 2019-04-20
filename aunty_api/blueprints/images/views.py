from app import app
from models.user import User
from models.image import Image
from flask import Blueprint, jsonify, request, redirect, url_for
from helpers import decode_auth_token
from sightengine.client import SightengineClient

images_api_blueprint = Blueprint('images_api', __name__, template_folder='templates')

@images_api_blueprint.route('/', methods=['POST'])
def create():
    auth_header = request.headers.get('Authorization')

    if auth_header:
        token = auth_header.split(" ")[1]
    else:
        return jsonify([{
            'status': 'failed',
            'message': 'Not authorization header.'
        }])

    decoded = decode_auth_token(token)
    user = User.get(User.id == decoded)

    if user:
        ##########################
        # Upload Image to AWS S3 #
        ##########################
        filename = 'kharissa.jpeg' # Dummy data until we receive filename from
        image = Image(filename=filename, user=user)

        if image.save():
            image_url = 'https://d3m9459r9kwism.cloudfront.net/img/examples/example7.jpg'  # image.url
            client = SightengineClient(app.config.get(
                'SIGHTENGINE_USER'), app.config.get('SIGHTENGINE_SECRET'))
            output = client.check('nudity','wad','offensive', 'scam','face-attributes').set_url(image_url)
            image.weapon = output['weapon']
            image.alcohol = output['alcohol']
            image.drugs = output['drugs']
            image.male = output['faces'][0]['attributes']['male']
            image.female = output['faces'][0]['attributes']['female']
            image.minor = output['faces'][0]['attributes']['minor']
            image.sunglasses = output['faces'][0]['attributes']['sunglasses']
            image.scam = output['scam']['prob']
            image.nudity = output['nudity']['safe']

            if image.save():
                return jsonify({
                    'status': 'success',
                    'message': 'Image analyzed successfully.',
                    'results': {
                        'weapon': image.weapon,
                        'alcohol': image.alcohol,
                        'drugs': image.drugs,
                        'male': image.male,
                        'female': image.female,
                        'minor': image.minor,
                        'sunglasses': image.sunglasses,
                        'scam': image.scam,
                        'nudity': image.nudity
                    }
                })
            else:
                return jsonify({
                    'status': 'failed',
                    'message': 'Something went wrong. The image was unable to be analyzed.'
                })
        else:
            return jsonify({
                'status': 'failed',
                'message': 'Image was unsuccessfully uploaded.'
            })
    else:
        return jsonify({
            'status': 'failed',
            'message': 'No user found.'
        })

