# app.py

from flask import Flask
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from models import db
from routes import auth_bp
from config import Config
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object(Config)

# front_end_url = "http://localhost:5173"
CORS(app, origins='https://online-professional-cleaner-app.vercel.app', methods=['GET', 'POST','OPTIONS'], allow_headers=['Content-Type', 'Authorization'])

# Initialize extensions
db.init_app(app)
jwt = JWTManager(app)
migrate = Migrate(app, db)

# Register blueprints
app.register_blueprint(auth_bp)

# Create tables
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
