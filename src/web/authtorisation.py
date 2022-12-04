# This Python file uses the following encoding: utf-8

from flask import flash, g, redirect, render_template, session, url_for
from flask_peewee.auth import Auth

from src.core.emails import SmtpConnection
from src.db.models import User
from src.web.forms import LoginForm


class MyAuth(Auth):
    """The model for authorization and authentication services.
    """
    def get_user_model(self):
        return User

    def authenticate(self, username, user_email, password):
        try:
            user = self.User.get(email=user_email)
        except self.User.DoesNotExist:
            user = self.User.create(
                username=username,
                email=user_email,
                password=password
            )
        else:
            if not user.active:
                return None, u'Вы деактивированы'
        return user, None

    def login_user(self, user):
        """Inject tne user into the session.
        """
        session['logged_in'] = True
        session['user_pk'] = user._pk
        session.permanent = True
        g.user = user
        flash(u'Вход выполнен', 'success')

    def login(self):
        error = None
        form = LoginForm()
        if form.validate_on_submit():
            smtp = SmtpConnection(
                user_email=form.user_email.data,
                password=form.password.data
            )
            error = smtp.check_connection()
            if error is None:
                authenticated_user, error = self.authenticate(
                    username=form.username.data,
                    user_email=form.user_email.data,
                    password=form.password.data
                )
            if error is None:
                self.login_user(authenticated_user)
                flash(
                    u'Рассылка будет с адреса: %s' % form.user_email.data
                 )
                return redirect(url_for('spamer.index_view'))
            flash(error)

        return render_template('login.html', 
            title = 'Sign In',
            form = form,
            error = error
        )

    def logout_user(self):
        if self.clear_session:
            session.clear()
        else:
            session.pop('logged_in', None)
        g.user = None
        flash(u'Вы вышли из аккаунта', 'success') 
