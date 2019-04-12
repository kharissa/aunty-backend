import jwt
from models.user import User
from flask import Blueprint, jsonify, request
from werkzeug.security import generate_password_hash
from helpers import encode_auth_token, decode_auth_token

users_api_blueprint = Blueprint('users_api', __name__, template_folder='templates')

@users_api_blueprint.route('/', methods=['POST'])
def index():
    req_data = request.get_json()
    first_name = req_data['firstName']
    last_name = req_data['lastName']
    email = req_data['email']
    date_of_birth = req_data['dateOfBirth']
    nationality = req_data['nationality']
    hashed_password = generate_password_hash(req_data['password'])
    
    u = User(first_name=first_name, last_name=last_name, email=email, password=hashed_password, dob=date_of_birth, nationality=nationality)

    if u.save():
        token = encode_auth_token(u)
        return jsonify({
            'auth_token': token,
            'message': 'Successfully created the account. Please log in.',
            'status': 'success',
            'user': {
                'id': u.id,
                'first_name': u.first_name,
                'last_name': u.last_name,
                'email': u.email
            }
        })
    else:
        errors = u.errors
        return jsonify({
            'status': 'failed',
            'message': errors
        })
