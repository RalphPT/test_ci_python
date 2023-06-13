from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTP
from cryptography.fernet import Fernet
from os import environ
from dotenv import load_dotenv

load_dotenv()
print(Fernet.generate_key())
def olvide_password(destinatario):
    fernet = Fernet(environ.get('FERNET_KEY'))
    token = fernet.encrypt(bytes(destinatario, 'utf-8'))

    email = environ.get('EMAIL_EMISOR')
    password = environ.get('PASSWORD_EMAIL_EMISOR')
    mensaje = MIMEMultipart()
    #titulo del correo
    mensaje['Subject'] = 'Olvidaste tu contraseña'

    mensaje['From'] = email
    mensaje['To'] = destinatario
    cuerpo = 'Hola, parece que has olvidado tu correo. Haz click en el siguiente link: http://localhost:5000/resetear-password?token={}'.format(token.decode('utf-8'))
    text = MIMEText(cuerpo, 'plain')

    mensaje.attach(text)

    emisor = SMTP('smtp.gmail.com', 587)

    emisor.starttls()

    emisor.login(email, password)

    emisor.sendmail(from_addr=email, to_addrs=destinatario, msg= mensaje.as_string())

    emisor.quit()

#olvide_password("raffotrejo@gmail.com")