from ast import pattern
import email
from email import encoders
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import json
from logging import exception
import os
import re
import smtplib
import ssl
import pyqrcode
PATH_TO_DATA = "./data/"

def check_email(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if(re.fullmatch(regex, email)):
        return True
    return False

def check_student_name(name):
    pattern = r"^([A-Za-z \-]{2,25})+$"
    if(re.fullmatch(pattern, name)):
        return True
    return False

def check_class_name(name):
    regex = r'[0-9]{1,2}-[A-Z]'
    if(re.fullmatch(regex, name)):
        return True
    return False


def send_email(registration_number,receiver_email,student_name,class_name):

    try:
        port = 587  # For starttls
        smtp_server = "smtp.office365.com"
        sender_email = "miniProject101@outlook.com"
        password = 'ehhuwzqtsigzygtl'


        #Setup the MIME
        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = receiver_email
        message['Subject'] = 'Thanks for Registration.'


        mail_content = '''Hello,\nThis is a confirmation mail.\nThanks for registration for the class.\nPlease find the attached QR code for attendance.\nStudent Name : {}\nRegistration Number : {}\nClass Name : {}'''.format(student_name,registration_number,class_name)
        
        message.attach(MIMEText(mail_content, 'plain'))
        attach_file_name = PATH_TO_DATA+class_name+"/qr/"+student_name+"-"+registration_number+".png"
        attach_file = open(attach_file_name, 'rb') # Open the file as binary mode
        payload = MIMEImage(attach_file.read(), name=student_name+"-"+registration_number+".png")

        message.attach(payload)
        text = message.as_string()

        context = ssl.create_default_context()
        with smtplib.SMTP(smtp_server, port) as server:
            server.starttls(context=context)
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, text)
        attach_file.close()
        return True

    except Exception as e:
        print(e)
        return False



def add_student(registration_number,email_id,student_name,class_name):

    try:
        path_name = PATH_TO_DATA+class_name+"/"
        if not os.path.isdir(path_name):
            os.makedirs(path_name)

        qr_path = path_name+"qr/"
        if not os.path.isdir(qr_path):
            os.makedirs(qr_path)

        
        filename = path_name+str(class_name)+".xls"

        if not os.path.isfile(filename):
            fob=open(filename,'a+')
            fob.write("Registration No."+'\t')
            fob.write("Student Name"+'\t')
            fob.write("Email ID"+'\n')
            fob.write("Class Name"+'\t')
            fob.close()
        
        fob=open(filename,'a+')
        fob.write(registration_number+'\t'+student_name+'\t'+email_id+'\t'+class_name+'\n') 
        fob.close()

        data = json.dumps({
                "registration_number":registration_number,
                "student_name":student_name,
                "email_id":email_id,
                "class_name":class_name
            })
        
        save_name = str(student_name+"-"+registration_number+'.png')
        save_dir=qr_path+save_name

        qr = pyqrcode.create(data)
        qr.png(save_dir, scale=6)
        
        return True
    except Exception as e:
        print(e)
        return False

if __name__=="__main__":
    add_student("284036","khungaur@gmail.com","Yajur Gaur","3-C")