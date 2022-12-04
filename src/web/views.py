# This Python file uses the following encoding: utf-8

from random import randint

from flask import (Blueprint, flash, g, redirect, render_template, request,
                   url_for)

from src.celery_tasks.tasks import celery_send_mail
from src.core.utils import get_list_email_templates, save_uploaded_file
from src.db.models import Contacts
from src.web.forms import AddContactForm, ChoiceTemplateForm
from src.web.server import auth

blue = Blueprint(name='spamer', import_name=__name__)


@blue.route('/')
def index_view():
    return render_template(
        'index.html', title=u'Сервис рассылки электронных писем'
    )


@blue.route('/list_templates')
def list_email_templates_view():
    return render_template(
        'list_templates.html',
        title=u'Список шаблонов',
        templates=get_list_email_templates()
    )


@blue.route('/load_contacts', methods=('GET', 'POST',))
@auth.login_required
def load_contacts_view():
    if request.method == 'POST' and request.files['file']:
        file_name = save_uploaded_file(request.files['file'], g.user.id)
        if file_name:
            Contacts.insert_from_csv(file_name, g.user.id)
            flash(u'Контакты добавлены')
            return redirect(url_for('spamer.index_view'))
        flash(u'Файл `%s` несохранён' % request.files['file'].filename)
    return render_template(
        'upload_contacts.html', title=u'Загрузить контакты'
    )


@blue.route('/add_contact', methods={'GET', 'POST'})
@auth.login_required
def add_contact_view():
    message = u'Контакт был добавлен'
    form = AddContactForm()
    if request.method == 'POST' and form.validate_on_submit():
        contact, added = Contacts.get_or_create(
            user_id=g.user.id,
            email=form.contact_email.data,
            name=form.contact_name.data
        )
        if not added:
            message += u' ранее'
        flash(message)
    return render_template(
        'add_contact.html', title=u'Добавить контакт', form=form
    )


@blue.route('/look_template/<template>')
def look_template_view(template):
    return render_template(template)


@blue.route('/choose_template', methods=('GET', 'POST'))
@auth.login_required
def choose_template_view():
    form = ChoiceTemplateForm()
    recepients = Contacts.get_user_contacts(g.user.id)

    if not recepients:
        flash(u'Некому рассылать, добавьте список контактов')
        return redirect(url_for('spamer.load_contacts_view'))

    templates = list(enumerate(get_list_email_templates()))
    form.choice.choices = templates

    pivot = randint(0, len(recepients) - 1)
    recepients = recepients[pivot:pivot + g.user.level]

    payload = {
        'username': g.user.username
    }

    if request.method == 'POST' and form.validate_on_submit():
        template = templates[int(form.choice.data)][1]

        celery_send_mail.apply_async((
            g.user.email,
            g.user.password,
            recepients,
            template,
            payload,
        ), countdown=form.countdown.data * 60 * 60)  # to hour

        flash(u'Рассылка с шаблоном `%s` начата' % template)

        return redirect(url_for('spamer.index_view'))

    return render_template(
        'choose_template.html',
        title='Начать рассылку',
        form=form
    )
