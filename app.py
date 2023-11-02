from flask import Flask, render_template, request, jsonify, session, make_response
from flask_session import Session
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity, create_access_token

from models import User, Category, db

app = Flask(__name__)

app.config['SESSION_TYPE'] = 'filesystem'  
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True
app.config['JWT_SECRET_KEY'] = 'moringaschool'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///moringa2.sqlite3'  

migrate = Migrate(app, db, render_as_batch=True)

Session(app)
jwt = JWTManager(app) 

db.init_app(app)

#deletes useless rows in db by changing the id of the thing I want to delete.
def clean():
   user = db.session.execute(db.select(User).filter_by(id=3)).scalar_one()
   db.session.delete(user)
   db.session.commit()

@app.route('/', methods=['GET'])
def get_data():
    data = {
        'message': 'Welcome to Moringa Daily',
        
    }

    return jsonify(data)

@app.route('/users', methods=['GET'])
def user_list():
    users = [user.to_dict() for user in User.query.all()]
    print(users)
    return make_response(jsonify(users), 200)



@app.route('/view-categories', methods=['GET'])
def view_categories():
    categories = Category.query.all()
    category_list = [{"category_id": category.category_id, "name": category.name, "description": category.description} for category in categories]
    return jsonify(category_list)

@app.route("/signup", methods=["POST"])
def signup():
    data = request.json  # Assumes you are sending JSON data in the request body

    username = data.get('username')
    password = data.get('password')
    role = data.get('role')

    if not username or not password or not role:
        return make_response(({'error': 'Username, password, and role are required'}), 400)

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


@app.route("/login", methods=["POST"])
def login():
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
    if not check_password_hash(user.password, password):
        return jsonify({'error': 'Invalid username or password'}), 401

    # Generate a JWT token for the user
    access_token = create_access_token(identity=user.username)

    # Return the token as part of the response
    return jsonify(access_token=access_token), 200

@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    print('current_user')
    return jsonify(logged_in_as=current_user), 200

if __name__ == '__main__':
    app.run(debug=True)
