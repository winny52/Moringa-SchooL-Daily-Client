from flask import Flask, request, jsonify,make_response,session,render_template
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from models import Category,Comment,Content,User,db,Wishlist,Rating
from flask_migrate import Migrate
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import JWTManager,get_jwt_identity
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///moringa.db'  
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
migrate = Migrate(app, db)

Session(app)
jwt = JWTManager(app) 

db.init_app(app)

def clean():
   user = db.session.execute(db.select(User).filter_by(id=3)).scalar_one()
   db.session.delete(user)
   db.session.commit()

# @app.route('/', methods=['GET'])
# def index():
#     return 'cleaned'

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

    return jsonify({'message': 'Login successful', 'user_id': user.id}), 200
    # Generate a JWT token for the user
    access_token = create_access_token(identity=user.username)

    # Return the token as part of the response
    print(access_token)
    return jsonify({'message': 'Login successful', 'access_token': access_token}), 200
#main api endpointapp.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///moringa.db'  
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
migrate = Migrate(app, db)


db.init_app(app) 

#main api endpoint
@app.route('/', methods=['GET'])
def get_data():
    data = {
        'message': 'Welcome to Moringa Daily',
        
    }
    return jsonify(data)

# Endpoint to get a list of signed-up users as JSON
@app.route('/users', methods=['GET'])
def user_list():
    users = [user.to_dict() for user in User.query.all()]
    return make_response(jsonify(users), 200)

# Admin route for creating a category
@app.route('/admin/create-category', methods=['POST'])
#add decorator
def create_category():
    data = request.get_json()
    name = data.get('name')
    category = Category(name=name)
    db.session.add(category)
    db.session.commit()
    # return jsonify({"message": "Category created successfully"})
    response = {
        'message': 'Category added successfully',
        'category_id': category.category_id
    }
    return jsonify(response), 201








# Route for viewing categories (accessible to techwriters and users)
@app.route('/view-categories', methods=['GET'])
def view_categories():
    categories = Category.query.all()
    category_list = [{"category_id": category.category_id, "name": category.name, "description": category.description} for category in categories]
    return jsonify(category_list)
#content routes for creating
@app.route('/content', methods=['POST'])
def create_content():
    data = request.get_json()
    title = data.get('title')
    description = data.get('description')
    category_id = data.get('category_id')
    user_id = data.get('user_id')
    media_url = data.get('media_url')

    # Create a new content instance
    content = Content(
        title=title,
        description=description,
        category_id=category_id,
        user_id=user_id,
        media_url=media_url
    )

    # Add the content to the database
    db.session.add(content)
    db.session.commit()

    # Return a response
    response = {
        'message': 'Content created successfully',
        'content_id': content.content_id
    }
    return jsonify(response), 201

# Route to get a list of all content
@app.route('/content', methods=['GET'])
def get_all_content():
    # Query the database to get all content items
    content_list = Content.query.all()

    # Serialize the content items to a list of dictionaries
    serialized_content = []
    for content in content_list:
        serialized_content.append({
            'content_id': content.content_id,
            'title': content.title,
            'description': content.description,
            'category_id': content.category_id,
            'user_id': content.user_id,
            'media_url': content.media_url,
            'average_rating': content.average_rating
        })

    return jsonify(serialized_content), 200

# Route to get a specific content item by its ID
@app.route('/content/<int:content_id>', methods=['GET'])
def get_content_by_id(content_id):
    # Query the database to get the content item with the specified ID
    content = Content.query.get(content_id)

    if content is not None:
        serialized_content = {
            'content_id': content.content_id,
            'title': content.title,
            'description': content.description,
            'category_id': content.category_id,
            'user_id': content.user_id,
            'media_url': content.media_url,
            'average_rating': content.average_rating
        }

        return jsonify(serialized_content), 200
    else:
        return jsonify({'message': 'Content not found'}), 404
    

    # Route to update a specific content item by its ID
@app.route('/content/<int:content_id>', methods=['PUT'])
def update_content(content_id):
    # Query the database to get the content item with the specified ID
    content = Content.query.get(content_id)

    if content is not None:
        # Parse the JSON data from the request
        data = request.get_json()

        # Update the content properties with the new values from the request
        if 'title' in data:
            content.title = data['title']
        if 'description' in data:
            content.description = data['description']
        if 'category_id' in data:
            content.category_id = data['category_id']
        if 'user_id' in data:
            content.user_id = data['user_id']
        if 'media_url' in data:
            content.media_url = data['media_url']

        # Commit the changes to the database
        db.session.commit()

        return jsonify({'message': 'Content updated successfully'}), 200
    else:
        return jsonify({'message': 'Content not found'}), 404
    
    # Route to delete a specific content item by its ID
@app.route('/content/<int:content_id>', methods=['DELETE'])
def delete_content(content_id):
    # Query the database to get the content item with the specified ID
    content = Content.query.get(content_id)

    if content is not None:
        # Remove the content from the database
        db.session.delete(content)
        db.session.commit()

        return jsonify({'message': 'Content deleted successfully'}), 200
    else:
        return jsonify({'message': 'Content not found'}), 404
    

    # Route to create a rating for a content
@app.route('/ratings', methods=['POST'])
def create_rating():
    # Parse the user's rating data from the request
    data = request.get_json()
    content_id = data.get('content_id')
    rating_value = data.get('rating')

    # Create a new Rating instance
    rating = Rating(
        content_id=content_id,
        rating=rating_value
    )

    # Add the rating to the database
    db.session.add(rating)
    db.session.commit()

    # Return a success message
    return jsonify({'message': 'Rating created successfully'}), 201



# Route to get a content's average rating by its content_id
@app.route('/content/<int:content_id>/average-rating', methods=['GET'])
def get_content_average_rating(content_id):
    # Query the database to get the content with the specified content_id
    content = Content.query.get(content_id)

    if content is not None:
        # Query the related Rating objects for the content
        ratings = Rating.query.filter_by(content_id=content_id).all()

        if ratings:
            # Calculate the average rating
            total_ratings = sum(rating.rating for rating in ratings)
            average_rating = total_ratings / len(ratings)

            # Format the average rating to one decimal place
            formatted_average_rating = round(average_rating, 1)

            # Serialize the formatted average rating
            serialized_average_rating = {
                'content_id': content.content_id,
                'average_rating': formatted_average_rating
            }

            return jsonify(serialized_average_rating), 200
        else:
            return jsonify({'message': 'No ratings found for this content'}), 200

    else:
        return jsonify({'message': 'Content not found'}), 404
    

#Endpoint to approve content
@app.route('/content/approve/<int:id>', methods=['POST'])
# @jwt_required
def approve_content(id):
    # Get the current user's identity from the JWT token
    current_user = get_jwt_identity()

    # Check if the current user is an admin
    user = User.query.filter_by(username=current_user).first()
    if user is None or user.role != 'admin':
        return jsonify({'error': 'Only admin users can approve content'}), 403

    content = Content.query.get(id)
    if content is None:
        return jsonify({'message': 'Content not found'}), 404

    # Update the content's "status" attribute to "approved"
    content.status = 'approved'
    db.session.commit()

    return jsonify({'message': 'Content approved successfully'}), 200

#Endpoint to delete flagged content

@app.route('/content/delete-approved/<int:id>', methods=['POST'])
# @jwt_required
def delete_flagged_content(id):
    # Get the current user's identity from the JWT token
    current_user = get_jwt_identity()

    # Check if the current user is an admin
    user = User.query.filter_by(username=current_user).first()
    if user is None or user.role != 'admin':
        return jsonify({'error': 'Only admin users can delete content'}), 403

    content = Content.query.get(id)
    if content is None:
        return jsonify({'message': 'Content not found'}), 404

    # Update the content's "status" attribute to "deleted"
    content.status = 'deleted'
    db.session.commit()

    return jsonify({'message': 'Content deleted successfully'}), 200


    # Route to create a comment for a content
@app.route('/comments', methods=['POST'])
def create_comment():
    # Parse the user's comment data from the request
    data = request.get_json()
    content_id = data.get('content_id')
    user_id = data.get('user_id')
    text = data.get('text')

    # Create a new Comment instance
    comment = Comment(
        content_id=content_id,
        user_id=user_id,
        text=text
    )

    # Add the comment to the database
    db.session.add(comment)
    db.session.commit()

    # Return a success message
    return jsonify({'message': 'Comment created successfully'}), 201


# Route to get comments for a specific content by its content_id
@app.route('/comments/<int:content_id>', methods=['GET'])
def get_comments(content_id):
    # Query the database to retrieve comments for the specified content
    comments = Comment.query.filter_by(content_id=content_id).all()

    # Serialize the comments
    serialized_comments = []
    for comment in comments:
        serialized_comment = {
            'comment_id': comment.comment_id,
            'user_id': comment.user_id,
            'text': comment.text
        }
        serialized_comments.append(serialized_comment)

    return jsonify(serialized_comments), 200


# Route to update a comment by its comment_id
@app.route('/comments/<int:comment_id>', methods=['PUT'])
def update_comment(comment_id):
    # Parse the updated comment data from the request
    data = request.get_json()
    new_text = data.get('text')

    # Query the database to retrieve the comment with the specified comment_id
    comment = Comment.query.get(comment_id)

    if comment is not None:
        # Update the comment's text with the new text
        comment.text = new_text

        # Commit the changes to the database
        db.session.commit()

        # Return a success message
        return jsonify({'message': 'Comment updated successfully'}), 200
    else:
        return jsonify({'message': 'Comment not found'}), 404
    

    # Route to delete a comment by its comment_id
@app.route('/comments/<int:comment_id>', methods=['DELETE'])
def delete_comment(comment_id):
    # Query the database to retrieve the comment with the specified comment_id
    comment = Comment.query.get(comment_id)

    if comment is not None:
        # Delete the comment from the database
        db.session.delete(comment)
        db.session.commit()

        # Return a success message
        return jsonify({'message': 'Comment deleted successfully'}), 200
    else:
        return jsonify({'message': 'Comment not found'}), 404

#Endpoint to add and delete conten from wishlist
@app.route('/add-to-wishlist/<int:content_id>', methods=['POST'])
def add_to_wishlist(content_id):
    user_id = request.json['user_id']  # Get the user ID from the JSON request
    user = User.query.get(user_id)  # Get the current user
    content = Content.query.get(content_id)  # Get the content by content ID
    
    # Create a Wishlist object and associate it with the user and content
    wishlist_item = Wishlist(user_id=user_id, content_id=content_id)
    db.session.add(wishlist_item)
    db.session.commit()
    return "Content added to wishlist"
@app.route('/remove-from-wishlist', methods=['DELETE'])
def remove_from_wishlist():
    user_id = request.json['user_id']
    content_id = request.json['content_id']
    user = User.query.get(user_id)
    content = Content.query.get(content_id)
    user.wishlists.remove(content)
    db.session.commit()
    return "Content removed from wishlist"

@app.route('/subscribe-to-category', methods=['POST'])
def subscribe_to_category():
    user_id = request.json['user_id']
    category_id = request.json['category_id']
    user = User.query.get(user_id)
    category = Category.query.get(category_id)
    user.subscriptions.append(category)
    db.session.commit()
    return "Subscribed to category"

with app.app_context():
        db.create_all()
    

if __name__ == '__main__':
     
     app.run(debug=True)
