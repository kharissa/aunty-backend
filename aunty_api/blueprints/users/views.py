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


@users_api_blueprint.route('/me/', methods=['GET', 'PUT'])
def show_current_user():
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
        if request.method == "GET":
            return jsonify({
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'dob': user.dob,
                'passport_num': user.passport_num,
                'nationality': user.nationality,
                'language_primary': user.language_primary,
                'language_secondary': user.language_secondary,
                'verified': user.verified})
        elif request.method == "PUT":
            req_data = request.get_json()
            user.first_name = req_data['firstName'] or user.first_name
            user.last_name = req_data['lastName'] or user.last_name
            user.email = req_data['email'] or user.email
            user.nationality = req_data['nationality'] or user.nationality
            user.passport_num = req_data['passportNum'] or user.passport_num
            user.language_primary = req_data['languagePrimary'] or user.language_primary
            user.language_secondary = req_data['languageSecondary'] or user.language_secondary
            if req_data['password']:
                user.password = generate_password_hash(req_data['password'])
            if user.save():
                return jsonify([{
                    'status': 'success',
                    'message': 'Successfully updated the user details.'
                }])
            else:
                return jsonify([{
                    'status': 'failed',
                    'message': 'Unable to update user.'
                }])
    else:
        return jsonify([{
            'status': 'failed',
            'message': 'Authentication failed.'
        }])
