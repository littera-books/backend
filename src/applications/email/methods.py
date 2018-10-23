import os

from jinja2 import Environment, FileSystemLoader

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import aiosmtplib

from common.read_secrets import secret_json


def initial_smtp_instance():
    return aiosmtplib.SMTP(
        hostname=secret_json['SMTP_HOST'],
        port=secret_json['SMTP_PORT'],
        use_tls=False
    )


def get_message(addr, user_id, first_name, host, scheme):
    TEMPORARY_DIR = os.path.dirname(os.path.abspath(__file__))
    env = Environment(
        loader=FileSystemLoader(TEMPORARY_DIR),
        trim_blocks=True
    )
    template = env.get_template('ActivateEmailTemplate.html')

    message = MIMEMultipart('alternative')
    message['Subject'] = '[Littera] 가입 활성화 메일'
    message['From'] = secret_json['EMAIL_HOST']
    message['To'] = addr

    url = f'{host}://{scheme}/activate?email={addr}&pk={user_id}'

    html = MIMEText(template.render(
        first_name=first_name,
        url=url,
    ), 'html')

    message.attach(html)

    return message


def get_reset_message(addr, password):
    TEMPORARY_DIR = os.path.dirname(os.path.abspath(__file__))
    env = Environment(
        loader=FileSystemLoader(TEMPORARY_DIR),
        trim_blocks=True
    )
    template = env.get_template('ResetPasswordTemplate.html')

    message = MIMEMultipart('alternative')
    message['Subject'] = '[Littera] 비밀번호 초기화 메일'
    message['From'] = secret_json['EMAIL_HOST']
    message['To'] = addr

    url = f'http://localhost:3006/sign-in'

    html = MIMEText(template.render(
        addr=addr,
        password=password,
        url=url,
    ), 'html')

    message.attach(html)

    return message


async def send_activate_mail(smtp_instance, addr, user_id, first_name, host, scheme):
    await smtp_instance.connect()
    await smtp_instance.ehlo()
    await smtp_instance.starttls()
    await smtp_instance.login(username=secret_json['EMAIL_HOST'], password=secret_json['EMAIL_PW'])

    message = get_message(addr, user_id, first_name, host, scheme)

    await smtp_instance.sendmail(secret_json['EMAIL_HOST'], addr, message.as_string())
    await smtp_instance.quit()


async def send_reset_password_mail(smtp_instance, addr, password):
    await smtp_instance.connect()
    await smtp_instance.ehlo()
    await smtp_instance.starttls()
    await smtp_instance.login(username=secret_json['EMAIL_HOST'], password=secret_json['EMAIL_PW'])

    message = get_reset_message(addr, password)

    await smtp_instance.sendmail(secret_json['EMAIL_HOST'], addr, message.as_string())
    await smtp_instance.quit()
