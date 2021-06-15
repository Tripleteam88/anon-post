from flask import Flask, render_template, url_for, request, session, redirect
from datetime import timedelta
from anonposts_classes import User, Post
import os


app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.permanent_session_lifetime = timedelta(days=1)

users = []
posts = []

@app.route('/index.html')
@app.route('/')
def index():
    return render_template("index.html", title="Home", session=session, posts=posts)

@app.route('/user', methods=['GET'])
def user():
    if "user" in session:
        user = session["user"]
    return render_template("user.html", user=user)

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
        post = Post(str(request.form['title']), postauthor, str(request.form['content']), (len(posts)+1))
        posts.insert(0, post)
        return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    success = None
    if request.method == 'GET':
        pass
    elif request.method == 'POST':
        success = False
        for user in users:
            if user.username == str(request.form['username']) and user.password == user.toHash(str(request.form['password'])):
                success = True
                session["user"] = user.username
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
        # Username validation
        if user.username == '':
            success = False
            confirmMsg = 'Invalid username'
        for otherUser in users:
            if otherUser.username == user.username:
                confirmMsg = 'This username already exists'
                success = False
                break
        # Password validation
        if user.password == '':
            success = False
            confirmMsg = 'Invalid password'
        if len(str(request.form['password'])) < 8 or len(str(request.form['password'])) > 64:
            success = False
            confirmMsg = 'Password must be between 8 and 64 characters'
        if success:
            # ID validation
            existingID = []
            for otherUser in users:
                existingID.append(otherUser.ID)
            while user.ID in existingID:
                user.genID()
            # Add user
            users.append(user)
            confirmMsg = f'New account created: {user.username}, please log in'

    return render_template("signup.html", title="Signup", confirmMsg=confirmMsg, success=success)

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop("user", None)
    return redirect(url_for('index'))



if __name__ == '__main__':
    app.run(debug=True)
