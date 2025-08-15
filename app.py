from flask import Flask, request, send_file, jsonify
import os
import subprocess
import uuid

app = Flask(__name__)

UPLOAD_FOLDER = "/tmp/uploads"
OUTPUT_FOLDER = "/tmp/outputs"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route("/")
def home():
    return "PDF to Word Converter API is running."

@app.route("/convert", methods=["POST"])
def convert_pdf_to_word():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    file_id = str(uuid.uuid4())
    pdf_path = os.path.join(UPLOAD_FOLDER, f"{file_id}.pdf")
    docx_path = os.path.join(OUTPUT_FOLDER, f"{file_id}.docx")

    # Save uploaded file
    file.save(pdf_path)

    try:
        # Convert using LibreOffice
        subprocess.run([
            "libreoffice", "--headless", "--convert-to", "docx",
            pdf_path, "--outdir", OUTPUT_FOLDER
        ], check=True)

        return send_file(docx_path, as_attachment=True)

    except subprocess.CalledProcessError as e:
        return jsonify({"error": "Conversion failed", "details": str(e)}), 500

    finally:
        # Cleanup
        if os.path.exists(pdf_path):
            os.remove(pdf_path)
        if os.path.exists(docx_path):
            os.remove(docx_path)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
