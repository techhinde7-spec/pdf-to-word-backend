import os
import uuid
from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from pdf2docx import Converter
import pypandoc

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "/tmp/uploads"
OUTPUT_FOLDER = "/tmp/outputs"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route("/")
def home():
    return "PDF ⇆ Word Converter API Running!"

@app.route("/convert", methods=["POST"])
def convert_file():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    filename = file.filename
    ext = filename.split(".")[-1].lower()
    file_id = str(uuid.uuid4())

    input_path = os.path.join(UPLOAD_FOLDER, f"{file_id}.{ext}")
    file.save(input_path)

    try:
        # PDF → DOCX
        if ext == "pdf":
            output_path = os.path.join(OUTPUT_FOLDER, f"{file_id}.docx")
            cv = Converter(input_path)
            cv.convert(output_path, start=0, end=None)
            cv.close()
            return send_file(output_path, as_attachment=True)

        # DOCX → PDF
        elif ext == "docx":
            output_path = os.path.join(OUTPUT_FOLDER, f"{file_id}.pdf")
            pypandoc.convert_file(input_path, "pdf", outputfile=output_path)
            return send_file(output_path, as_attachment=True)

        else:
            return jsonify({"error": "Only PDF or DOCX supported"}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
