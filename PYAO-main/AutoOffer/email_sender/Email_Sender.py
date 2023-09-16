import smtplib
import socket
import os, schedule, time, random
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
from AutoOffer import settings
from AutoOffer.html_manipulation import HTML
from AutoOffer.db import db_funct
from Signatures import Signatures
import datetime
from AutoOffer.misc import line
from AutoOffer.ghl_api.update import opp_update
from AutoOffer.ghl_api.mapping import create_custom_fields_map, create_stage_map, create_users_map
from AutoOffer.ghl_api.api_key_picker import ghl_api

# Create Property profile instance
pp = HTML.PropertyProfile()

# Create Signatures instance
sig = Signatures()

db_funct.create_db()

def create_message_with_attachment(sender, to, subject, body, attachment_path, signature_html):
    message = MIMEMultipart()
    message['From'] = sender
    message['To'] = to
    message['Subject'] = subject

    # Attach the body to the email
    message.attach(MIMEText(body))

    # Attach the signature to the email
    message.attach(MIMEText(signature_html, 'html'))

    # Attach the offer file to the email
    with open(attachment_path, 'rb') as attachment_file:
        attachment = MIMEBase('application', 'octet-stream')
        attachment.set_payload(attachment_file.read())
        encoders.encode_base64(attachment)
        # Making the Name of the Attached file to the base name of the file
        attachment.add_header('Content-Disposition', 'attachment', filename=os.path.basename(attachment_path))
        message.attach(attachment)

    return message.as_string()

def send_scheduled_email(server, sender, to, message, prop):
    try:
        server.sendmail(sender, to, message)
        print("Email sent successfully!")
        
        # Update the  Offer_Sent column to show offer ws sent
        db_funct.multi_db_update(
            mls_id=prop[pp.mls_id],
            data_dict={pp.offer_sent: datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')},
            overwrite=True
        )
 
        # Switch the the deal to offer made
        api_key = ghl_api(location=prop[pp.location])
        print(api_key)
        users = create_users_map(token=ghl_api)
        pipeline_id, stages = create_stage_map(token=api_key)
        opp_update(token=api_key, street_address=prop[pp.steet_address], days_back=45, stage_id=stages.get("1stOfferMade/FollowUp"), pipeline_id=pipeline_id)

    except PermissionError as e:
        print("An error occurred while sending the email: {}".format(e))

def bulk_email(**kwargs):
    sender = settings.EMAIL_ADDRESS
    to = kwargs['to_email']
    subject = kwargs['subject']
    body = kwargs['body']
    attachment_path = kwargs['offer_path']
    signature_html = kwargs['signature_html']

    print(f'Body: {body}')
    # Connect to the SMTP server 
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_username = settings.EMAIL_ADDRESS
    smtp_password = settings.EMAIL_PASSWORD

    try:
        smtp_conn = smtplib.SMTP(smtp_server, smtp_port)
        smtp_conn.starttls()
        smtp_conn.login(smtp_username, smtp_password)
    except (smtplib.SMTPException, socket.gaierror) as e:
        print("Failed to connect to the SMTP server: {}".format(e))
        return

    # Create the body message and add the attachment
    message = create_message_with_attachment(sender, to, subject, body, attachment_path, signature_html)

    # Send the scheduled email
    send_scheduled_email(smtp_conn, sender, to, message, prop=kwargs['prop'])

    # Disconnect from the SMTP server
    smtp_conn.quit()

def main():
        # Create a db if there isn't one
        db_funct.create_db()

        # Define how many properties to send in one session
        props_per_sesh = 10

        # Define session time interaval in minutes
        # sesh_time = 30*60

        # Find all the properties that need offer sent on them by checking if the Offer_Sent field in NULL
        props = db_funct.get_sorted_rows_with_null_and_not_null(sort_column=pp.last_updated, 
                                                                null_list=[pp.offer_sent],
                                                                not_null_list=[pp.email_body,
                                                                            pp.pdf_offer_path,])

        # print(f'Properties to send offer on {props}')

        if props:
            # Only send 10 then wait 30 minutes to send the anothe batch of 10
            props = props[:props_per_sesh]

            # Iterate over all the properties
            for prop in props:
                # print(prop)

                # Check if in acceptable time range
                current_time = datetime.datetime.now().time()
                start_time = datetime.time(hour=settings.offer_start_hour, minute=0)  # 7:00 AM
                end_time = datetime.time(hour=settings.offer_end_hour, minute=0)   # 9:00 PM

                if start_time <= current_time <= end_time:
                    pass
                else:
                    print(f'({line()}) Out side of run time. Waiting for scheduled r')
                    break

                # Select the Houston signature
                if prop[pp.location] == "HOU":
                    signature = sig.hou_signature

                # Select the San Antonio signature
                if prop[pp.location] == "SA":
                    signature = sig.sa_signature

                bulk_email(
                    to_email = prop[pp.agent_email],
                    subject = f"Cash Offer for {prop[pp.steet_address]}",
                    body = prop[pp.email_body],
                    offer_path = prop[pp.pdf_offer_path],
                    prop = prop,
                    signature_html = signature,
                    )
                
                # Make random wait time in minutes
                wait_time = random.uniform(3.0, 4.5) * 60 

                # Get the current time
                current_time = time.time()

                # Add the wait_time in seconds to the current time
                future_time = current_time + wait_time

                # Convert the future_time to a human-readable format with abbreviated month, date, and time
                future_time_formatted = time.strftime('%b %d, %Y %I:%M:%S %p', time.localtime(future_time))

                # Print the formatted time
                print(f"Future time after adding wait time: {future_time_formatted}")

                time.sleep(wait_time)
        else:
            print(f'({line()}) No properties to send offer on. Wait for the next schedule')

def job():
    current_time = datetime.datetime.now().time()
    start_time = datetime.time(hour=settings.offer_start_hour, minute=0)  # 7:00 AM
    end_time =  datetime.time(hour=settings.offer_end_hour, minute=0)  # 9:00 PM

    if start_time <= current_time <= end_time:
        main()
    else:
        print(f'({line()}) Out side of run time')

if __name__ == '__main__':

    job()

    # This will run the code as soon as it's starting rather than waiting
    schedule.every(3).minutes.do(job)

    while True:
        schedule.run_pending()
        time.sleep(1)


       
