from app import app
import os
from models.user import User
from models.image import Image
from flask import Blueprint, jsonify, request, redirect, url_for
from helpers import decode_auth_token
from sightengine.client import SightengineClient
from helpers import upload_file_to_s3
import base64
import datetime
import boto3
import botocore
from config import S3_KEY, S3_SECRET, S3_BUCKET

s3 = boto3.client(
    "s3",
    aws_access_key_id=S3_KEY,
    aws_secret_access_key=S3_SECRET
)

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
        # Retrieving image in data uri scheme
        dataUri = request.get_json()['dataUri']
        
        # Decoding into an image
        decoded_img = base64.b64decode(dataUri.split(",")[1])

        # Saving filename as user id and current datetime string
        current_time = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        filename = f'{user.id}{current_time}.jpg'

        # Uploading image to AWS
        s3.put_object(
            Body=decoded_img, Bucket=app.config["S3_BUCKET"], Key=filename, ACL='public-read')

        # Creating an image pw instance
        image = Image(filename=filename, user=user)

        if image.save():

            # If image saves in DB, send to SightEngine API
            client = SightengineClient(os.environ.get(
                'SIGHTENGINE_USER'), os.environ.get('SIGHTENGINE_SECRET'))
            output = client.check('nudity','wad','offensive', 'scam','face-attributes').set_url(image.url)
            print(output)
            # Updating image with returned output from SightEngine
            image.weapon = output['weapon']
            image.alcohol = output['alcohol']
            image.drugs = output['drugs']
            image.scam = output['scam']['prob']
            image.nudity = output['nudity']['raw']
            
            if output['faces']:
                image.male = output['faces'][0]['attributes']['male']
                image.female = output['faces'][0]['attributes']['female']
                image.minor = output['faces'][0]['attributes']['minor']
                image.sunglasses = output['faces'][0]['attributes']['sunglasses']

            if image.save() and output['status'] == 'success':
                return jsonify({
                    'status': 'success',
                    'message': 'Image analyzed successfully.',
                    'imageId': image.id,
                    'results': {
                        'weapon': image.weapon,
                        'alcohol': image.alcohol,
                        'drugs': image.drugs,
                        'male': image.male or 0,
                        'female': image.female or 0,
                        'minor': image.minor or 0,
                        'sunglasses': image.sunglasses or 0,
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


@images_api_blueprint.route('/<image_id>', methods=['GET'])
def show(image_id):
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
    query = Image.select().where(Image.id == image_id, Image.user_id == user.id)

    if user and query.exists():
        image = Image.get(Image.id == image_id)
        return jsonify({
            'status': 'success',
            'message': 'Image retrieved successfully.',
            'imageId': image.id,
            'imageURL': image.url,
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
            'message': 'Unable to retrieve this image for this user.'
        })
