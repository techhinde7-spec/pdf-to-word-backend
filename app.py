from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
import os
import subprocess
import tempfile
import uuid

app = Flask(__name__)
CORS(app)  # allow all origins

@app.route("/")
def home():
    return jsonify({"status": "running"})

@app.route("/convert", methods=["POST"])
def convert():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    uploaded_file = request.files["file"]
    if uploaded_file.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    with tempfile.TemporaryDirectory() as tmpdir:
        input_path = os.path.join(tmpdir, uploaded_file.filename)
        uploaded_file.save(input_path)

        output_ext = ".docx" if input_path.endswith(".pdf") else ".pdf"
        output_path = os.path.join(tmpdir, str(uuid.uuid4()) + output_ext)

        # Use LibreOffice CLI for conversion
        try:
            subprocess.run([
                "libreoffice", "--headless", "--convert-to",
                "docx" if output_ext == ".docx" else "pdf",
                "--outdir", tmpdir, input_path
            ], check=True)
        except subprocess.CalledProcessError as e:
            return jsonify({"error": "Conversion failed", "details": str(e)}), 500

        if not os.path.exists(output_path):
            # try to guess filename (LibreOffice sometimes renames it)
            for f in os.listdir(tmpdir):
                if f.endswith(output_ext):
                    output_path = os.path.join(tmpdir, f)
                    break

        return send_file(output_path, as_attachment=True)
