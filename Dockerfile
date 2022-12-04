FROM python:2.7.18-slim-stretch
LABEL author="xewus" version="test"
RUN mkdir /mailgun
COPY ./requirements.txt /mailgun/
RUN pip2 install -r /mailgun/requirements.txt --no-cache-dir
COPY . .
ENV SECRET_KEY=Your2secret1key
ENV CELERY_BROKER_URL=redis://172.17.0.2:6379/0
CMD celery worker -A src.celery_tasks.tasks -B -l info & waitress-serve src.web.server:flask_app