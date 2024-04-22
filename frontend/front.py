"""Code for a flask frontend to access the API and display the data for users and admins"""
import os, requests
from flask import jsonify, request, Flask, redirect, url_for, flash, g
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)

login_manager = LoginManager(app)
login_manager.login_view = "login"


api_url = os.getenv("API_URL")


class User(UserMixin):
    """Class to create a user object"""
    def __init__(self, id, name, email, password, admin=False):
        self.id = id
        self.name = name
        self.email = email
        self.password = password
        self.admin = admin
    
    @classmethod
    def get(cls, user_id):
        # Replace this with the actual code to get the user from the API
        response = requests.get(f'{api_url}/user/{user_id}')
        if response.status_code == 200:
            data = response.json()
            return cls(id=data[0], name=data[1], email=data[2], password=data[3])#, admin=data[4])
        return None


login_manager.user_loader(User.get)


@app.route("/")
def index():
    """Function to render the page for the users and admins"""
    body = "<h1>Med service</h1>"
    body += "<button onclick='window.location.href=\"/login\"'>Login</button>"
    body += "<button onclick='window.location.href=\"/register\"'>Register</button>"
    return body


@app.route("/login", methods=["GET"])
def login():
    """Function to render the login page"""
    body = "Login page"
    body += "<form action='/login' method='post'>"
    body += "<input type='text' name='email' placeholder='Email'>"
    body += "<input type='password' name='password' placeholder='Password'>"
    body += "<input type='submit' value='Login'>"
    body += "</form>"
    return body


@app.route("/login", methods=["POST"])
def login_post():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
    # Replace this with the actual code to authenticate the user
    response = requests.post(f'{api_url}/login', json=request.form.to_dict())
    if response.status_code == 200:
        data = response.json()
        user = User.get(data['id'])
        if user is None:
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user)
        return redirect(url_for('profile'))
    flash('Invalid username or password')
    return redirect(url_for('login'))


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route("/register")
def register():
    """Function to render the register page"""
    body = "Register page"
    body += "<form action='/register' method='post'>"
    body += "<input type='text' name='name' placeholder='Name'>"
    body += "<input type='text' name='email' placeholder='Email'>"
    body += "<input type='password' name='password' placeholder='Password'>"
    body += "<input type='submit' value='Register'>"
    body += "</form>"
    return body


@app.route("/register", methods=["POST"])
def register_post():
    # Replace this with the actual code to register the user
    response = requests.post(f'{api_url}/create', json=request.form.to_dict())
    if response.status_code == 200:
        return redirect(url_for('login'))
    flash('Invalid username or password')
    return redirect(url_for('register'))


@app.route("/profile")
@login_required
def profile():
    """Function to render the profile page"""
    body = "Profile page"
    body += f"<p>Welcome, {current_user.name}</p>"
    body += "<button onclick='window.location.href=\"/logout\"'>Logout</button>"
    return body


if __name__ == "__main__":
    app.secret_key = "super secret key"
    app.run(debug=True, host="0.0.0.0", port=5500)
