from models.user import User
from models.itinerary_pin import ItineraryPin
from models.map_pin import MapPin
from flask import Blueprint, jsonify, request
from werkzeug.security import generate_password_hash
from helpers import encode_auth_token, decode_auth_token

pins_api_blueprint = Blueprint('pins_api', __name__, template_folder='templates')

@pins_api_blueprint.route('/map/', methods=['GET', 'POST'])
def create_map_pin():
    if request.method == "POST":
        req_data = request.get_json()
        pin_name = req_data['pinName']
        user_id = req_data['userId']
        longitude = req_data['longitude']
        latitude = req_data['latitude']
        is_safe = req_data['isSafe']
        category = req_data['category']
        radius = req_data['radius']
        source = req_data['source']
        is_public = req_data['isPublic']
        user = User.get(User.id == user_id)

        if user:
            map_pin = MapPin(user=user, name=pin_name, longitude=longitude, latitude=latitude, is_safe=is_safe, category=category, radius=radius, is_public=is_public, source=source)

            if map_pin.save():
                return jsonify({
                    'message': 'Successfully created the map pin.',
                    'status': 'success',
                    'pin': {
                        'id': map_pin.id,
                        'user_id': map_pin.user_id,
                        'longitude': map_pin.longitude,
                        'latitude': map_pin.latitude,
                        'name': map_pin.name,
                        'category': map_pin.category,
                        'is_public': map_pin.is_public,
                        'is_safe': map_pin.is_safe
                    }
                })
            else:
                errors = map_pin.errors
                return jsonify({
                    'status': 'failed',
                    'message': errors
                })
        else:
            return jsonify([{
                'status': 'failed',
                'message': 'User cannot be found.'
            }])
    elif request.method == "GET":
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
            public_pins = MapPin.select().where(MapPin.is_public == True)
            private_pins = MapPin.select().where(
                MapPin.user_id == user.id, MapPin.is_public == False)

            return jsonify({'publicPins':
                [{'id': public_pin.id,
                'longitude': str(public_pin.longitude),
                'latitude': str(public_pin.latitude),
                'is_safe': public_pin.is_safe,
                'category': public_pin.category,
                'name': public_pin.name,
                'radius': public_pin.radius} for public_pin in public_pins],
                'privatePins':
                [{'id': private_pin.id,
                  'longitude': str(private_pin.longitude),
                  'latitude': str(private_pin.latitude),
                  'is_safe': private_pin.is_safe,
                  'category': private_pin.category,
                  'name': private_pin.name,
                  'radius': private_pin.radius} for private_pin in private_pins]}
            )
        else:
            return jsonify([{
                'status': 'failed',
                'message': 'Authentication failed.'
            }])


@pins_api_blueprint.route('/itinerary/', methods=['GET', 'POST'])
def create_itinerary_pin():
    if request.method == "POST":
        req_data = request.get_json()
        pin_name = req_data['pinName']
        user_id = req_data['userId']
        longitude = req_data['longitude']
        latitude = req_data['latitude']
        start_time = req_data['startTime']
        address = req_data['address']
        user = User.get(User.id == user_id)

        if user:
            itinerary_pin = ItineraryPin(
                user=user, name=pin_name, longitude=longitude, latitude=latitude, start_time=start_time, address=address)

            if itinerary_pin.save():
                return jsonify({
                    'message': 'Successfully created the map pin.',
                    'status': 'success',
                    'pin': {
                        'id': itinerary_pin.id,
                        'userId': itinerary_pin.user_id,
                        'longitude': str(itinerary_pin.longitude),
                        'latitude': str(itinerary_pin.latitude),
                        'start_time': itinerary_pin.start_time,
                        'pinName': itinerary_pin.name,
                        'address': itinerary_pin.address
                    }
                })
            else:
                errors = itinerary_pin.errors
                return jsonify({
                    'status': 'failed',
                    'message': errors
                })
        else:
            return jsonify([{
                'status': 'failed',
                'message': 'User cannot be found.'
            }])
    elif request.method == "GET":
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
            pins = ItineraryPin.select().where(
                ItineraryPin.user_id == user.id, ItineraryPin.resolved == False)
            return jsonify(
                [{'id': pin.id,
                  'userId': pin.user_id,
                  'longitude': str(pin.longitude),
                  'latitude': str(pin.latitude),
                  'start_time': pin.start_time,
                  'address': pin.address,
                  'pinName': pin.name} for pin in pins],
            )
        else:
            return jsonify([{
                'status': 'failed',
                'message': 'Authentication failed.'
            }])

@pins_api_blueprint.route('/itinerary/delete/', methods=['POST'])
def delete_itinerary_pin():
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

    req_data = request.get_json()
    pin_id = req_data['pinId']

    
    pin = ItineraryPin.delete().where(ItineraryPin.id == pin_id)
    
    if pin.execute():
        return jsonify([{
        'status': 'success',
        'message': 'Successfully delete itinerary pin.'
    }])
    else:
        return jsonify([{
            'status': 'failed',
            'message': 'Unable to delete itinerary pin.'
    }])




