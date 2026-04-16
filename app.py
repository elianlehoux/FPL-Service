"""
app.py — Flask API for the FPL PDF filling service.

Endpoints:
    POST /api/fill-pdf  — Receives JSON, returns filled PDF
    GET  /               — Serves the test frontend
"""

from flask import Flask, request, send_file, render_template
from flask_cors import CORS
from pdf_service import fill_pdf
import io

app = Flask(__name__)
CORS(app)


@app.route("/")
def index():
    """Serve the test frontend."""
    return render_template("index.html")


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
        pdf_bytes = fill_pdf(data)
        return send_file(
            io.BytesIO(pdf_bytes),
            mimetype="application/pdf",
            as_attachment=True,
            download_name="FPL_FILLED.pdf",
        )
    except Exception as e:
        return {"error": str(e)}, 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)
