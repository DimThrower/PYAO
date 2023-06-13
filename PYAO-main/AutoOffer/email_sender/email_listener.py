import imaplib
import email
import socket

# IMAP server settings
IMAP_SERVER = 'imap.gmail.com'
IMAP_PORT = 993
EMAIL_ADDRESS = 'charles@rightwayhomesolutions.com'
EMAIL_PASSWORD = 'qhnvhdipzcdchirg'
FOLDER_NAME = 'Test'  # Specify the name of the folder you want to access

# Socket settings
SOCKET_SERVER_ADDRESS = ('localhost', 5000)  # Replace with the appropriate server address

def process_email(msg):
    # Extract relevant data from the email
    email_data = extract_data(msg)
    # print(email_data)

    # Create a socket connection
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect(SOCKET_SERVER_ADDRESS)

        # Send the email data to the other program
        client_socket.sendall(email_data.encode())

def extract_data(msg):
    # Extract the desired data from the email message
    # Modify this function to extract the relevant data based on your requirements
    subject = msg['Subject']
    sender = msg['From']
    body = ''

    if msg.is_multipart():
        for part in msg.get_payload():
            if part.get_content_type() == 'text/plain':
                body = part.get_payload(decode=True).decode('utf-8')
                break
    else:
        body = msg.get_payload(decode=True).decode('utf-8')

    # Return the extracted data as a string
    return f'Subject: {subject}\nFrom: {sender}\nBody: {body}'

def main():
    # Connect to the IMAP server
    mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
    mail.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

    # Select the folder
    mail.select(FOLDER_NAME)

    # Search for unread email messages in the folder
    result, data = mail.search(None, 'ALL')
    if result == 'OK':
        email_ids = data[0].split()
        for email_id in email_ids:
            # Fetch the email data
            result, msg_data = mail.fetch(email_id, '(RFC822)')
            if result == 'OK':
                raw_email = msg_data[0][1]
                # Parse the raw email data
                msg = email.message_from_bytes(raw_email)
                print(msg)
                # Process the email
                process_email(msg)

    # Disconnect from the server
    mail.logout()

if __name__ == '__main__':
    main()
