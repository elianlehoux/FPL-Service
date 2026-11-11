"""
pdf_service.py — Core PDF filling logic.

Takes a dictionary of data, fills the PDF template fields,
draws crossout marks where needed, and returns the result as bytes.
"""

import io
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from config import TEMPLATE_PATH, FIELD_MAP, CROSSOUT_MAP, ROUTE_LINE_LIMITS, OTHER_INFO_LINE_LIMITS, FONT_NAME


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

    # --- Step 0: Initialize Canvas and Widget Mapping ---
    import fitz
    doc_fitz = fitz.open(TEMPLATE_PATH)
    page_fitz = doc_fitz[0]
    
    # Store widget properties for perfect ReportLab alignment
    widget_info = {}
    for w in page_fitz.widgets():
        widget_info[w.field_name] = {
            "rect": w.rect,
            "font_size": w.text_fontsize if w.text_fontsize > 0 else 10.5
        }

    overlay_packet = io.BytesIO()
    overlay_canvas = canvas.Canvas(overlay_packet, pagesize=(page_width, page_height))

    # --- Step 1: Process text values ---
    acroform_values = {}
    found_any = False

    def split_text_to_lines(text, max_chars_list):
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
                current_line = word
        if current_line:
            lines.append(current_line)
        return lines

    for json_key, pdf_info in FIELD_MAP.items():
        if json_key in data and data[json_key] is not None:
            value = data[json_key]
            if isinstance(pdf_info, list):
                limits = ROUTE_LINE_LIMITS if json_key == "route" else OTHER_INFO_LINE_LIMITS
                lines = split_text_to_lines(value, limits)
                for i, pdf_field_name in enumerate(pdf_info):
                    if i < len(lines):
                        acroform_values[pdf_field_name] = lines[i]
            else:
                acroform_values[pdf_info] = str(value).upper()
            found_any = True
    
    # Render flattened text using ReportLab with exact Box Centering alignment
    if found_any:
        
        # Determine which fields should be left-aligned vs centered
        left_aligned_fields = [
            "Textbox13", "Textbox14", "Textbox15", "Textbox16", "Textbox17",  # Route
            "Textbox22", "Textbox23", "Textbox24", "Textbox25",  # Other info
            "Textbox33", # Remarks
            "Textbox32", # Aircraft colour
            "Textbox34"  # Pilot in command
        ]

        for field_name, text in acroform_values.items():
            if field_name in widget_info:
                info = widget_info[field_name]
                r = info["rect"]
                font_size = info["font_size"]
                
                # ReportLab Y is bottom-left, PyMuPDF is top-left
                rl_y_bottom = page_height - r.y0 - r.height
                
                # Adjust font size logic
                multiline_fields = ["Textbox13", "Textbox14", "Textbox15", "Textbox16", "Textbox17", 
                                    "Textbox22", "Textbox23", "Textbox24", "Textbox25", "Textbox33"]
                
                if field_name in multiline_fields:
                    font_size = 10
                else:
                    font_size = info["font_size"]
                
                overlay_canvas.setFont(FONT_NAME, font_size)
                
                spaced_fields = {
                    "Aircraft identification": 7,
                    "Type of aircraft": 4,
                    "Number": 2,
                    "Textbox9": 4,  # departure_aerodrome
                    "Textbox10": 4, # departure_time
                    "Textbox11": 5, # cruising_speed
                    "Textbox12": 5, # level
                    "Textbox18": 4, # destination_aerodrome
                    "Textbox19": 4, # total_eet
                    "Textbox20": 4, # altn_aerodrome
                    "Textbox21": 4, # altn_aerodrome_2
                    "Textbox26": 4, # endurance
                    "Textbox28": 3, # persons_on_board
                }
                
                if field_name in spaced_fields:
                    slots = spaced_fields[field_name]
                    slot_width = r.width / slots
                    
                    # Pad text with spaces if shorter to distribute properly, or just use length
                    # For time fields, right justification or left? Time is usually filled "1400".
                    # Persons on board "2" might be right justified (2 at the end) but let's just 
                    # distribute left-to-right whatever they typed. The HTML ensures max length.
                    for i, char in enumerate(text[:slots]):
                        char_width = overlay_canvas.stringWidth(char, FONT_NAME, font_size)
                        # Center of the current slot
                        x_pos = r.x0 + (slot_width * i) + (slot_width - char_width) / 2.0
                        y_pos = rl_y_bottom + (r.height - font_size) / 2.0 + (font_size * 0.25) - 1
                        overlay_canvas.drawString(x_pos, y_pos, char)
                else:
                    text_width = overlay_canvas.stringWidth(text, FONT_NAME, font_size)
                    
                    # Check alignment
                    if field_name in left_aligned_fields:
                        # Left Align with padding
                        x_pos = r.x0 + 4
                    else:
                        # Center Align horizontally
                        x_pos = r.x0 + (r.width - text_width) / 2.0
                    
                    # Center vertically based on font size baseline
                    y_pos = rl_y_bottom + (r.height - font_size) / 2.0 + (font_size * 0.25) - 1
                        
                    overlay_canvas.drawString(x_pos, y_pos, text)

    # --- Step 2: Draw overlays (crossouts and signatures) ---
    from config import CROSSOUT_GROUPS
    import base64
    from reportlab.lib.utils import ImageReader

    for master_key, sub_keys in CROSSOUT_GROUPS.items():
        all_false = True
        for sk in sub_keys:
            if data.get(sk) is True:
                all_false = False
                break
        if all_false:
            data[master_key] = False
        else:
            data[master_key] = True

    has_overlays = True # Always True since we are rendering all text here
    for json_key, coords_list in CROSSOUT_MAP.items():
        if json_key in data and data[json_key] is False and coords_list:
            for coord in coords_list:
                x = coord["x"]
                y = coord["y"]
                w = coord["w"]
                h = coord["h"]
                overlay_canvas.setFillColorRGB(0, 0, 0)
                overlay_canvas.rect(x, y, w, h, fill=1, stroke=0)
                
    if data.get("signature_image"):
        try:
            header, encoded = data["signature_image"].split(",", 1)
            img_data = base64.b64decode(encoded)
            img_stream = io.BytesIO(img_data)
            img_reader = ImageReader(img_stream)
            
            # Signature coordinates (Signature36 field area — Far Right)
            sig_x = 325
            sig_y = 51
            sig_w = 80
            sig_h = 26
            
            overlay_canvas.drawImage(img_reader, sig_x, sig_y, width=sig_w, height=sig_h, mask='auto')
        except Exception as e:
            print(f"DEBUG: Failed to process signature: {e}")

    # Merge overlay with template background
    overlay_canvas.save()
    overlay_packet.seek(0)
    overlay_reader = PdfReader(overlay_packet)
    writer.pages[0].merge_page(overlay_reader.pages[0])

    # --- Step 3: FLATTEN The Template ---
    # Strip AcroForm and Annotations completely so no blue interactive boxes remain
    if "/Annots" in writer.pages[0]:
        del writer.pages[0]["/Annots"]
    if "/AcroForm" in writer.root_object:
        del writer.root_object["/AcroForm"]

    # --- Step 3: Write result to bytes ---
    output = io.BytesIO()
    writer.write(output)
    output.seek(0)
    return output.read()
