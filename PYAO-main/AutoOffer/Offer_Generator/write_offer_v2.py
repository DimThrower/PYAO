from PyPDF2 import PdfFileReader, PdfFileWriter
from AutoOffer import settings
import os
import HTML_TREC
from PyPDF2.generic import NameObject

text_fields = HTML_TREC.TextFields()
box_fields = HTML_TREC.CheckBoxes()

def updateCheckboxValues(page, fields):
    for j in range(0, len(page['/Annots'])):
        writer_annot = page['/Annots'][j].getObject()
        for field in fields:
            if writer_annot.get('/FT') == '/Btn':  # Check if it's a button field
                if writer_annot.get('/T') == field:
                    # print(field)
                    writer_annot.update({
                        NameObject("/V"): NameObject(fields[field]),
                        NameObject("/AS"): NameObject(fields[field])
                    })


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



# data_to_fill = {
#     text_fields.seller: 'Test Sgggeller',
#     text_fields.buyer: 'Test Buyer',
#     box_fields.buyer_pay_title_policy: '/On',
#     # Add more fields as needed
# }

# # Specify your input and output file paths
# input_pdf_path = settings.blank_TREC_file_path
# output_pdf_path = os.path.join(settings.filled_TREC_file_path_HOU, 'Test.pdf')

# print(fill_pdf(input_pdf_path, output_pdf_path, pdf_data_dict=data_to_fill))

