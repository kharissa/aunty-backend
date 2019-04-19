from models.user import User
from flask import Blueprint, jsonify, request
from twilio.rest import Client
from helpers import decode_auth_token
import os

sos_api_blueprint = Blueprint('sos', __name__, template_folder='templates')

@sos_api_blueprint.route('/', methods=['POST'])
def message():
    auth_header = request.headers.get('Authorization')

    decoded = decode_auth_token(token)
    user = User.get(User.id == decoded)

    contacts = PersonalContact.select().where(PersonalContact.user_id == user.id)
    phone_number = contacts.phone_number

    req_data = request.get_json()
    latitude = req_data['latitude']
    longitude = req_data['longitude']
    
    account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
    auth_token = os.environ.get('TWILIO_AUTH_TOKEN')

    client = Client(account_sid, auth_token)

    message = client.messages.create(
        to=phone_number, 
        from_=os.environ.get('TWILIO_PHONE_NUMBER'),
        body=f"Hey, {user.first_name} {user.last_name} is in danger! Aunty very worried! Can you please help? Current latitude: {latitude}, longitude: {longitude}")

    if message.sid:
        return jsonify({
            'status': 'success',
            'id': message.sid
        })
    else: 
        return jsonify({
            'status' : 'failed',
            'message': 'Will return ASAP.'
        })

