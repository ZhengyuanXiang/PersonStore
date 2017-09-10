from . import auth
from flask import flash, redirect, render_template, request, url_for
from .forms import LoginForm, RegisterForm
from ..models import User
from .. import db

from flask_login import login_user, current_user

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Invalid username or password.')

    return render_template('auth/login.html', form=form)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            flash('Email has been registed')
            return render_template('auth/register.html', form=form)

        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Regist success please login.')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html', form=form)

@auth.route('/change_password', methods=['GET', 'POST'])
def change_password():
    pass

@auth.route('/logout')
def logout():
    pass

