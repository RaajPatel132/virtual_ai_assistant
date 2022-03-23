import smtplib
from configparser import ConfigParser
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import speech_recognition as sr
from gtts import gTTS
from playsound import playsound
import os

def mic_input():
    """
    Fetch input from mic
    :return: user's voice input as text if true, false if fail
    """
    try:
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print('Say something...')
            r.pause_threshold = 1
            r.adjust_for_ambient_noise(source, duration=1)
            audio = r.listen(source)
        try:
            command = r.recognize_google(audio).lower()
            print('You said: ' + command + '\n')
        except sr.UnknownValueError:
            print('....')
            command = self.mic_input()
        return command
    except Exception as e:
        print(e)
        return False


def text2speech(text):
    """
    Convert any text to speech
    :param text: text (String)
    :return: True / False (Play sound if True otherwise write exception to log and return False)
    """
    try:
        myobj = gTTS(text=text, lang='en', slow=False)
        myobj.save("tmp.mp3")
        playsound("tmp.mp3")
        os.remove("tmp.mp3")
        return True
    except Exception as e:
        mytext = "Sorry I couldn't understand, or not implemented to handle this input"
        print(mytext)
        myobj = gTTS(text=mytext, lang='en', slow=False)
        myobj.save("tmp.mp3")
        playsound("tmp.mp3")
        os.remove("tmp.mp3")
        print(e)
        return False

def send(config_path):
    print("To use this features make sure you have enabled less secure apps: \
                 https://myaccount.google.com/lesssecureapps")

    configur = ConfigParser()
    print(configur.read(config_path))

    email = configur.get('default', 'email_address')

    if email == '':
        return "Please run 'setup' command to set your email id first."

    # get Recipient email id#
    print('Who is the recipient?')
    text2speech('Who is the recipient?')
    recipient = input("Enter Email ID: ")

    # get subject#
    print('What is subject of email?')
    text2speech('What is subject of email?')
    subject = mic_input()
    print(subject)

    # get message#
    print('What should I say to them?' + recipient)
    text2speech('What should I say to them?')
    message = mic_input()
    print(message)

    # sender email#
    print("Is this your email ID?: " + email)
    text2speech("Is this your email ID?: " + email)
    text2speech("Confirm by typing y/Y for yes or anything else for NO")
    ch = input("Confirm by typing y/Y for yes or anything else for NO: ")
    if ch.lower() == 'y':
        text2speech("Please enter your password-")
        sender_password = input("Password (we never save or share password): ")
        sender_email = email
        ##Build message ###
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient
        msg['Subject'] = subject
        # message = 'here is the email'
        msg.attach(MIMEText(message))
        try:
            # send mail#
            mail = smtplib.SMTP('smtp.gmail.com', 587)
            mail.ehlo()
            mail.starttls()
            mail.login(sender_email, sender_password)
            mail.sendmail(sender_email, recipient, msg.as_string())
            mail.close()
            return 'Email has been sent successfully. You can check your inbox.'

        except Exception as e:
            return "Unable to send mail, please check your credentials. Or there may be some technical error"
    else:
        return "Please run 'setup' command to set your email id first."