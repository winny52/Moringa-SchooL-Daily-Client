#!/usr/bin/env python

from flask import Flask, jsonify, request,make_response, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from models import db, Users

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///earth.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

def seed():
    User1 = Users(
        username = 'testone', 
        password = 'admin',
    )

    db.session.add(User1)
    db.session.commit()

@app.route('/')
def index():
    return 'this is index' 

@app.route('/success/<name>')
def success(name):
   return 'welcome %s' % name

@app.route('/fail')
def fail():
   return 'wrong password and username'




@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return 'register now'

    elif request.method == 'POST':
        newUser = Users(
                username=request.form.get("username"), 
                password=request.form.get("password"), 
        )

    db.session.add(newUser)        
    db.session.commit()
    
    return "202"


@app.route('/login',methods = ['POST', 'GET'])
def login():
   if request.method == 'POST':
      user = request.form['username']
      user_pass = request.form['password']

      db_user = db.session.execute(db.select(Users).filter_by(id=user)).scalar_one()

      if(db_user.password == user_pass):
        return redirect(url_for('success', name=db_user.username))
      
      else:
          return redirect(url_for('fail'))

   else:
      return "This is login page" 
if __name__ == '__main__':
    app.run(port=5555, debug=True)
