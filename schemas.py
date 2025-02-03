# schemas.py

from marshmallow import Schema, fields

class CleanerSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()
    phone_number = fields.Str()
    cleaning_service = fields.Str()
    location = fields.Str()
    rating = fields.Float()

class ClientSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()
    phone_number = fields.Str()
    location = fields.Str()

class BookingSchema(Schema):
    id = fields.Int(dump_only=True)
    cleaner_id = fields.Int()
    client_id = fields.Int()
    status = fields.Str()
