import fitz

def test_fitz():
    doc = fitz.open('FPL_TEMPLATE.pdf')
    page = doc[0]
    
    WIDGETS = [w for w in page.widgets()]
    for w in WIDGETS:
        if w.field_name == 'Aircraft identification':
            w.field_value = 'LVABC'
            w.update()
            
    # Try to flatten using fitz
    doc.save('test_fitz.pdf', deflate=True)

test_fitz()
