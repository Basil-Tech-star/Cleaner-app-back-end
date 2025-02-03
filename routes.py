# routes.py

from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models import db, Cleaner, Client, Booking
from schemas import CleanerSchema , ClientSchema, BookingSchema
import bcrypt

auth_bp = Blueprint('auth', __name__)

# Route for user registration
@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    name = data['name']
    phone_number = data['phone_number']
    location = data['location']
    password = data['password']

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    new_client = Client(name=name, phone_number=phone_number, location=location, password=hashed_password)
    db.session.add(new_client)
    db.session.commit()

    return jsonify({"message": "Client registered successfully!"}), 201

# Route for user login
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    phone_number = data['phone_number']
    password = data['password']

    client = Client.query.filter_by(phone_number=phone_number).first()

    if not client or not bcrypt.checkpw(password.encode('utf-8'), client.password ):#.encode('utf-8')):
        return jsonify({"message": "Invalid credentials"}), 401

    access_token = create_access_token(identity=str(client.id))

    return jsonify({"access_token": access_token})

# Route for adding a cleaner (for admin, can be modified)
@auth_bp.route('/cleaner', methods=['POST'])
@jwt_required()
def add_cleaner():
    current_user_id = get_jwt_identity()
    data = request.get_json()

    name = data['name']
    phone_number = data['phone_number']
    cleaning_service = data['cleaning_service']
    location = data['location']

    new_cleaner = Cleaner(name=name, phone_number=phone_number, cleaning_service=cleaning_service, location=location)
    db.session.add(new_cleaner)
    db.session.commit()

    return jsonify({"message": "Cleaner added successfully!"}), 201

# Route to book a cleaner
@auth_bp.route('/book', methods=['POST'])
@jwt_required()
def book_cleaner():
    current_user_id = get_jwt_identity()
    data = request.get_json()

    cleaner_id = data['cleaner_id']
    status = 'Pending'

    new_booking = Booking(client_id=current_user_id, cleaner_id=cleaner_id, status=status)
    db.session.add(new_booking)
    db.session.commit()

    return jsonify({"message": "Cleaner booked successfully!"}), 201

# Route to view all cleaners
@auth_bp.route('/cleaners', methods=['GET'])
def get_cleaners():
    cleaners = Cleaner.query.all()
    cleaner_schema = CleanerSchema(many=True)
    return jsonify(cleaner_schema.dump(cleaners))
