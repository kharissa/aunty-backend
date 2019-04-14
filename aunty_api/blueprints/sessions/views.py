from models.user import User
from flask import Blueprint, jsonify, request
from werkzeug.security import check_password_hash
from helpers import encode_auth_token, decode_auth_token

sessions_api_blueprint = Blueprint('sessions_api', __name__, template_folder='templates')

@sessions_api_blueprint.route('/', methods=['POST'])
def create():
    req_data = request.get_json()
    email = req_data['email']
    user = User.get(User.email == email)
    
    if user:
        password_to_check = req_data['password']
        hashed_password = user.password
        result = check_password_hash(hashed_password, password_to_check)
        if result:
            token = encode_auth_token(user)
            return jsonify({
                'auth_token': token,
                'message': 'Successfully signed in.',
                'status': 'success',
                'user': {
                    'id': user.id,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'email': user.email
                }})
        else:
            return jsonify({
                'status': 'failed',
                'message': 'Password do not match.'
            })
