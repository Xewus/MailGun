# This Python file uses the following encoding: utf-8

from peewee import (BooleanField, CharField, ForeignKeyField, IntegerField,
                    Model)

from src.core.utils import get_contact_from_csv
from src.settings import (MAX_LENGTH_EMAIL, MAX_LENGTH_PASSWORD,
                          MAX_LENGTH_USERNAME)
from src.web.server import db


class BaseModel(Model):
    class Meta:
        database = db.database


class User(BaseModel):
    username = CharField(
        max_length=MAX_LENGTH_USERNAME,
        null=False
    )
    email = CharField(
        max_length=MAX_LENGTH_EMAIL,
        null=False,
        unique=True
    )
    password = CharField(
        max_length=MAX_LENGTH_PASSWORD,
        null=False
    )
    level = IntegerField(
        null=False,
        default=10
    )
    active = BooleanField(default=True)
    admin = BooleanField(default=False)

    class Meta:
        table_name = 'user'


class Contacts(BaseModel):
    user_id = ForeignKeyField(
        model=User,
        backref='contacts'
    )
    email = CharField(
        max_length=MAX_LENGTH_EMAIL,
        null=False
    )
    name = CharField(
        max_length=MAX_LENGTH_USERNAME,
        null=False
    )

    class Meta:
        table_name = 'contacts'

    @staticmethod
    def insert_from_csv(file_name, user_id, delete_old=True):
        """Fill in a table with contacts for the user from `csv` file.

        #### Args:
        - file_name (str): The path to file.csv with contacts.
        - user_id: The contacts`s owner id.
        - delete_old (bool): Whether to delete old contacts.

        #### Returns:
        - str: 'Inserted %d rows'
        """
        data = get_contact_from_csv(file_name, user_id)
        if delete_old:
            Contacts.delete().where(Contacts.user_id == user_id).execute()
        Contacts.insert_many(
            data,
            fields=[Contacts.email, Contacts.name, Contacts.user_id]
        ).execute()

    @staticmethod
    def get_user_contacts(user_id):
        """Get the list contacts of the user.

        #### Args:
        - user_id: The contacts`s owner id.

        #### Returns:
        - list[dict['email': str, 'name': str, 'user_id': int]]
        """
        return Contacts.select().where(
            Contacts.user_id == user_id
        ).dicts()
