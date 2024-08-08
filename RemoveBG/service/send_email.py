import email.message 
import smtplib
from django.conf import settings

from Master.settings import BASE_DIR


class DataEmail():

    def read_layout_email(type):
        with open(f'{BASE_DIR}/RemoveBG/service/layout-email/{type}.txt') as f:
            print("f", f)
            return f.read()

    def auto_email_contact_inside(request):

        body_email = DataEmail.read_layout_email(type='layout_email_inside')

        # body_email = body_email.replace('{number_for_whats}', f'api.whatsapp.com/send/?phone={request.data["phoneContact"]}')
        # body_email = body_email.replace('{phone_contact}', request.data["phoneContact"])
        body_email = body_email.replace('{logo_principal}', f'{settings.SITE_URL}{settings.STATIC_URL}img/logo-principal.png')
        body_email = body_email.replace('{logo_footer}', f'{settings.SITE_URL}{settings.STATIC_URL}img/favicon_32x32.ico')
        body_email = body_email.replace('{name_contact}', request.POST["name"])
        body_email = body_email.replace('{email_contact}', request.POST["email"])
        body_email = body_email.replace('{message_contact}', request.POST["message"])
        
        msg = email.message.Message()
        msg['Subject'] = "E-mail automatico - Contato"
        msg['From'] = "contato@masterremovebg.com"
        msg['To'] = "contato@masterremovebg.com"  # Inserir o email de destino
        password = "Trashcomics2?"
        msg.add_header('Content-Type', 'text/html')
        msg.set_payload(body_email)

        s = smtplib.SMTP_SSL('smtp.kinghost.net', 465)
        s.login(msg['From'], password)
        s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))
        print('Email enviado')