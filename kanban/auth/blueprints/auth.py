import sqlite3
from datetime import datetime
from flask import (Blueprint, flash, redirect, render_template,
                   request, session, url_for, jsonify, g)

# for handling forms
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length

# for password hashing
from flask_bcrypt import generate_password_hash, check_password_hash

# allows this to be registered as a blueprint
bp = Blueprint('auth', __name__,
               static_folder='../static',
               template_folder='../templates'
               )


# classes to contain forms input fields
class RegisterForm(FlaskForm):
    username = StringField(validators=[DataRequired(), Length(min=3, max=20)])
    password = PasswordField(validators=[DataRequired(), Length(min=8, max=128)])
    confirm_password = PasswordField(validators=[DataRequired(), Length(min=8, max=128)])


class LoginForm(FlaskForm):
    username = StringField(validators=[DataRequired()])
    password = PasswordField(validators=[DataRequired()])
    submit = SubmitField('Log In')


# registration page
@bp.route('/register', methods=('GET', 'POST'))
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # make sure that password & confirm password are the same
        if form.confirm_password.data != form.password.data:
            form.username.errors.append('The passwords you entered do not match.')
            return render_template('auth/register.html', form=form)

        # add new user to database
        db = g.db
        command = 'INSERT INTO users (username, password_hash, display_name, created_at) VALUES (?, ?, ?, ?)'
        try:
            db.execute(
                command,
                (
                    form.username.data.lower(),
                    generate_password_hash(form.password.data),
                    form.username.data,
                    datetime.now()
                )
            )
            db.commit()
            flash('Your account has been created. Please login to continue.', 'success')
            return redirect(url_for('auth.login'))
        except sqlite3.IntegrityError:
            # username already taken
            form.username.errors.append('This username is already taken. Please choose a different one.')
            return render_template('auth/register.html', form=form)
    else:
        return render_template('auth/register.html', form=form)


# login page
@bp.route('/login', methods=('GET', 'POST'))
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db = g.db
        try:
            command = 'SELECT id, password_hash FROM users WHERE username = ?'
            user = db.execute(command, (form.username.data.lower(),)).fetchone()

            # check if user exists
            if user:
                # check if password_hash matches
                if check_password_hash(user['password_hash'], form.password.data):
                    session['user_id'] = user['id']
                    return redirect(url_for('kanban.index'))

            form.username.errors.append('Invalid username or password.')
            return render_template('auth/login.html', form=form)
        except sqlite3.IntegrityError:
            form.username.errors.append('Invalid username or password.')
            return render_template('auth/login.html', form=form)
    else:
        return render_template('auth/login.html', form=form)


@bp.route('/logout')
def logout():
    session.clear()
    flash('You have been successfully logged out.', 'success')
    return redirect(url_for('auth.login'))


# api for checking if username is available
@bp.route('/check-username')
def check_username():
    username = request.args.get('username', '').lower()
    if not username:
        return jsonify(available=False)

    db = g.db
    user = db.execute('SELECT id FROM users WHERE username=?', (username,)).fetchone()
    return jsonify(available=(user is None))