from dotenv import load_dotenv
import os
from datetime import datetime, time


# Get the full path of the current file
full_path = os.path.abspath(__file__)
# print("Full path:", full_path)

# Truncate the path to two folders up
PYAO_path = os.path.dirname(os.path.dirname(full_path))
# print("Two folders up:", PYAO_path)

def load_env_var():
    load_dotenv(os.path.join(PYAO_path,'AutoOffer\PYAO.env'))
    # load_dotenv(r'C:\Script\PYAO-main\AutoOffer\PYAO.env')

load_env_var()

# chromeDrivePath = r'C:\Script\PYAO-main\chromedriver.exe'
# firefoxDrivePath = r'C:\Program Files\Mozilla Firefox\firefox.exe'
# blank_TREC_file_path = r'file://C:/Script/PYAO-main/Contracts/Blank 1-4 Trec Contract.pdf'
# filled_TREC_file_path_HOU = r'C:\Script\PYAO-main\Contracts\HOU'
# filled_TREC_file_path_SA = r'C:\Script\PYAO-main\Contracts\SA'

chromeDrivePath = os.path.join(PYAO_path, 'chromedriver.exe')
firefoxDrivePath = r'C:\Program Files\Mozilla Firefox\firefox.exe'
blank_TREC_file_path = os.path.join(PYAO_path,'Contracts/Signed 1-4 Trec Contract with POF.pdf')
# blank_TREC_file_path = blank_TREC_file_path#fr'file://{blank_TREC_file_path}'
filled_TREC_file_path_HOU = os.path.join(PYAO_path,'Contracts\HOU')
scrape_error_log_path = os.path.join(PYAO_path, "scrape_error_log.txt")
# filled_TREC_file_path_SA = os.path.join(PYAO_path,'Contracts\SA')

IMAP_SERVER = 'imap.gmail.com'
IMAP_PORT = 993
EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
EMAIL_ADDRESS_2 = os.getenv('EMAIL_ADDRESS_2')
EMAIL_PASSWORD_2 = os.getenv('EMAIL_PASSWORD_2')
FROM_EMAIL_ADDRESS = os.getenv("FROM_EMAIL_ADDRESS")
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
max_offers = 10 # (offer_end_hour-offer_start_hour)*60/avg_wait*0.70

#*out of state,!*new,!*renovated,*no FHA,*repair* ne,*fire dama,*inherit,*value add,*probate,*estate,*tear down,*bring all,*must sale,*outdated,*eeds work,*distress,*tlc,*handy man,*ash onl,*invest,*fixer-upper,*as-is,*as is,*motivat,*all offer,*needs update,*lank canvas,!*auction,!*hud


