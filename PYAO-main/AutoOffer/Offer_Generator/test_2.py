import os
import pdfrw

from AutoOffer import settings
import HTML_TREC

html_fields = HTML_TREC.TextFields()

ANNOT_KEY = '/Annots'
ANNOT_FIELD_KEY = '/T'
SUBTYPE_KEY = '/Subtype'
WIDGET_SUBTYPE_KEY = '/Widget'

def write_fillable_pdf(input_pdf_path, output_pdf_path, data_dict):
    template_pdf = pdfrw.PdfReader(input_pdf_path)
    annotations = template_pdf.pages[0][ANNOT_KEY]

    for annotation in annotations:
        if annotation[SUBTYPE_KEY] == WIDGET_SUBTYPE_KEY and annotation[ANNOT_FIELD_KEY]:
            key = annotation[ANNOT_FIELD_KEY][1:-1]  # Remove parentheses
            if key in data_dict.keys():
                annotation.update(
                    pdfrw.PdfDict(V='{}'.format(data_dict[key]))
                )

    pdfrw.PdfWriter().write(output_pdf_path, template_pdf)

data_to_fill = {
    html_fields.seller: 'Test Seller',
    html_fields.buyer: 'Test Buyer',
    # Add more fields as needed
}

output_pdf_path = os.path.join(str(settings.filled_TREC_file_path_HOU), 'Test.pdf')

# write_fillable_pdf(settings.blank_TREC_file_path, output_pdf_path, data_to_fill)

from PyPDF2 import PdfFileReader
import os

def inspect_checkboxes(pdf_path):
    reader = PdfFileReader(open(pdf_path, 'rb'))
    for page in reader.pages:
        if '/Annots' in page:
            for annot in page['/Annots']:
                annot_object = annot.getObject()
                if annot_object.get('/FT') == '/Btn':  # Button field (checkbox/radio)
                    field_name = annot_object.get('/T')[1:-1]  # Field name
                    appearance_dict = annot_object.get('/AP')
                    if appearance_dict and '/N' in appearance_dict:
                        normal_appearances = appearance_dict['/N']
                        print(f"Field: {field_name}, Possible Values: {list(normal_appearances.keys())}")

pdf_path = 'path_to_your_pdf.pdf'  # Replace with your PDF file path
inspect_checkboxes(settings.blank_TREC_file_path)
