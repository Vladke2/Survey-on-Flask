from flask import render_template, redirect, url_for, flash
from .form import RegisterForm, LoginForm
from app import login_manager, app
from .models import session, User
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash


@login_manager.user_loader
def load_user(user_id):
    return session.query(User).get(user_id)


@app.route('/login', methods=["POST", "GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        user = session.query(User).filter_by(email=email).first()
        if not user:
            flash(f'User with email {email} does not exist. <a href={url_for("register")}>Register', 'error')
            return redirect(url_for('login'))
        elif check_password_hash(user.password, form.password.data):
            login_user(user=user)
            return redirect(url_for('home'))
        else:
            flash('Email or password are incorrect!', 'error')
            return redirect(url_for('login'))
    else:
        return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/register', methods=["POST", "GET"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = RegisterForm()
    if form.validate_on_submit():
        user = session.query(User).filter_by(email=form.email.data).first()
        if user:
            flash(f'User with email {user.email} exist. <a href={url_for("login")}>Login', 'error')
            return redirect(url_for('register'))
        new_user = User(username=form.username.data,
                        email=form.email.data,
                        password=generate_password_hash(form.password.data),
                        age=form.age.data
                        )
        try:
            session.add(new_user)
            session.commit()
            flash('Thanks for registering', "success")
            return redirect(url_for("login"))
        except Exception as exc:
            return exc
        finally:
            session.close()
    return render_template('register.html', form=form)
