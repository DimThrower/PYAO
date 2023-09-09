from dotenv import load_dotenv
import os
from datetime import datetime, time



def load_env_var():
    load_dotenv(r'C:\Script\PYAO-main\AutoOffer\PYAO.env')

load_env_var()

chromeDrivePath = r'C:\Script\PYAO-main\chromedriver.exe'
firefoxDrivePath = r'C:\Program Files\Mozilla Firefox\firefox.exe'
blank_TREC_file_path = r'file://C:/Script/PYAO-main/Contracts/Blank 1-4 Trec Contract.pdf'
filled_TREC_file_path_HOU = r'C:\Script\PYAO-main\Contracts\HOU'
filled_TREC_file_path_SA = r'C:\Script\PYAO-main\Contracts\SA'

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
GHL_HOU_API_KEY = os.getenv('GHL_HOU_API')
GHL_SA_API_KEY = os.getenv('GHL_SA_API')

db_host = 'localhost'
db_user = 'root'
db_password = os.getenv('DB_PASSWORD')
db_name = 'auto_offer'
db_table_name = 'property'

offer_start_hour = 7
offer_end_hour = 21
short_wait = 3.0 # seconds
long_wait = 4.5 # seconds
avg_wait = (short_wait+long_wait)/2
max_offers = (offer_end_hour-offer_start_hour)*60/avg_wait*0.70


