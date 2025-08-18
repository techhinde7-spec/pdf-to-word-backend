from flask import Flask, request, send_file
import os
import subprocess
import uuid

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route("/convert", methods=["POST"])
def convert_pdf_to_word():
    if "file" not in request.files:
        return {"error": "No file provided"}, 400
    
    file = request.files["file"]
    if file.filename == "":
        return {"error": "No file selected"}, 400

    # Save PDF
    file_id = str(uuid.uuid4())
    input_path = os.path.join(UPLOAD_FOLDER, f"{file_id}.pdf")
    output_path = os.path.join(OUTPUT_FOLDER, f"{file_id}.docx")
    file.save(input_path)

    # Run LibreOffice conversion
    subprocess.run([
        "libreoffice",
        "--headless",
        "--convert-to", "docx",
        "--outdir", OUTPUT_FOLDER,
        input_path
    ])

    # Send the converted file
    if os.path.exists(output_path):
        return send_file(output_path, as_attachment=True)
    else:
        return {"error": "Conversion failed"}, 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

