from dotenv import load_dotenv
import os

def load_env_var():
    load_dotenv(r'C:\Script\PYAO-main\AutoOffer\PYAO.env')

load_env_var()

chromeDrivePath = r'C:\Script\PYAO-main\chromedriver.exe'
firefoxDrivePath = r'C:\Program Files\Mozilla Firefox\firefox.exe'
blank_TREC_file_path = r'file://C:/Script/PYAO-main/Contracts/Blank 1-4 Trec Contract.pdf'
filled_TREC_file_path = r'C:\Script\PYAO-main\Contracts'
IMAP_SERVER = 'imap.gmail.com'
IMAP_PORT = 993
EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
GHL_USERNAME = os.getenv('GHL_USERNAME')
GHL_PASSWORD = os.getenv('GHL_PASSWORD')
FOLDER_NAME = 'GHL_Security_Code'
HAR_USERNAME = os.getenv('HAR_username')
HAR_PASSWORD = os.getenv('HAR_PASSWORD')
OPENAI_API_KEY = os.getenv('OPENAI_KEY')
db_host = 'localhost'
db_user = 'root'
db_password = os.getenv('DB_PASSWORD')
db_name = 'auto_offer'
db_table_name = 'property'


