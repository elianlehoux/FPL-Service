import fitz
import io
from pypdf import PdfReader, PdfWriter

def test_flatten():
    # 1. Fill with pypdf
    reader = PdfReader('FPL_TEMPLATE.pdf')
    writer = PdfWriter()
    writer.append(reader)
    writer.update_page_form_field_values(writer.pages[0], {'Aircraft identification': 'LVABC'})
    
    # Needs appearances
    from pypdf.generic import NameObject, BooleanObject, DictionaryObject
    if "/AcroForm" not in writer.root_object:
        writer.root_object.update({NameObject("/AcroForm"): DictionaryObject()})
    writer.root_object["/AcroForm"].update({NameObject("/NeedAppearances"): BooleanObject(True)})
    
    out = io.BytesIO()
    writer.write(out)
    
    # 2. Flatten with PyMuPDF
    fitz_doc = fitz.open('pdf', out.getvalue())
    page = fitz_doc[0]
    
    # Generate appearances for widgets before flattening
    for w in page.widgets():
        w.update()
    
    # Save with no forms
    fitz_doc.save('test_flatten2.pdf')

test_flatten()
