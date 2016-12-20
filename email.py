from participant import Participant
import socket
import sys
import time

connection = ""
buffer_size = ""

"""
    Error sending email so close down and clean up the connection.
"""


def die(error_message):
    global connection

    print(error_message)
    connection.close()
    sys.exit(1)


"""
    Sends a line of data to the email server, and collects the response code.
    If the response code is not what is expected, then crap out and kill the connection.
"""


def send_and_receive(data, expected_response):
    global connection
    global buffer_size

    send(data)

    received = connection.recv(buffer_size)
    code = int(received[:3])
    if code == expected_response:
        print("ok..")
    else:
        print("Error sending message: Code %s expecting %s data transmitted %s" %
              (str(code), str(expected_response), data))

    return


"""
    Short little wrapper method for sending data through the SMTP connection.
"""


def send(data):
    global connection
    if data != "":
        data += "\n"
        connection.send(bytes(data, 'UTF-8'))
        # print (data)

    return


def send_email_body(template):
    global connection

    # start with the Subject and From data
    send("To: " + template['to'])
    send("Subject: " + template['subject'])
    send("From: " + template['from_appearance'])

    time.sleep(1)
    # MIME header
    send("Mime-Version: 1.0;")
    send("Content-Type: text/html; charset=\"ISO-8859-1\";")
    send("Content-Transfer-Encoding: 7bit;")

    time.sleep(1)
    # message body - text version first
    send("<html>")
    send(template['html_component'] + "\n")
    send("</html>")

    return


"""
    Send a flippin email.

    Takes a Participant object, and the email address to send the email to.
"""


def send_email(participant, email):
    global connection
    global buffer_size

    email_template = dict()
    lines = (open(participant.template).readlines())
    email_template['from'] = lines[0].strip()
    email_template['from_appearance'] = lines[1].strip()
    email_template['subject'] = lines[2].strip()
    email_template['html_component'] = "".join(lines[3:])

    email_template['to'] = email

    # substitute in the variables into the HTML component
    email_template['html_component'] \
        = email_template['html_component'].replace("<UNI_ID>", str(participant.uid))
    email_template['html_component']\
        = email_template['html_component'].replace("<FIRST_NAME>", str(participant.first_name))
    email_template['html_component']\
        = email_template['html_component'].replace("<FULL_NAME>", str(participant.full_name))
    email_template['html_component']\
        = email_template['html_component'].replace("<USER_ID>", str(participant.anon_id))
    email_template['html_component'] \
        = email_template['html_component'].replace("<BATCH_ID>", str(1)) #todo this

    # set up the connection
    TCP_IP = '130.56.66.51'
    TCP_PORT = 25
    buffer_size = 1024

    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection.connect((TCP_IP, TCP_PORT))

    send_and_receive("", 220)
    send_and_receive("HELO anu.edu.au", 250)
    send_and_receive("MAIL FROM:" + email_template['from'], 250)
    send_and_receive("RCPT TO:" + email_template['to'], 250)
    send_and_receive("DATA", 354)

    send_email_body(email_template)

    send_and_receive(".", 250)
    send_and_receive("QUIT", 221)

    connection.close()

