import smtplib
import socket
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from jinja2 import Environment, FileSystemLoader

from src.settings import (EMAIL_TEMPLATES_DIR, GOOGLE_CODE_CONNECTED,
                          GOOGLE_CODE_LOGINED, GOOGLE_HOST, GOOGLE_PORT)

env = Environment(
    loader=FileSystemLoader(EMAIL_TEMPLATES_DIR))


class SmtpConnection(object):
    """Create connection to SMTP.
    """
    set_connection = 'No connection'

    def __init__(
        self, user_email, password, host=None, port=None, timeout=None
    ):
        self.timeout = timeout or 2  # default 2 seconds
        self.email = user_email
        if user_email.split('@')[-1] == 'gmail.com':
            self.__init_google_mail(password=password)
        else:
            return

    def __init_google_mail(self, password):
        """Connect to Google SMTP and set attr self.set_connection.
        If connection `OK`,
        `self.set_connection` == None,
        else message with error.
        """
        self.password = password
        self.host = GOOGLE_HOST
        self.port = GOOGLE_PORT
        self.set_connection = self.__set_google_connection()

    def __set_google_connection(self):
        """Create a connection to the `Google SMTP server`.

        #### Returns:
        - None: Connection OK.
        - str: A message with an error conection.
        """
        try:
            self.smtp = smtplib.SMTP(
                host=self.host, port=self.port, timeout=self.timeout
            )

            code, _ = self.smtp.starttls()
            if code not in GOOGLE_CODE_CONNECTED:
                return 'Remote server returned unexpected code: %s' % code

            code, _ = self.smtp.login(user=self.email, password=self.password)
            if code not in GOOGLE_CODE_LOGINED:
                return 'Remote server returned unexpected code: %s' % code

        except socket.timeout:
            return 'The host `%s` didn`t respond.' % self.host

        except smtplib.SMTPAuthenticationError:
            return 'Incorrect email or application_key.'
        return None

    def check_connection(self):
        err = self.set_connection
        if not err:
            self.smtp.close()
            return None
        return err


class HtmlEmail(object):
    """To render an email with html template and send it.
    """
    def __init__(
        self,
        template,
        from_addr,
        recepient,
        password,
        payload=None,
        header=None,
        standart=True
    ):
        self.from_addr = from_addr
        self.to_addr = recepient['email']
        if standart:
            self.email = self.__make_standart_emal(
                template, from_addr, recepient, payload, header
            )
        self.connection = SmtpConnection(
            user_email=from_addr,
            password=password
        )

    def __make_standart_emal(
        self, template, from_addr, recepient, payload=None, header=None
    ):
        """Make an email with given an HTML-temlate.

        #### Returns:
        - str: An email as string ready to send.
        """
        if payload:
            recepient.update(payload)

        template = env.get_template(template)
        email_text = template.render(recepient)
        email = MIMEMultipart('alternative')
        email['From'] = from_addr

        if recepient:
            email['To'] = recepient['email']
        if header:
            email['Subject'] = Header(header, charset='utf-8')

        email.attach(MIMEText(email_text, 'html', 'utf-8'))
        return email.as_string()

    def send(self):
        """Send email.
        """
        self.connection.smtp.sendmail(
            from_addr=self.from_addr,
            to_addrs=self.to_addr,
            msg=self.email
        )
