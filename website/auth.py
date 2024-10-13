from flask import Blueprint

auth = Blueprint('auth', __name__)

@auth.route("/log-in")
def logIn():
    return "here is the login page"

@auth.route("/log-out")
def logOut():
    return "here is the log out page"

@auth.route("/sign-up")
def signUp():
    return "here is the signup page"