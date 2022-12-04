import jinja2
from flask import Flask
from flask_peewee.db import Database

from src.settings import EMAIL_TEMPLATES_DIR, PAGE_TEMPLATES_DIR, FlaskConfig

flask_app = Flask(__name__)

flask_app.config.update(**FlaskConfig)
flask_app.config["APPLICATION_ROOT"] = "/abc/123"

db = Database(app=flask_app)

jinja_loader = jinja2.ChoiceLoader([
    jinja2.FileSystemLoader(PAGE_TEMPLATES_DIR),
    jinja2.FileSystemLoader(EMAIL_TEMPLATES_DIR)
])

flask_app.jinja_loader = jinja_loader

from src.db.models import Contacts, User
from src.web.authtorisation import MyAuth

auth = MyAuth(
    app=flask_app,
    db=db,
    user_model=User,
    prefix='/spam',
    default_next_url='/spam'
)

User.create_table(fail_silently=True)
Contacts.create_table(fail_silently=True)

from .views import blue

flask_app.register_blueprint(
    blueprint=blue,
    url_prefix='/spam'
)
