from flask import Flask, request, jsonify,make_response
from flask_sqlalchemy import SQLAlchemy
from models import Category,Comment,Content,User,db
from flask_migrate import Migrate


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///moringa.db'  
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
    description = data.get('description')
    category = Category(name=name, description=description)
    db.session.add(category)
    db.session.commit()
    return jsonify({"message": "Category created successfully"})

# Route for viewing categories (accessible to techwriters and users)
@app.route('/view-categories', methods=['GET'])
def view_categories():
    categories = Category.query.all()
    category_list = [{"category_id": category.category_id, "name": category.name, "description": category.description} for category in categories]
    return jsonify(category_list)

# Endpoint to add content and retrieve content
@app.route('/api/content', methods=['GET', 'POST'])
def content():
    if request.method == 'POST':
        
        title = request.json['title']
        description = request.json['description']
        category_id = request.json['category_id']
        user_id = request.json['user_id']
        content_type = request.json['content_type']
        rating = request.json['rating']
        is_flagged = request.json['is_flagged']
        image_thumbnail = request.json['image_thumbnail']
        video_url = request.json['video_url']
        status = request.json['status']

    
        new_content = Content(
            title=title,
            description=description,
            category_id=category_id,
            user_id=user_id,
            content_type=content_type,
            rating=rating,
            is_flagged=is_flagged,
            image_thumbnail=image_thumbnail,
            video_url=video_url,
            status=status
        )

        db.session.add(new_content)
        db.session.commit()

        response = {
            "content_id": new_content.content_id,
            "title": new_content.title,
            "description": new_content.description,
            "category_id": new_content.category_id,
            "user_id": new_content.user_id,
            "content_type": new_content.content_type,
            "rating": new_content.rating,
            "is_flagged": new_content.is_flagged,
            "image_thumbnail": new_content.image_thumbnail,
            "video_url": new_content.video_url,
            "status": new_content.status
        }

        return jsonify(response), 201
    elif request.method == 'GET':
        content_list = Content.query.all()
        content_data = []

        for content in content_list:
            content_data.append({
                "content_id": content.content_id,
                "title": content.title,
                "description": content.description,
                "category_id": content.category_id,
                "user_id": content.user_id,
                "content_type": content.content_type,
                "rating": content.rating,
                "is_flagged": content.is_flagged,
                "image_thumbnail": content.image_thumbnail,
                "video_url": content.video_url,
                "status": content.status
            })

        return jsonify(content_data), 200
    
#End point to update specific content
@app.route('/content/<int:id>', methods=['PUT'])
def update_content(id):
    content = Content.query.get(id)
    if content is None:
        return jsonify({'message': 'Content not found'}), 404

    data = request.get_json()

    content.title = data.get('title', content.title)
    content.description = data.get('description', content.description)
    content.content_type = data.get('content_type', content.content_type)
    content.rating = data.get('rating', content.rating)
    content.is_flagged = data.get('is_flagged', content.is_flagged)
    content.image_thumbnail = data.get('image_thumbnail', content.image_thumbnail)
    content.video_url = data.get('video_url', content.video_url)
    content.status = data.get('status', content.status)

    db.session.commit()

    updated_content = {
        "content_id": content.content_id,
        "title": content.title,
        "description": content.description,
        "category_id": content.category_id,
        "user_id": content.user_id,
        "content_type": content.content_type,
        "rating": content.rating,
        "is_flagged": content.is_flagged,
        "image_thumbnail": content.image_thumbnail,
        "video_url": content.video_url,
        "status": content.status
    }

    return jsonify({'message': 'Content updated successfully', 'content': updated_content})

#End point to delete content by id 
@app.route('/content/<int:id>', methods=['DELETE'])
def delete_content(id):
    content = Content.query.get(id)
    if content is None:
        return jsonify({'message': 'Content not found'}), 404

    db.session.delete(content)
    db.session.commit()

    return jsonify({'message': 'Content deleted successfully'})


#Endpoint to add comment for specific content item
@app.route('/content/<int:content_id>/comments', methods=['GET', 'POST'])
def get_or_create_comments(content_id):
    if request.method == 'GET':
        
        content = Content.query.get(content_id)
        if content is None:
            return jsonify({'message': 'Content not found'}), 404

        comments = Comment.query.filter_by(content_id=content_id).all()
        comment_list = []

        for comment in comments:
            comment_list.append({
                'comment_id': comment.comment_id,
                'text': comment.text,
                'user_id': comment.user_id,  
                
            })

        return jsonify(comment_list)
    
    elif request.method == 'POST':
        
        content = Content.query.get(content_id)
        if content is None:
            return jsonify({'message': 'Content not found'}), 404

        data = request.get_json()

        new_comment = Comment(
            content_id=content_id,
            user_id=data['user_id'],  
            text=data['text']
            
        )

        db.session.add(new_comment)
        db.session.commit()

        return jsonify({'message': 'Comment added successfully'})
    
#Endpoint for deleting a comment 
@app.route('/comments/<int:id>', methods=['DELETE'])
def delete_comment(id):
    comment = Comment.query.get(id)
    if comment is None:
        return jsonify({'message': 'Comment not found'}), 404

    db.session.delete(comment)
    db.session.commit()

    return jsonify({'message': 'Comment deleted successfully'})




# Route for adding an article to the wishlist
@app.route('/add-to-wishlist/<int:content_id>', methods=['POST'])
def add_to_wishlist(content_id):
    user_id = request.json['user_id']  # Get the user ID from the JSON request
    user = User.query.get(user_id)  # Get the current user
    article = Content.query.get(content_id)  # Get the article by content ID
    user.wishlists.append(article)
    db.session.commit()
    return "Article added to wishlist"

# Route for removing an article from the wishlist
@app.route('/remove-from-wishlist/<int:content_id>', methods=['POST'])
def remove_from_wishlist(content_id):
    user_id = request.json['user_id']  # Get the user ID from the JSON request
    user = User.query.get(user_id)  # Get the current user
    article = Content.query.get(content_id)  # Get the article by content ID
    user.wishlists.remove(article)
    db.session.commit()
    return "Article removed from wishlist"

with app.app_context():
        db.create_all()
    

if __name__ == '__main__':
     
     app.run(debug=True)
