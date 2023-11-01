# Import necessary libraries and modules
from flask import Flask, render_template
from flask.sessions import Session
from flask import request, jsonify
from flask_restful import Resource
from models import User
from werkzeug.security import check_password_hash,generate_password_hash
from flask_jwt_extended import JWTManager


# Create a Flask application
app = Flask(__name__)


# Initialize Flask-RESTful
api = Api(app)


# Configure Flask-Session
app.config['SESSION_TYPE'] = 'filesystem'  # You can choose other options
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True

# Initialize Flask-Session
Session(app)

# Configure Flask-JWT-Extended
app.config['JWT_SECRET_KEY'] = 'your_secret_key'
jwt = JWTManager(app) 

# Initialize SQLAlchemy (assuming you are using SQLAlchemy for the database)
app.config['SQLALCHEMY_DATABASE_URI'] = 'your_database_uri'  # Replace with your actual database URI
db = SQLAlchemy(app)
db.init_app(app)

# Define routes and views
class Signup(Resource):
    def post(self):
        data = request.json  # Assumes you are sending JSON data in the request body

        username = data.get('username')
        password = data.get('password')
        role = data.get('role')

        if not username or not password or not role:
            return jsonify({'error': 'Username, password, and role are required'}), 400

        # Check if the specified role is valid (admin, user, or writer)
        if role not in ['admin', 'user', 'writer']:
            return jsonify({'error': 'Invalid role specified'}), 400
        
         # Hash the password before storing it
        hashed_password = generate_password_hash(password)

        # Store the hashed password in the database
        user = User(username=username, password_hash=hashed_password, role=role)
        db.session.add(user)
        db.session.commit()

        return jsonify({'message': 'User registered successfully'}), 201


class Login(Resource):
     def post(self):
        data = request.json  # Assumes you are sending JSON data in the request body

        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({'error': 'Username and password are required'}), 400

        # Find the user by username in the database
        user = User.query.filter_by(username=username).first()

        if not user:
            return jsonify({'error': 'Invalid username or password'}), 401

        # Check if the provided password matches the stored password hash
        if not check_password_hash(user.password_hash, password):
            return jsonify({'error': 'Invalid username or password'}), 401

        return jsonify({'message': 'Login successful', 'user_id': user.user_id}), 200
        # Generate a JWT token for the user
        access_token = create_access_token(identity=user.user_id)

        # Return the token as part of the response
        return jsonify({'message': 'Login successful', 'access_token': access_token}), 200

# Add routes 
api.add_resource(Signup, '/signup')
api.add_resource(Login, '/login')



if __name__ == '__main__':
    app.run(debug=True)
