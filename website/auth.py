from flask import Blueprint, render_template, url_for,request,flash,redirect
from .models import User
from . import db
from werkzeug.security import generate_password_hash,check_password_hash 
from flask_login import login_user, logout_user,current_user, login_required


auth= Blueprint("auth", __name__)



@auth.route("/signup" ,methods= ['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get("email")
        username = request.form.get("username")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        email_in_use = User.query.filter_by(email=email).first()
        username_in_use = User.query.filter_by(username=username).first()

        if email_in_use:
            flash('Email already exists.', category='error')
        elif len(email) < 8:
            flash('Email is invalid.', category='error')     
        elif username_in_use:
            flash('Username already exists.',category='error')
        elif len(username) < 2:
            flash('Your username is too short.', category='error')    
        elif password1!= password2:
            flash('Passwords do not match', category='error')
        elif len(password1) < 8:
            flash('Your password is too short.', category='error') 
        else:
            new_user = User(email= email, username =username,password = generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('User Created')
            return redirect(url_for('views.home'))
    return render_template('signup.html', user=current_user)

        
        
   

@auth.route("/login",methods= ['GET', 'POST'] )
def login():
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")

        user= User.query.filter_by(email= email).first()
        if user:
            if check_password_hash(user.password, password):   
               flash('Logged In', category='success')
               login_user(user,remember=True)
               return redirect(url_for('views.home'))
            else:
                flash('The password you entered is incorrect', category='error')
        else:
           flash('Email does not exist.', category='error')         

    return render_template('login.html', user=current_user)
    

@auth.route("/logout" )
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.home'))
   
  
    

