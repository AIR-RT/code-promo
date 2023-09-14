import csv
import string
import random
import smtplib

# here you put the file name of HelloAsso
csv_db = 'adhesion-assoname-2023-2024.csv' 

# this will be the name of the file you will be refering then, because it will display mail and code side to side
# then you will add the code to HelloAsso using the dashboard
csv_save = 'code-promo-event.csv' 

# bulk var to save data + gen code
data = [["email","code"]]
data.append(['',''])
i=0
MailList ={}
CodeList ={}
email = []
RandCode = ""
size=10
chars=string.ascii_uppercase + string.digits



# serveur 
sender_email = "mail" # the e-mail that will send the message
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
# Email configuration
# SMTP server configuration
smtp_server = 'smtp.univ-nantes.fr'  # SMTP SERVER just do a quick google search to find it
smtp_port = 465  # Port for TLS (465 for univ nantes 587 for Gmail)
smtp_username = 'xxxxx' # 95% of time this is the sender_email
smtp_password = 'PASS'  # the pass of the sender e-mail




try:
    with open(csv_db, mode='r', newline='') as file:
        csv_reader = csv.reader(file, delimiter=';') # might be another delimiter if not using default HelloAsso files
        # Skip the header row (first line)
        next(csv_reader)
        # get all the e-mail from the user and then store them in a file so you can review it
        for line_number, row in enumerate(csv_reader, start=2):  # Start line numbering from 2
                email = row[1] # get the e-mail
                RandCode = ''.join(random.choice(chars) for _ in range(size)) # gen the code
                MailList[i]=email # second time storing e-mail
                CodeList[i]=RandCode # second time storing the code
                i+=1 # increment the loop to update the pointer
# error gestion
except FileNotFoundError:
    print(f"File '{csv_db}' not found.")
except Exception as e:
    print(f"An error occurred while searching for the file: {str(e)}")

try:
    message = MIMEMultipart() # Create the email message
    for index in range(0, len(MailList)): # for each e-mail we found 

        receiver_email = MailList[index]
        subject = 'This is a random code sent for test (python script)' # just rand subject
        message_text = f'This is the code number {index}, this is the randcode: {CodeList[index]}' # just rand message

        message['From'] = sender_email
        message['To'] = receiver_email
        message['Subject'] = subject
        # Attach the email body (plain text)
        message.attach(MIMEText(message_text, 'plain'))

        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)
        
        server.sendmail(sender_email, receiver_email, message.as_string())
        print('Email sent successfully!') # one prompt for each e-mail
        data.append([receiver_email,RandCode]) # store both e-mail and code to then print them in the file
        server.quit() # we disconnect
        # please note that if we don't disconnect and just kept the connexion while we are sending all the mail
        # we could expect to be faster, but this isn't that important in our case.

except Exception as e:
    print(f'Error: {str(e)}')

try:
    with open(csv_save, mode='w', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerows(data) # we write data for the user we sent a e-mail to in the specified file.
        # then you will need to put all the code to HelloAsso

except Exception as e:
     print(f"An error occurred while storing the data: {str(e)}")