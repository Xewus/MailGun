from celery import Celery

from src.core.emails import HtmlEmail
from src.settings import CELERY_BROKER_URL

celery_app = Celery(
    __name__,
    broker=CELERY_BROKER_URL,
    C_FORCE_ROOT=1
)

celery_app.config_from_object(__name__)


@celery_app.task(name='sending_mail')
def celery_send_mail(
    user_email, password, recepients, template, payload
):
    """Sending emails with Celery.

    #### Args:
    - user_email (str): An email of sender.
    - recepients (list): Resepients emails.
    - template (str): A name of template for message.
    - payload (dict): A dict with variables to rendering the template.
    """
    for recepient in recepients:
        email = HtmlEmail(
            template=template,
            from_addr=user_email,
            password=password,
            recepient=recepient,
            payload=payload
        )
        email.send()
