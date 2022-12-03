FROM python:2.7.18-slim-stretch
LABEL author="xewus" version="test"
RUN mkdir /mailgun
COPY ./requirements.txt /mailgun/
RUN pip2 install -r /mailgun/requirements.txt --no-cache-dir
COPY src/ flask_run.py start_app.py /mailgun/
WORKDIR /mailgun
ENV SECRET_KEY=Your2secret1key
CMD [ "./start_app.py" ]
