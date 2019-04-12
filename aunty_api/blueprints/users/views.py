from flask import Blueprint, jsonify, request
from werkzeug.security import generate_password_hash
from models.user import User
from flask_login import LoginManager, login_required, current_user, login_user

users_api_blueprint = Blueprint('users_api',
                             __name__,
                             template_folder='templates')

@users_api_blueprint.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        req_data = request.get_json()
        first_name = req_data['firstName']
        last_name = req_data['lastName']
        email = req_data['email']
        password = req_data['password']
        date_of_birth = req_data['dateOfBirth']
        nationality = req_data['nationality']
        hashed_password = generate_password_hash(password)
        
        u = User(first_name=first_name, last_name=last_name, email=email, password=hashed_password, date_of_birth=date_of_birth, nationality=nationality)

        if u.save():
            return jsonify({
                'auth_token': 'DUMMY_TOKEN',
                'message': 'Successfully created a user and signed in.',
                'status': 'success',
                'user': {
                    'id': 'DUMMY_USER_ID',
                    'first_name': first_name,
                    'last_name': last_name,
                    'email': email,
                    'date_of_birth': date_of_birth,
                    'nationality': nationality
                }
            })
        else:
            errors = u.errors
            return jsonify({
                'status': 'failed',
                'message': errors
            })
    else:
        return jsonify({
            'status': 'failed',
            'message': 'Try a POST request!'
        })
