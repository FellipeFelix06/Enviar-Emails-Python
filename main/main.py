from dotenv import load_dotenv
from email import encoders
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from string import Template
from datetime import datetime
from pathlib import Path
from smtplib import SMTP
import locale
import os

load_dotenv()

set_locale = locale.setlocale(locale.LC_ALL, '')

DIR_ANEXO = Path(__file__).parent / 'doc.pdf'
DIR_HTML = Path(__file__).parent / 'index.html'

remetente = os.getenv('FROM_EMAIL', '')
destinatario = os.getenv('TO_EMAIL', '')

smtp_server = 'smtp.gmail.com'
smtp_port = 587
smtp_username = remetente
smtp_password = os.getenv('EMAIL_PASSWORD', '')

subject = 'Nova mensagem para ${email}'
template_subject = Template(subject)

mime_multipart = MIMEMultipart()
mime_multipart['FROM'] = remetente
mime_multipart['TO'] = destinatario
mime_multipart['SUBJECT'] = template_subject.substitute(email=destinatario)

def converte_brl(valor):
    brl = 'R$' + locale.currency(val=valor, symbol=False, grouping=True)
    return brl

def data_exibida():
    data_atual = datetime.now()
    data_formatada = data_atual.strftime('%d/%m/%Y')
    return data_formatada


with open(DIR_HTML, 'r') as html:
    body = html.read()
    template_body = Template(body)
    body = template_body.substitute(data=data_exibida(),
    valor=converte_brl(125006), nome='Fellipe'
    )

with open(DIR_ANEXO, 'rb') as file:
    part = MIMEBase('application', 'pdf')
    part.set_payload(file.read())
    encoders.encode_base64(part)
    part.add_header('content-disposition', 'attachment',
    filename=DIR_ANEXO.name
    )
    mime_multipart.attach(part)
    mime_multipart.attach(MIMEText(body, 'html'))

with SMTP(smtp_server, smtp_port) as server:
    server.ehlo()
    server.starttls()
    server.login(smtp_username, smtp_password)
    server.send_message(mime_multipart)