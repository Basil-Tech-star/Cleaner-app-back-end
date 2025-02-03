# models.py

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Cleaner(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(15), nullable=False, unique=True)
    cleaning_service = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Float, nullable=True)

class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(15), nullable=False, unique=True)
    location = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)  # Hashed password
    bookings = db.relationship('Booking', backref='client', lazy=True)

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cleaner_id = db.Column(db.Integer, db.ForeignKey('cleaner.id'), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='Pending')
