from . import auth
from flask import flash, redirect, render_template, request, url_for
from .forms import LoginForm, RegisterForm
from ..models import User

from flask_login import login_user


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query_by_email(form.email.data)
        if user and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Invalid username or password.')

    return render_template('auth/login.html', form=form)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User.query_by_email(form.email.data)
        if user:
            flash('Email has been registed')
            return render_template('auth/register.html', form=form)

        user = User(form.email.data,
                    form.username.data,
                    form.password.data)

        if not user.add_user():
            flash('Email has been registed')
            return render_template('auth/register.html', form=form)

        flash('Reg success please login.')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html', form=form)


@auth.route('/change_password', methods=['GET', 'POST'])
def change_password():
    pass


@auth.route('/logout')
def logout():
    pass
