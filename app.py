import os
import urllib.request
from flask import Flask, render_template, url_for, request, redirect, session
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from flask_bcrypt import bcrypt
from datetime import datetime

UPLOAD_FOLDER = 'static/upload_img/'

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


app = Flask(__name__)
app.secret_key = "secret key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
db = SQLAlchemy(app)
db.init_app(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

class User(db.Model):
    # __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    date_updated = db.Column(db.DateTime, default=datetime.utcnow)
    image = db.Column(db.String(200), nullable=True)
    image_name = db.Column(db.String(200), nullable=True)
    def __repr__(self):
        return '<User %r>' % self.id

class Content(db.Model):
    # __tablename__ = 'contents'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=True)
    email = db.Column(db.String(200), nullable=True)
    phone = db.Column(db.String(200), nullable=True)
    about = db.Column(db.String(500), nullable=True)
    post = db.Column(db.String(200), nullable=True)
    image = db.Column(db.String(200), nullable=True)
    image_name = db.Column(db.String(200), nullable=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    date_updated = db.Column(db.DateTime, default=datetime.utcnow)
    post_title =   db.Column(db.String(200), nullable=True)
    post_content = db.Column(db.String(500), nullable=True)

    def __repr__(self):
        return '<Content %r>' % self.id

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
            user_name = request.form['name']
            user_email = request.form['email']
            user_password = request.form['password']
            
            find_user = User.query.filter_by(email=user_email).first()
            
            if find_user is None:
                user_password = user_password.encode('utf-8')
                encPassword = bcrypt.hashpw(user_password, bcrypt.gensalt())   
                new_user = User(username = user_name, email=user_email,password=encPassword)
                try:
                    db.session.add(new_user)
                    db.session.commit()
                    return render_template('success.html')
                except:
                    return 'Issue in Adding User'
            else:
                return render_template('login.html')
                # try:
                #     db.session.delete(find_user)
                #     db.session.commit()
                #     return render_template('success.html')
                # except:
                #     return 'Issue in Adding User'
    else :
        return render_template('register.html')


@app.route('/login', methods=['Get','POST'])
def login():
    if request.method == 'POST':
            user_email = request.form['email']
            user_password = request.form['password']
            user_password = user_password.encode('utf-8')
            hashed = bcrypt.hashpw(user_password, bcrypt.gensalt(10)) 
            find_user = User.query.filter_by(email=user_email).first()
            
            if find_user is None:
                return render_template("failure.html")
            elif find_user.email==user_email :
                if bcrypt.checkpw(user_password, hashed):
                # if find_user.password == user_password:
                    users = User.query.order_by(User.date_created).all()
                    # return render_template('compose.html', users=users)
                    return render_template('update.html', users=users)
                else:
                    return render_template("failure.html")
    else:
        return render_template('login.html')

@app.route("/update", methods=["POST","GET"])
def update():
    if request.method == 'POST':
        try:
            name = request.form.get("name")
            email = request.form.get("email")
            phone = request.form.get("phone")
            about = request.form.get("about")
            post = request.form.get("post")
            file_url =''
            if file.filename == '':
                print('No selected file')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                file_url =url_for('static',filename='upload_img/'+filename )
                image_name= filename
            image = file_url
            
            db.session.commit()
        except Exception as e:
            print("Couldn't update Profile")
            print(e)
        return redirect("/")
    else:
        return render_template("failure.html")

@app.route('/contents',methods=['GET'])
def content():
     if request.method == 'GET':
            posts = User.query.join(Content,Content.user_id==User.id).all()
            return render_template('content.html', posts=posts)

@app.route("/logout",methods=['Get','POST'])
def logout():
    if(request.method=='POST'):
        return redirect('/login')


@app.route('/compose', methods=['Get','POST'])
def compose():
    if request.method == 'POST':
        
        userTitle = request.form['postTitle']
        userContent = request.form['postBody']
        new_content = Content(post_title=userTitle,post_content=userContent)
        try:
            db.session.add(new_content)
            db.session.commit()
            return render_template('content.html', posts = posts )
        except:
            return 'Issue in Adding Content'
    else:
        return render_template('compose.html')
        
if __name__ == "__main__":
    app.run(debug=True,port=2000)