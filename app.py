from flask import Flask, request, send_file
import os
import mammoth

app = Flask(__name__)

@app.route("/")
def home():
    return "PDF to Word Converter Backend is running!"

@app.route("/convert", methods=["POST"])
def convert_pdf_to_word():
    if "file" not in request.files:
        return "No file uploaded", 400

    uploaded_file = request.files["file"]
    if uploaded_file.filename == "":
        return "No selected file", 400

    # Save uploaded file
    pdf_path = "uploaded.pdf"
    uploaded_file.save(pdf_path)

    # Simulate conversion (just renaming for now)
    docx_path = "converted.docx"
    os.rename(pdf_path, docx_path)

    return send_file(docx_path, as_attachment=True, download_name="converted.docx")
