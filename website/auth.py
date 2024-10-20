from flask import Blueprint, redirect, render_template, request, flash, session, url_for
from werkzeug.security import generate_password_hash, check_password_hash

from helpers import get_user, is_found, save_user
from website.models import User

auth = Blueprint('auth', __name__)

@auth.route("/login", methods=['GET', 'POST'])
def logIn():

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = get_user(email)
        
        if user:
            if check_password_hash(user['password'], password):
                flash("logged in successfully", category='success')
                return redirect(url_for('auth.auth_success', email=email))
            else:
                flash("Incorrect password", category='error')
        else:
            flash("Email doesn't exist", category='error')

    return render_template("login.html")



@auth.route("/sign-up", methods=['GET', 'POST'])
def signUp():
    
    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        lastName = request.form.get('lastName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        phoneNumber = request.form.get('number')

        # Validation checks

        if len(email) < 4:
            flash("Email must be greater than 3 characters.", category='error')
        elif(is_found(email)):
            print("Email is already registered before")
            flash("Email is already registered before", category='error')
        elif len(firstName) < 2:
            flash("First name must be greater than 1 character.", category='error')
        elif len(lastName) < 2:
            flash("Last name must be greater than 1 character.", category='error')
        elif len(password1) < 7:
            flash("Password must be at least 7 characters.", category='error')
        elif password1 != password2:
            flash("Passwords don't match.", category='error')
        else:

            # Create new user with hashed password
            new_user = User(email=email, firstName=firstName, lastName=lastName, phoneNumber=phoneNumber, password=generate_password_hash(password1, method='pbkdf2:sha256'))
            # add the user to jason file
            save_user(new_user, fileName='users.json')

            flash('Account created successfully!', category='success')

            return redirect(url_for('auth.auth_success', email=email))

    return render_template("sign_up.html")
    

@auth.route("/log-out")
def logOut():
    flash("you have logged out", "success")
    session.clear()
    return render_template("slots.html", log_out=True)


@auth.route("/auth-success")
def auth_success():
    email = request.args.get('email')
    session["email"] = email
    return render_template("slots.html", email=email)
