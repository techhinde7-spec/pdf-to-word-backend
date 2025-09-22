# app.py
import os
import tempfile
from flask import Flask, request, send_file, abort, jsonify
from pdf2docx import Converter  # pip install pdf2docx

app = Flask(__name__)

@app.route("/")
def index():
    return "PDF → DOCX converter. POST to /convert/pdf-to-docx with form field 'file'."

@app.route("/convert/pdf-to-docx", methods=["POST"])
def pdf_to_docx():
    if 'file' not in request.files:
        return jsonify({"error": "missing file"}), 400

    f = request.files['file']
    filename = f.filename or "upload.pdf"
    name, ext = os.path.splitext(filename)
    if ext.lower() not in ['.pdf']:
        return jsonify({"error": "only .pdf allowed"}), 400

    # create temp files
    with tempfile.TemporaryDirectory() as tmp:
        in_path = os.path.join(tmp, "input.pdf")
        out_path = os.path.join(tmp, "output.docx")
        f.save(in_path)

        try:
            # convert using pdf2docx
            cv = Converter(in_path)
            # You can pass start and end page if desired: cv.convert(out_path, start=0, end=2)
            cv.convert(out_path, start=0, end=None)
            cv.close()
        except Exception as e:
            return jsonify({"error": "conversion_failed", "message": str(e)}), 500

        if not os.path.exists(out_path):
            return jsonify({"error": "conversion_failed", "message": "output missing"}), 500

        return send_file(out_path, as_attachment=True, download_name=f"{name}.docx")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
