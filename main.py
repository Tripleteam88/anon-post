from flask import Flask, render_template, url_for, request, session, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
import os
import hashlib
from datetime import datetime as dt


app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.permanent_session_lifetime = timedelta(days=1)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

def toHash(value:str):
    hash_obj = hashlib.sha256(bytes(value, 'utf8'))
    return hash_obj.hexdigest()

class User(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    username = db.Column(db.String(64))
    password = db.Column(db.String(64))
    def __init__(self, username, password):
        self.username = username
        self.password = toHash(password)

class Post(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    title = db.Column(db.String(10000))
    author = db.Column(db.String(64))
    content = db.Column(db.String(10000))
    datePosted = db.Column(db.String(100))
    def __init__(self, title:str, author:str, content:str):
        self.title = title
        self.author = author
        self.content = content
        self.datePosted = str(dt.now().strftime('%b. %e %Y %r'))

@app.route('/index.html')
@app.route('/')
def index():
    posts = Post.query.all()
    posts.reverse()
    return render_template("index.html", title="Home", session=session, posts=posts)

@app.route('/user', methods=['GET'])
def user():
    if "user" in session:
        user = session["user"]
    return render_template("user.html", title="Profile", user=user)

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'GET':
        if "user" not in session:
            return redirect(url_for('login'))
        return render_template('create.html')
    else:
        postauthor = None
        try:
            postauthor = str(request.form['author'])
        except KeyError:
            postauthor = session['user']
        post = Post(str(request.form['title']), postauthor, str(request.form['content']))
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    success = None
    if request.method == 'GET':
        pass
    elif request.method == 'POST':
        success = False
        findUser = User.query.filter_by(username=str(request.form['username']), password=toHash(value=str(request.form['password']))).first()
        if findUser:
            success = True
            session["user"] = findUser.username
        if success:
            return redirect(url_for('index'))
    return render_template("login.html", title="Login", success=success)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    confirmMsg = None
    success = False
    if request.method == 'POST':
        user = User(username=str(request.form['username']), password=str(request.form['password']))
        success = True
        # 8 to 64 characters
        if len(str(request.form['password'])) < 8 or len(str(request.form['password'])) > 64:
            success = False
            confirmMsg = 'Password must be between 8 and 64 characters'
        if (len(str(request.form['username'])) < 4 or len(str(request.form['username'])) > 64):
            success = False
            confirmMsg = 'Username must be between 4 and 64 characters'
        # Username validation
        if user.username == '':
            success = False
            confirmMsg = 'Invalid username'
        if User.query.filter_by(username=user.username).first():
            confirmMsg = 'This username already exists'
            success = False
        # Password validation
        if user.password == '':
            success = False
            confirmMsg = 'Invalid password'
        if success:
            # Add user
            db.session.add(user)
            db.session.commit()
            confirmMsg = f'New account created: {user.username}, please log in'

    return render_template("signup.html", title="Signup", confirmMsg=confirmMsg, success=success)

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop("user", None)
    return redirect(url_for('index'))


def main():
    db.create_all()
    app.run(debug=True)
    #app.run(host='0.0.0.0', port=8080)


if __name__ == '__main__':
    main()
