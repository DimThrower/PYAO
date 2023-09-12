import sqlite3, os
import mysql.connector
from AutoOffer.html_manipulation.HTML import PropertyProfile 
from AutoOffer import settings 

# Create an instance of PropertyProfile

def create_db():
    db_host = settings.db_host
    db_user = settings.db_user
    db_password = settings.db_password
    db_name = settings.db_name

    # Establish connection to MySQL server
    connection = mysql.connector.connect(
        host = db_host,
        user = db_user,
        password = db_password
    )

    # Create a cursor object
    cursor = connection.cursor()

    # Check if the database exists
    cursor.execute(f"SHOW DATABASES LIKE '{db_name}'")
    database_exists = cursor.fetchone()

    if not database_exists:
        # Create the database
        cursor.execute(f"CREATE DATABASE {db_name}")
    else:
        print(F'DB already created: {db_name}')

    # Close the cursor and reconnect to the database
    cursor.close()
    connection = mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_name
    )

    # Create a new cursor
    cursor = connection.cursor()


    # Create the property table
    pp = PropertyProfile()

    cursor.execute(f'''CREATE TABLE IF NOT EXISTS property (
                        {pp.mls_id} INT PRIMARY KEY,
                        {pp.steet_address} VARCHAR(255),
                        {pp.city} VARCHAR(255),
                        {pp.zip_Code} VARCHAR(255),
                        {pp.state} VARCHAR(255),
                        {pp.county} VARCHAR(255),
                        {pp.list_price} VARCHAR(255),
                        {pp.dom} VARCHAR(255),
                        {pp.agent_first_name} VARCHAR(255),
                        {pp.agent_last_name} VARCHAR(255),
                        {pp.agent_email} VARCHAR(255),
                        {pp.agent_cell} VARCHAR(255),
                        {pp.agent_phone} VARCHAR(255),
                        {pp.hoa} VARCHAR(255),
                        {pp.owner_name} VARCHAR(255),
                        {pp.year_built} VARCHAR(255),
                        {pp.bed} VARCHAR(255),
                        {pp.bath} VARCHAR(255),
                        {pp.half_bath} VARCHAR(255),
                        {pp.sqft} VARCHAR(255),
                        {pp.lot} VARCHAR(255),
                        {pp.block} VARCHAR(255),
                        {pp.mud} VARCHAR(255),
                        {pp.arv} VARCHAR(255),
                        {pp.repair} INT,
                        {pp.offer_price} INT,
                        {pp.em} INT,
                        {pp.om} INT,
                        {pp.option_days} INT,
                        {pp.close_date} VARCHAR(255),
                        {pp.subdivision} VARCHAR(255),
                        {pp.legal_description} VARCHAR(255),
                        {pp.lead_based_paint} VARCHAR(255),
                        {pp.escrow_agent} VARCHAR(255),
                        {pp.title_company_name} VARCHAR(255),
                        {pp.title_company_address} VARCHAR(255),
                        {pp.confidence_score} VARCHAR(255),
                        {pp.forcast_sd} VARCHAR(255),
                        {pp.confidence_score_tolerance_lvl} VARCHAR(255),
                        {pp.offer_sent} VARCHAR(255),
                        {pp.ghl_check} VARCHAR(255),
                        {pp.deal_taken} VARCHAR(255),
                        {pp.pdf_offer_path} VARCHAR(255),
                        {pp.last_updated} TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )''')

    # Commit the changes
    connection.commit()

    # Close the connection
    connection.close()

create_db()