"""
app.py — Flask API for the FPL PDF filling service.

Endpoints:
    POST /api/fill-pdf  — Receives JSON, returns filled PDF
"""

from flask import Flask, request, send_file
from flask_cors import CORS
from pdf_service import fill_pdf
import io

app = Flask(__name__)
CORS(app)


@app.route("/api/fill-pdf", methods=["POST"])
def api_fill_pdf():
    """
    Receive a JSON payload, fill the FPL PDF template, and return the PDF.

    Expected JSON: a flat dictionary with keys matching config.FIELD_MAP
    and config.CROSSOUT_MAP.

    Returns: application/pdf file download.
    """
    data = request.get_json()

    if not data:
        return {"error": "No JSON data provided"}, 400

    try:
        # Generate dynamic filename: {Aircraft ID} {Date}.pdf
        aircraft = data.get("aircraft_id", "FPL").replace("/", "-")
        date_val = data.get("date", "").replace("/", "-")
        filename = f"{aircraft} {date_val}.pdf".strip() if date_val else f"{aircraft}.pdf"
        
        pdf_bytes = fill_pdf(data)
        
        return send_file(
            io.BytesIO(pdf_bytes),
            mimetype="application/pdf",
            as_attachment=True,
            download_name=filename,
        )
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {"error": str(e)}, 500


if __name__ == "__main__":
    import os
    # Debug mode only when explicitly requested (never in production).
    app.run(debug=os.environ.get("FLASK_DEBUG") == "1", port=5000, host="0.0.0.0")
