import mysql.connector
from AutoOffer import settings
import aiomysql
import asyncio, functools

from AutoOffer.html_manipulation.HTML import PropertyProfile

# Create an instance of PropertyProfile
pp = PropertyProfile()

import mysql.connector
from AutoOffer.html_manipulation.HTML import PropertyProfile 
from AutoOffer import settings 

# Create database
def create_db():
    # Load environment variables
    settings.load_env_var()

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

    # Close the cursor and reconnect to the database
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
                        {pp.public_remarks} VARCHAR(1500),
                        {pp.ghl_check} DATETIME,
                        {pp.deal_taken} VARCHAR(255),
                        {pp.pdf_offer_path} VARCHAR(255),
                        {pp.email_body} VARCHAR(3000),
                        {pp.ai_cost} float4,
                        {pp.offer_sent} DATETIME,
                        {pp.ghl_offer_made} DATETIME,
                        {pp.last_updated} TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )''')

    # Close cursor
    cursor.close()

    # Commit the changes
    connection.commit()

    # Close the connection
    connection.close()

def connect_to_database(func):
    def wrapper(*args, **kwargs):
        # Connect to the database
        conn = mysql.connector.connect(
            host=settings.db_host,
            user=settings.db_user,
            password=settings.db_password,
            database=settings.db_name
        )
        cursor = conn.cursor()

        # Call the wrapped function
        result = func(cursor, *args, **kwargs)

        # This is here so when changes aren't made to the db the commit doesn't cause an error
        try:
            # Commit to what every changes are made
            conn.commit()
        except mysql.connector.errors.InternalError:
            pass
        # Close the database connection
        conn.close()

        return result
    return wrapper

# Get all the db title and puts them into a list
@connect_to_database
def get_column_names(cursor, table_name=settings.db_table_name):
    cursor.execute(f"SELECT * FROM {table_name} LIMIT 0")
    columns = [column[0] for column in cursor.description]
    return columns

# Inputs done piece of data into the column
@connect_to_database
def one_db_update(cursor, mls_id, column_name, data, table_name=settings.db_table_name):
    # Check if the mls_id exists
    cursor.execute(f"SELECT * FROM {table_name} WHERE mls_id = {mls_id}")
    result = cursor.fetchone()

    if result:
        # Update the existing row with the new data
        cursor.execute(f"UPDATE {table_name} SET {column_name} = %s WHERE mls_id = {mls_id}", (data,))

    else:
        # Insert a new row with the mls_id and data
        cursor.execute(f"INSERT INTO {table_name} (mls_id, {column_name}) VALUES ({mls_id}, %s)", (data,))

# Input multiple pieces of data into the db
@connect_to_database
def multi_db_update(cursor, mls_id, data_dict, overwrite=False, table_name=settings.db_table_name):
    # Check if the mls_id exists
    cursor.execute(f"SELECT * FROM {table_name} WHERE mls_id = {mls_id}")
    result = cursor.fetchone()

    if result:
        if overwrite:
            # Update the existing row with the new data
            query = f"UPDATE {table_name} SET "
            query += ", ".join([f"{column} = %s" for column in data_dict.keys()])
            query += f" WHERE mls_id = {mls_id}"
            cursor.execute(query, tuple(data_dict.values()))
            print(query)
        else:
            print(f"Entry with mls_id {mls_id} already exists. Skipping update.")
    else:
        # Insert a new row with the mls_id and data
        columns = ','.join(data_dict.keys())
        values = ','.join(['%s'] * len(data_dict))
        query = f"INSERT INTO {table_name} (mls_id, {columns}) VALUES ({mls_id}, {values})"
        cursor.execute(query, tuple(data_dict.values()))
        print(query)

# Will get the first column of a sort
@connect_to_database
def get_sorted_row_with_null(cursor, sort_column, null_column, table_name=settings.db_table_name):
    # Construct the SQL query to retrieve the first row with null value in the specified column
    query = f"SELECT * FROM {table_name} WHERE {null_column} IS NULL ORDER BY {sort_column} ASC LIMIT 1"
    cursor.execute(query)
    
    # Fetch the first row from the result
    row = cursor.fetchone()

    if row:
        # Get the column names
        column_names = [column[0] for column in cursor.description]

        # Create a dictionary with column names as keys and row data as values
        row_dict = dict(zip(column_names, row))

        return row_dict
    else:
        return None

# Will get the collection of sorted rows, that have a certain column set to null,
# and another comlun set to a specified value
@connect_to_database
def get_sorted_rows_with_values_and_null(cursor, sort_column, null_column, value_dict, table_name=settings.db_table_name):
    # Construct the SQL query to retrieve the first row with specific values in the specified columns
    query = f"SELECT * FROM {table_name} WHERE {null_column} IS NULL AND "
    conditions = []

    for column, value in value_dict.items():
        conditions.append(f"{column} = %s")

    query += " AND ".join(conditions)
    query += f" ORDER BY {sort_column} ASC"
    # print(query)

    cursor.execute(query, tuple(value_dict.values()))

    # Fetch the first row from the result
    rows = cursor.fetchall()
    # print(rows)
    if rows:
        # Get the column names
        column_names = [column[0] for column in cursor.description]
        # print(column_names)

        # Create a list of dictionaries, where each dictionary represents a row with column names as keys and row data as values
        result = []
        try:
            print(f'Number of results from DB are {len(rows)}')
            for row in rows:
                row_dict = dict(zip(column_names, row))
                result.append(row_dict)
        # Handle id rows only have one properties, help to prvent the TypeError
        except TypeError:
            print(f'Number of results from DB is 1')
            row_dict = dict(zip(column_names, rows))
            result.append(row_dict)

        return result
    else:
        return None

@connect_to_database
def get_sorted_rows_with_null_and_not_null(cursor, sort_column, null_list=None, not_null_list=None, table_name=settings.db_table_name):
    # Construct the SQL query to retrieve the first row with null value in the specified column
    query = f"SELECT * FROM {table_name} WHERE"

    # Check to see if null_list exist
    if null_list:
        # Interate through entire list
        for index, column in enumerate(null_list):
            # Check to see if 'AND' is already in, to ensure query doesn't error
            if ('AND' not in query) and ('WHERE ' not in query) and index == 0:
                query += (f" {column} IS NULL")
            else:
                query += (f" AND {column} IS NULL")

    # Check to see if not_null_list exist
    if not_null_list:
        # Interate through entire list
        for index, column in enumerate(not_null_list):
            # Check to see if 'AND' is already in, to ensure query doesn't error
            if ('AND' not in query) and ('WHERE ' not in query) and index == 0:
                query += (f" {column} IS NOT NULL")
            else:
                query += (f" AND {column} IS NOT NULL")

    query += f" ORDER BY {sort_column} ASC"
    print(query)

    cursor.execute(query)
    
    # Fetch the first row from the result
    rows = cursor.fetchall()

    if rows:
        # Get the column names
        column_names = [column[0] for column in cursor.description]

        # Create a list of dictionaries, where each dictionary represents a row with column names as keys and row data as values
        result = []
        try:
            print(f'Number of results from DB are {len(rows)}')
            for row in rows:
                row_dict = dict(zip(column_names, row))
                result.append(row_dict)
        # Handle id rows only have one properties, help to prvent the TypeError
        except TypeError:
            print(f'Number of results from DB is 1')
            row_dict = dict(zip(column_names, rows))
            result.append(row_dict)

        return result
    else:
        return None
    
# Will get all the rows of a sort
# @connect_to_database
def get_all_sorted_with_null(cursor, sort_column, null_column, table_name=settings.db_table_name):
    # Construct the SQL query to retrieve all rows with null value in the specified column
    query = f"SELECT * FROM {table_name} WHERE {null_column} IS NULL ORDER BY {sort_column} ASC"
    cursor.execute(query)
    
    # Fetch all rows from the result
    rows = cursor.fetchall()

    if rows:
        # Get the column names
        column_names = [column[0] for column in cursor.description]

        result = []
        # Create a list of dictionaries, where each dictionary represents a row with column names as keys and row data as values
        try:
            for row in rows:
                row_dict = dict(zip(column_names, row))
                result.append(row_dict)
        # Handle id rows only have one properties, help to prvent the TypeError
        except TypeError:
            row_dict = dict(zip(column_names, rows))
            result.append(row_dict)

        return result
    else:
        return None

# Will sort, and pull a specified number or rows from a specified column
@connect_to_database  
def fetch_sorted_rows(cursor, sort_column, column, num_of_rows='ALL', table_name=settings.db_table_name):
    # Establish a connection
    # Build the SQL query
    if num_of_rows == 'ALL':
        query = f"SELECT {column} FROM {table_name} ORDER BY {sort_column}"
    else:
        query = f"SELECT {column} FROM {table_name} ORDER BY {sort_column} LIMIT {num_of_rows}"

    # Execute the query
    cursor.execute(query)

    # Fetch the result rows into a list
    column_values = [row[0] for row in cursor]

    return column_values


# print(get_sorted_rows_with_null_and_not_null(
#     sort_column=pp.last_updated,
#     null_list=[
#         pp.offer_sent,
#         pp.email_made
#     ],
#     not_null_list=[
#         pp.pdf_offer_path,
#     ],
# ))
# print(fetch_sorted_rows(sort_column=pp.last_updated, column=pp.mls_id))

# print(get_all_sorted_with_null(sort_column=pp.last_updated, null_column=pp.ghl_check))

# print(get_sorted_row_with_null(sort_column=pp.last_updated, null_column=pp.ghl_check))


# multi_db_update(mls_id=1234, data_dict={pp.steet_address: '3 john street',
#                                  pp.list_price: '12345'})

# column_names = get_column_names()
# print(column_names)

"""
Async Code
"""

async def async_connect_to_database(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        # Connect to the database
        conn = await aiomysql.connect(
            host=settings.db_host,
            user=settings.db_user,
            password=settings.db_password,
            db=settings.db_name
        )
        cursor = await conn.cursor()

        # Call the wrapped function
        result = await func(cursor, *args, **kwargs)

        # This is here so when changes aren't made to the db the commit doesn't cause an error
        try:
            # Commit to whatever changes are made
            await conn.commit()
        except aiomysql.InternalError:
            pass

        # Close the database connection
        conn.close()
        await conn.wait_closed()

        return result

    return wrapper

# @async_connect_to_database
async def async_get_column_names(cursor, table_name=settings.db_table_name):
    await cursor.execute(f"SELECT * FROM {table_name} LIMIT 0")
    columns = [column[0] for column in cursor.description]
    return columns

# @async_connect_to_database
async def async_one_db_update(cursor, mls_id, column_name, data, table_name=settings.db_table_name):
    # Check if the mls_id exists
    await cursor.execute(f"SELECT * FROM {table_name} WHERE mls_id = {mls_id}")
    result = await cursor.fetchone()

    if result:
        # Update the existing row with the new data
        await cursor.execute(f"UPDATE {table_name} SET {column_name} = %s WHERE mls_id = {mls_id}", (data,))

    else:
        # Insert a new row with the mls_id and data
        await cursor.execute(f"INSERT INTO {table_name} (mls_id, {column_name}) VALUES ({mls_id}, %s)", (data,))

# @async_connect_to_database
async def async_multi_db_update(cursor, mls_id, data_dict, overwrite=False, table_name=settings.db_table_name):
    # Check if the mls_id exists
    await cursor.execute(f"SELECT * FROM {table_name} WHERE mls_id = {mls_id}")
    result = await cursor.fetchone()

    if result:
        if overwrite:
            # Update the existing row with the new data
            query = f"UPDATE {table_name} SET "
            query += ", ".join([f"{column} = %s" for column in data_dict.keys()])
            query += f" WHERE mls_id = {mls_id}"
            await cursor.execute(query, tuple(data_dict.values()))
            # print(query)
        else:
            print(f"Entry with mls_id {mls_id} already exists. Skipping update.")
    else:
        # Insert a new row with the mls_id and data
        columns = ','.join(data_dict.keys())
        values = ','.join(['%s'] * len(data_dict))
        query = f"INSERT INTO {table_name} (mls_id, {columns}) VALUES ({mls_id}, {values})"
        await cursor.execute(query, tuple(data_dict.values()))
        print(query)

# @async_connect_to_database
async def async_get_sorted_row_with_null(cursor, sort_column, null_column, table_name=settings.db_table_name):
    # Construct the SQL query to retrieve the first row with null value in the specified column
    query = f"SELECT * FROM {table_name} WHERE {null_column} IS NULL ORDER BY {sort_column} ASC LIMIT 1"
    await cursor.execute(query)
    
    # Fetch the first row from the result
    row = await cursor.fetchone()

    if row:
        # Get the column names
        column_names = [column[0] for column in cursor.description]

        # Create a dictionary with column names as keys and row data as values
        row_dict = dict(zip(column_names, row))

        return row_dict
    else:
        return None

# @async_connect_to_database
async def async_get_all_sorted_with_null(cursor, sort_column, null_column, table_name=settings.db_table_name):
    # Construct the SQL query to retrieve all rows with null value in the specified column
    query = f"SELECT * FROM {table_name} WHERE {null_column} IS NULL ORDER BY {sort_column} ASC"
    await cursor.execute(query)
    
    # Fetch all rows from the result
    rows = await cursor.fetchall()

    if rows:
        # Get the column names
        column_names = [column[0] for column in cursor.description]

        # Create a list of dictionaries, where each dictionary represents a row with column names as keys and row data as values
        result = []
        # Create a list of dictionaries, where each dictionary represents a row with column names as keys and row data as values
        try:
            for row in rows:
                row_dict = dict(zip(column_names, row))
                result.append(row_dict)
        # Handle id rows only have one properties, help to prvent the TypeError
        except TypeError:
            row_dict = dict(zip(column_names, rows))
            result.append(row_dict)

        return result
    else:
        return None

async def async_get_sorted_rows_with_null_and_not_null(cursor, sort_column, null_list=None, not_null_list=None, table_name=settings.db_table_name):
    # Construct the SQL query to retrieve the first row with null value in the specified column
    query = f"SELECT * FROM {table_name} WHERE"

    # Check to see if null_list exist
    if null_list:
        # Interate through entire list
        for index, column in enumerate(null_list):
            # Check to see if 'AND' is already in, to ensure query doesn't error
            if ('AND' not in query) and ('WHERE ' not in query) and index == 0:
                query += (f" {column} IS NULL")
            else:
                query += (f" AND {column} IS NULL")

    # Check to see if not_null_list exist
    if not_null_list:
        # Interate through entire list
        for index, column in enumerate(not_null_list):
            # Check to see if 'AND' is already in, to ensure query doesn't error
            if ('AND' not in query) and ('WHERE ' not in query) and index == 0:
                query += (f" {column} IS NOT NULL")
            else:
                query += (f" AND {column} IS NOT NULL")

    query += f" ORDER BY {sort_column} ASC"
    print(query)

    await cursor.execute(query)
    
    # Fetch the first row from the result
    rows = await cursor.fetchall()

    if rows:
        # Get the column names
        column_names = [column[0] for column in cursor.description]

        # Create a list of dictionaries, where each dictionary represents a row with column names as keys and row data as values
        result = []
        try:
            print(f'Number of results from DB are {len(rows)}')
            for row in rows:
                row_dict = dict(zip(column_names, row))
                result.append(row_dict)
        # Handle id rows only have one properties, help to prvent the TypeError
        except TypeError:
            print(f'Number of results from DB is 1')
            row_dict = dict(zip(column_names, rows))
            result.append(row_dict)

        return result
    else:
        return None
# conns = []  
# for _ in range(1,3):  
#     conn = mysql.connector.connect(
#         host=settings.db_host,
#         user=settings.db_user,
#         password=settings.db_password,
#         database=settings.db_name
#     )
#     conns.append(conn)

#     # Apend the cursor instance to the cursors list
# print(conns)

# print(get_all_sorted_with_null(cursor=conns[1].cursor(), sort_column=pp.last_updated, null_column=pp.pdf_offer_path, table_name=settings.db_table_name))