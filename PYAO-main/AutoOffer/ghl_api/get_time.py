from datetime import datetime, timedelta

def get_time(days_back):
# Get the current date and time
    current_date = datetime.utcnow()

    # Calculate the date 45 days before today
    past_date = current_date - timedelta(days_back)

    # Format the past date in ISO 8601 format
    formatted_date = past_date.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    # Convert the string to a datetime object
    datetime_obj = datetime.strptime(formatted_date, '%Y-%m-%dT%H:%M:%S.%fZ')

    #print(formatted_date)
    return(datetime_obj)