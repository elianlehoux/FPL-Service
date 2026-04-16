"""
pdf_service.py — Core PDF filling logic.

Takes a dictionary of data, fills the PDF template fields,
draws crossout marks where needed, and returns the result as bytes.
"""

import io
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from config import TEMPLATE_PATH, FIELD_MAP, CROSSOUT_MAP, ROUTE_LINE_LIMITS, OTHER_INFO_LINE_LIMITS


def fill_pdf(data: dict) -> bytes:
    """
    Fill the FPL PDF template with the provided data.

    Args:
        data: Dictionary with JSON keys matching those in config.FIELD_MAP
              and config.CROSSOUT_MAP.

    Returns:
        The filled PDF as bytes, ready to be saved or sent as a response.
    """
    reader = PdfReader(TEMPLATE_PATH)
    writer = PdfWriter()
    writer.append(reader)

    page = reader.pages[0]
    page_width = float(page.mediabox.width)
    page_height = float(page.mediabox.height)

    # --- Step 0: Force NeedAppearances ---
    from pypdf.generic import NameObject, BooleanObject, DictionaryObject
    
    if "/AcroForm" not in writer.root_object:
        writer.root_object.update({
            NameObject("/AcroForm"): DictionaryObject()
        })
    
    acroform = writer.root_object["/AcroForm"]
    acroform.update({
        NameObject("/NeedAppearances"): BooleanObject(True)
    })

    # --- Step 1: Fill AcroForm text fields ---
    acroform_values = {}
    found_any = False

    def split_text_to_lines(text, max_chars_list):
        """Splits text into a list of lines using a list of max char limits."""
        if not text: return []
        words = str(text).upper().replace('\n', ' ').split()
        lines = []
        current_line = ""
        line_idx = 0
        
        for word in words:
            limit = max_chars_list[line_idx] if line_idx < len(max_chars_list) else max_chars_list[-1]
            
            new_len = len(current_line) + 1 + len(word) if current_line else len(word)
            
            if new_len <= limit:
                current_line = (current_line + " " + word) if current_line else word
            else:
                if current_line:
                    lines.append(current_line)
                    line_idx += 1
                
                # word goes to the next line
                current_line = word
                
        if current_line:
            lines.append(current_line)
        return lines

    # Process normal fields and multi-line fields
    for json_key, pdf_info in FIELD_MAP.items():
        if json_key in data and data[json_key] is not None:
            value = data[json_key]
            
            # If the config maps this key to a LIST of PDF fields (multi-line)
            if isinstance(pdf_info, list):
                # Choose correct limits based on field purpose
                limits = ROUTE_LINE_LIMITS if json_key == "route" else OTHER_INFO_LINE_LIMITS
                lines = split_text_to_lines(value, limits)
                for i, pdf_field_name in enumerate(pdf_info):
                    if i < len(lines):
                        acroform_values[pdf_field_name] = lines[i]
            # Normal single-field mapping
            else:
                acroform_values[pdf_info] = str(value).upper()
            found_any = True
    
    if found_any:
        print(f"DEBUG: Filling fields: {list(acroform_values.keys())}")
        writer.update_page_form_field_values(writer.pages[0], acroform_values)

    # --- Step 2: Draw crossout marks for Casilla 19 checkboxes ---
    overlay_packet = io.BytesIO()
    overlay_canvas = canvas.Canvas(overlay_packet, pagesize=(page_width, page_height))

    has_crossouts = False
    for json_key, coords_list in CROSSOUT_MAP.items():
        # If the key is present and its value is False, draw the crossout
        if json_key in data and data[json_key] is False and coords_list:
            for coord in coords_list:
                x = coord["x"]
                y = coord["y"]
                w = coord["w"]
                h = coord["h"]
                overlay_canvas.setFillColorRGB(0, 0, 0)
                overlay_canvas.rect(x, y, w, h, fill=1, stroke=0)
                has_crossouts = True

    if has_crossouts:
        overlay_canvas.save()
        overlay_packet.seek(0)
        overlay_reader = PdfReader(overlay_packet)
        writer.pages[0].merge_page(overlay_reader.pages[0])

    # --- Step 3: Write result to bytes ---
    output = io.BytesIO()
    writer.write(output)
    output.seek(0)
    return output.read()
