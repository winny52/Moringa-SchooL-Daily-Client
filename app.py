from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from models import User

app = Flask(__name__)

# Configure SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///moringa.db'
db = SQLAlchemy(app)  # Initialize SQLAlchemy with your app


@app.route('/register', methods=['POST'])
def register_user():
    # Get user registration data from the request
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    role = data.get('role')  # Include role field in registration data

    # Check if the username or email already exists in the database
    existing_user = User.query.filter((User.username == username) | (User.email == email)).first()

    if existing_user:
        return jsonify({'message': 'Username or email already exists'}), 400

    # Check if the specified role is valid (Admin, Tech Writer, or Reader)
    valid_roles = ['Admin', 'Tech Writer', 'Reader']
    if role not in valid_roles:
        return jsonify({'message': 'Invalid user role'}), 400

    # Create a new User instance and add it to the database
    new_user = User(username=username, email=email, password=password, role=role)

    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User registered successfully'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error registering user'}), 500
    finally:
        db.session.close()

if __name__ == '__main__':
    app.run(debug=True)


@app.route('/', methods=['GET'])
def get_data():
    data = {
        'message': 'Welcome to Moringa Daily',
        
    }
    return jsonify(data)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create the database tables if they don't exist
    app.run(debug=True)

