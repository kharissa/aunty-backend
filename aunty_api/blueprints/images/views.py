from app import app
from models.user import User
from models.image import Image
from flask import Blueprint, jsonify, request, redirect, url_for
from helpers import decode_auth_token, s3
from sightengine.client import SightengineClient
from helpers import upload_file_to_s3
import base64
import datetime

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
        dataUri = request.get_json()['dataUri']
        decoded_img = base64.b64decode(dataUri)
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        filename = f'{user.id}-{timestamp}.png'
        s3.put_object(Body=dataUri, Bucket="gogaigai", Key=filename)
        image = Image(filename=filename, user=user)

        if image.save():
            image_url = image.url
            client = SightengineClient(app.config.get(
                'SIGHTENGINE_USER'), app.config.get('SIGHTENGINE_SECRET'))
            output = client.check('nudity','wad','offensive', 'scam','face-attributes').set_url(image_url)
            
            if 'weapon' in output:
                image.weapon = output['weapon']
            else:
                image.weapon = '0'
        
            if 'alcohol' in output:
                image.alcohol = output['alcohol']
            else:
                image.alcohol = '0'

            if 'drugs' in output:
                image.drugs = output['drugs']
            else:
                image.drugs = '0'

            if 'male' in output:
                image.male = output['faces'][0]['attributes']['male']
            else:
                image.male = '0'

            if 'female' in output:
                image.female = output['faces'][0]['attributes']['female']
            else:
                image.female = '0'

            if 'minor' in output:
                image.minor = output['faces'][0]['attributes']['minor']
            else:
                image.minor = '0'

            if 'sunglasses' in output:
                image.sunglasses = output['faces'][0]['attributes']['sunglasses']
            else:
                image.sunglasses = '0'

            if 'scam' in output:
                image.scam = output['scam']['prob']
            else:
                image.scam = '0'

            if 'nudity' in output:
                image.nudity = output['nudity']['safe']
            else:
                image.nudity = '0'


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

