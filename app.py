from flask import Flask, render_template, request, jsonify, session, make_response
from flask_session import Session
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import JWTManager

from models import User, db

app = Flask(__name__)
api = Api(app)

# Configure Flask-Session
app.config['SESSION_TYPE'] = 'filesystem'  
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True
app.config['JWT_SECRET_KEY'] = 'moringaschool'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///moringa.sqlite3'  

migrate = Migrate(app, db)

Session(app)
jwt = JWTManager(app) 

db.init_app(app)

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
        user = User(username=username, password=hashed_password, role=role)

        db.session.add(user)
        db.session.commit()

        return make_response(jsonify({'message': 'User registered successfully'}), 201)


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

api.add_resource(Signup, '/signup')
api.add_resource(Login, '/login')

if __name__ == '__main__':
    app.run(debug=True)
