import jwt
from models.user import User
from models.personal_contact import PersonalContact
from flask import Blueprint, jsonify, request
from werkzeug.security import generate_password_hash
from helpers import encode_auth_token, decode_auth_token

users_api_blueprint = Blueprint('users_api', __name__, template_folder='templates')

@users_api_blueprint.route('/', methods=['POST'])
def create():
    req_data = request.get_json()
    first_name = req_data['firstName']
    last_name = req_data['lastName']
    email = req_data['email']
    date_of_birth = req_data['dateOfBirth']
    nationality = req_data['nationality']
    hashed_password = generate_password_hash(req_data['password'])
    
    user = User(first_name=first_name, last_name=last_name, email=email, password=hashed_password, dob=date_of_birth, nationality=nationality)

    if user.save():
        token = encode_auth_token(user)
        return jsonify({
            'auth_token': token,
            'message': 'Successfully created the account. Please log in.',
            'status': 'success',
            'user': {
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email
            }
        })
    else:
        errors = user.errors
        return jsonify({
            'status': 'failed',
            'message': errors
        })


@users_api_blueprint.route('/<user_id>/', methods=['GET'])
def show(user_id):
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
        contacts = PersonalContact.select().where(PersonalContact.user_id == user.id)
        return jsonify({
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'dob': user.dob,
            'passport_num': user.passport_num,
            'nationality': user.nationality,
            'language_primary': user.language_primary,
            'language_secondary': user.language_secondary,
            'verified': user.verified,
            'personalContacts':
                [{'id': contact.id,
                  'name': contact.name,
                  'relationship': contact.relationship,
                  'location': contact.location,
                  'priority': contact.priority,
                  'phone_number': contact.phone_number,
                  'email': contact.email} for contact in contacts]}
        )
    else:
        return jsonify([{
            'status': 'failed',
            'message': 'Authentication failed.'
        }])
