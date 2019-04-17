from models.personal_contact import PersonalContact
from models.user import User
from flask import Blueprint, jsonify, request
from werkzeug.security import check_password_hash
from helpers import encode_auth_token, decode_auth_token

contacts_api_blueprint = Blueprint(
    'contacts_api', __name__, template_folder='templates')

@contacts_api_blueprint.route('/', methods=['GET', 'POST'])
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

        if request.method == "GET":
            contacts = PersonalContact.select().where(PersonalContact.user_id == user.id)
            return jsonify({
                'personalContacts':
                    [{'id': contact.id,
                      'name': contact.name,
                      'relationship': contact.relationship,
                      'location': contact.location,
                      'priority': contact.priority,
                      'phone_number': contact.phone_number,
                      'email': contact.email} for contact in contacts]})

        elif request.method == "POST":
            req_data = request.get_json()
            req_data['name']
            req_data['email']
            req_data['location']
            req_data['relationship']
            contact = PersonalContact(name=req_data['name'], email=req_data['email'], relationship=req_data['relationship'], location=req_data['location'], user=user)
            
            if contact.save():
                return jsonify([{
                    'status': 'success',
                    'message': 'Successfully created a contact.',
                    'contact': {
                        'id': contact.id,
                        'name': contact.name,
                        'location': contact.location,
                        'email': contact.email,
                        'relationship': contact.relationship
                    }
                }])
            else:
                return jsonify([{
                    'status': 'failed',
                    'message': 'Unable to save contact.'
                }])
    else:
        return jsonify([{
            'status': 'failed',
            'message': 'Authentication failed.'
        }])

@contacts_api_blueprint.route('/<contact_id>', methods=['PUT'])
def update(contact_id):
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
        contact = PersonalContact.get(PersonalContact.id == contact_id, PersonalContact.user_id == user.id)

        req_data = request.get_json()
        contact.name = req_data['name'] or contact.name
        contact.relationship = req_data['relationship'] or contact.relationship
        contact.location = req_data['location'] or contact.location
        contact.priority = req_data['priority'] or contact.priority
        contact.email = req_data['email'] or contact.email
        contact.phone_number = req_data['phoneNumber'] or contact.phone_number

        if contact.save():
            return jsonify([{
                'status': 'success',
                'message': 'Successfully updated the contact details.'
            }])
        else:
            return jsonify([{
                'status': 'failed',
                'message': 'Unable to update contact.'
            }])
    else:
        return jsonify([{
            'status': 'failed',
            'message': 'Authentication failed.'
        }])
