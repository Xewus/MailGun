# This Python file uses the following encoding: utf-8
 
from validate_email import validate_email
from wtforms.validators import StopValidation


class EmailValidator(object):
    def __init__(self, message = None, verify=False):
        self.message = message or u'Некорректная почта'
        self.verify = verify

    def __call__(self, form, field):
        if field.data is None:
            raise StopValidation(self.message)
        if not validate_email(field.data, verify=self.verify):
            raise StopValidation(self.message)
