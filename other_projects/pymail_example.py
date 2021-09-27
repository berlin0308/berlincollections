from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import sys
import smtplib

myaccount = 'berlinchen0308@gmail.com'
ntuaccount = 'b09611007@ntu.edu.tw'

"""輸入信件主旨 內容 (收件者 副本 預設為gmail帳號) (寄件者為gmail帳號)"""
def SendMail(subject,content,receive = myaccount,cc = myaccount ):
    mypassword = 'blackie0308'
    print('start to send mail...')
    sender = myaccount #step1:setup sender gmail,ex:"Fene1977@superrito.com"
    password = mypassword #step2:setup password
    recipient = receive #step3:setup recipients mail
    
    #多個收件人 e.g."Hinte1969@jourrapide.com,Fene1977@rhyta.com,Fene1977@teleworm.us"
    
    outer = MIMEMultipart()
    outer['Subject'] = subject
    outer['To'] = recipient
    outer["Cc"]= cc
    outer['From'] = sender
    
    outer.attach(MIMEText(content))
    mailBody = outer.as_string()

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as s: #send webservice to gmail smtp socket
            s.ehlo()
            s.starttls()
            s.login(sender, password)
            s.sendmail(sender, recipient,mailBody)
            s.close()
        print("mail sent!")
        print("\nSender Account Check:",sender)
        print("Recipient Account Check:",recipient)
        print("\nSubject:",subject)
        print("\nContent:",content)
    except:
        print("Unable to send the email. Error: ", sys.exc_info()[0])
        raise
       

title = "Hello World"
string = "Hello\nWorld"

SendMail(title,string,ntuaccount)
