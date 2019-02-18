'''
Created on Aug 27, 2016
@author: Burkhard
'''

from GMAIL_PWD import GMAIL_PWD, MAIN_EMAIL

import imaplib
import email

import base64

def extract_body(payload):
    if isinstance(payload,str):
        return payload
    else:
        return '\n'.join([extract_body(part.get_payload()) for part in payload])

def read_email_1():

    conn = imaplib.IMAP4_SSL("imap.gmail.com", 993)
    conn.login(MAIN_EMAIL, GMAIL_PWD)
    conn.select()
    typ, data = conn.search(None, 'UNSEEN')
    try:
        for num in data[0].split():
            typ, msg_data = conn.fetch(num, '(RFC822)')
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_string(response_part[1])
                    subject=msg['subject']
                    print(subject)
                    payload=msg.get_payload()
                    body=extract_body(payload)
                    print(body)
            typ, response = conn.store(num, '+FLAGS', r'(\Seen)')
    finally:
        try:
            conn.close()
        except:
            pass
        conn.logout()


def read_email_2():
    YA_HOST = "imap.gmail.com"#"imap.yandex.ru"
    YA_PORT = 993
    YA_USER = MAIN_EMAIL
    YA_PASSWORD = GMAIL_PWD
    SENDER = MAIN_EMAIL

    connection = imaplib.IMAP4_SSL(host=YA_HOST, port=YA_PORT)
    connection.login(user=YA_USER, password=YA_PASSWORD)

    status, msgs = connection.select('INBOX')
    assert status == 'OK'

    typ, data = connection.search(None, '(UNSEEN)', 'FROM', '"%s"' % SENDER)
    print(data)
    for num in data[0].split():
        typ, message_data = connection.fetch(num, '(RFC822)')
        #print(data)
        print('Message %s\n%s\n' % (num, message_data[0][1]))
        mail = email.message_from_bytes(message_data[0][1])
        print("Mail" ,mail)
        for part in mail.walk():
            content_type = part.get_content_type()
            print(content_type)
            play_load = part.get_payload()
            print(play_load)
            print(part["Date"])
            print(part["Subject"])
            print(part["From"])
            print(part["To"])
            print(part["Content-Transfer-Encoding"])    #base64
            print(part["Received"])
            filename = part.get_filename()
            if filename:
                print(filename)
                # Нам плохого не надо, в письме может быть всякое барахло
                with open(part.get_filename(), 'wb') as new_file:
                    new_file.write(part.get_payload(decode=True))

            #Первый способ декодтроавания тела сообщения
            if part["Content-Transfer-Encoding"] == "base64":
                print("Variant 1:   ", base64.b64decode(play_load).decode("UTF-8"))

            #Второй способ декодирования ела сообщения (Более правильный)
            print("Variant 2:   ", part.get_payload(decode=True))

            with open(str(num), 'wb') as new_file:
                new_file.write(part.get_payload(decode=True))

    connection.close()
    connection.logout()

if __name__ == '__main__':
    read_email_2()