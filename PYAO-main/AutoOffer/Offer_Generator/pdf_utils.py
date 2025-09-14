from PyPDF2 import PdfFileReader, PdfFileWriter
import re
from PyPDF2.generic import NameObject
from datetime import datetime, timedelta
import logging
from AutoOffer.Offer_Generator import pdf_statics

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def remove_non_numeric(input_string):
    """
    Removes all non-numeric characters from a string.
    
    Args:
        input_string: The string to process
        
    Returns:
        A string containing only numeric characters (0-9)
    """
    # This regex pattern matches any character that is NOT a digit (0-9)
    pattern = r'[^0-9]+'

    # Substitute all matched characters with an empty string
    cleaned_string = re.sub(pattern, '', str(input_string))
    
    return cleaned_string

def generate_closing_date(days_to_close=14):
    # Get today's date
    today = datetime.now()

    # Calculate the date 2 weeks from today
    closing_date = today + timedelta(days=days_to_close)

    # Check if it falls on a Saturday or Sunday
    if closing_date.weekday() >= 5:  # 5 is Saturday, 6 is Sunday
        # If it's a Saturday or Sunday, add the necessary days to get to Monday
        days_until_monday = 7 - closing_date.weekday()
        closing_date += timedelta(days=days_until_monday)

    # Format the result as a string
    closing_date_string = closing_date.strftime("%m/%d/%Y")
    return(closing_date_string)

text_fields = pdf_statics.TextFields()
box_fields = pdf_statics.CheckBoxes()

def updateCheckboxValues(page, fields):
    for annot in page['/Annots']:
        writer_annot = annot.get_object()  # Dereference IndirectObject
        
        if writer_annot.get('/FT') == '/Btn':  # Check if it's a button (checkbox)
            field_name = writer_annot.get('/T')
            
            if field_name in fields and fields[field_name]:  # Check if this field needs to be updated and the field value is "Yes"
                # Dereference the '/AP' object if it exists
                print(f"Found button: {field_name}")
                if '/AP' in writer_annot:
                    ap_dict = writer_annot['/AP'].get_object()
                    
                    # Dereference the '/N' object within '/AP'
                    if '/N' in ap_dict:
                        appearance_dict = ap_dict['/N'].get_object()
                        
                        # Extract the first key as the export value
                        keys_list = list(appearance_dict.keys())
                        print(f"Keys list: {keys_list}")

                        # Check if the first key contains "Off", if so, use the second key
                        export_value = keys_list[0] if keys_list and "Off" not in keys_list[0] else (keys_list[1] if len(keys_list) > 1 else None)
                        print(f"Export value for {field_name} is: {export_value}. The choices are {appearance_dict}")
                        
                        if export_value:
                            # Update the checkbox value dynamically using the export value
                            writer_annot.update({
                                NameObject("/V"): NameObject(export_value),
                                NameObject("/AS"): NameObject(export_value)
                            })
                            
                            # Verify the update was successful
                            actual_value = writer_annot.get('/V')
                            actual_state = writer_annot.get('/AS')
                            
                            if actual_value == export_value and actual_state == export_value:
                                logging.info(f"Successfully updated checkbox {field_name}: Value={actual_value}, State={actual_state}")
                                buttons_updated = True
                            else:
                                logging.error(f"Failed to update checkbox {field_name}")
                                logging.error(f"Expected: Value={export_value}, State={export_value}")
                                logging.error(f"Actual: Value={actual_value}, State={actual_state}")

def check_filled_fields(pdf_path, pdf_data):
    reader = PdfFileReader(pdf_path)

    for page in reader.pages:
        if '/Annots' in page:
            for annot in page['/Annots']:
                try:
                    annot_object = annot.getObject()
                    if '/T' in annot_object:
                        field_name = annot_object['/T']
                        field_value = annot_object.get('/V')
                        if field_name in pdf_data:
                            expected_value = pdf_data[field_name]
                            # print(f"Field: {field_name}, Expected: {expected_value}, Found: {field_value}")
                            if str(field_value) != str(expected_value):
                                print(f"Warning: Field '{field_name}' does not have the expected value!")
                                return False
                except Exception as e:
                    print(f"Error processing annotation: {e}")

    return True

def fill_pdf(input_pdf_path, output_pdf_path, pdf_data_dict):

    reader = PdfFileReader(input_pdf_path)
    writer = PdfFileWriter()

    # Filling the fields
    for pageNum in range(reader.numPages):
        page = reader.pages[pageNum]
        writer.addPage(page)
        try:
            updateCheckboxValues(page, pdf_data_dict)
            writer.updatePageFormFieldValues(page, pdf_data_dict)
        except KeyError as e:
            print(f"No fields on page {pageNum}")
            # print(e)

    with open(output_pdf_path, 'wb') as output_pdf_file:
        writer.write(output_pdf_file)

    return check_filled_fields(output_pdf_path, pdf_data_dict)

def has_non_empty_string_or_true(tuple):
    return any(x and (isinstance(x, str) and x.strip() != "" or x is True) for x in tuple)

def convert_str_2_float(input_string):
    # This regex pattern will match any character that is NOT a digit or a period
    pattern = r'[^\d.]+'
    # Substitute all matched characters with an empty string
    cleaned_string = re.sub(pattern, '', input_string)
    return float(cleaned_string)
