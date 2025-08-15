import os
import subprocess
import uuid
from flask import Flask, request, send_file, jsonify
from flask_cors import CORS

app = Flask(__name__)

# Allow CORS for all domains
CORS(app, resources={r"/*": {"origins": "*"}})

# Increase file upload limit (100MB)
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024

UPLOAD_FOLDER = "/tmp/uploads"
OUTPUT_FOLDER = "/tmp/outputs"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route("/")
def home():
    return "PDF to Word Converter API is running 🚀"

@app.route("/convert", methods=["POST"])
def convert_pdf_to_word():
    try:
        # Check if file is uploaded
        if "file" not in request.files:
            return jsonify({"error": "No file uploaded"}), 400

        file = request.files["file"]

        if file.filename == "":
            return jsonify({"error": "No selected file"}), 400

        # Save uploaded PDF
        pdf_filename = f"{uuid.uuid4()}.pdf"
        pdf_path = os.path.join(UPLOAD_FOLDER, pdf_filename)
        file.save(pdf_path)

        # Generate DOCX output path
        docx_filename = f"{uuid.uuid4()}.docx"
        docx_path = os.path.join(OUTPUT_FOLDER, docx_filename)

        # Convert PDF to DOCX using LibreOffice
        command = [
            "libreoffice", "--headless", "--convert-to", "docx",
            "--outdir", OUTPUT_FOLDER, pdf_path
        ]
        subprocess.run(command, check=True)

        # LibreOffice outputs with original name, rename to our UUID
        original_docx_path = os.path.join(
            OUTPUT_FOLDER, os.path.splitext(os.path.basename(pdf_path))[0] + ".docx"
        )

        if not os.path.exists(original_docx_path):
            return jsonify({"error": "Conversion failed"}), 500

        os.rename(original_docx_path, docx_path)

        # Send DOCX file to user
        return send_file(docx_path, as_attachment=True)

    except subprocess.CalledProcessError as e:
        return jsonify({"error": f"Conversion error: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        # Cleanup uploaded files to save space
        for f in os.listdir(UPLOAD_FOLDER):
            os.remove(os.path.join(UPLOAD_FOLDER, f))
        for f in os.listdir(OUTPUT_FOLDER):
            if f.endswith(".pdf"):  # keep converted files for sending
                os.remove(os.path.join(OUTPUT_FOLDER, f))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
