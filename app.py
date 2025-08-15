from flask import Flask, request, send_file, jsonify
from pdf2docx import Converter
import os

app = Flask(__name__)

@app.route("/convert", methods=["POST"])
def convert_file():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    input_path = "/tmp/input.pdf"
    output_path = "/tmp/output.docx"
    file.save(input_path)

    try:
        cv = Converter(input_path)
        cv.convert(output_path, start=0, end=None)
        cv.close()
    except Exception as e:
        return jsonify({"error": f"Conversion failed: {str(e)}"}), 500

    return send_file(output_path, as_attachment=True, download_name="converted.docx")

@app.route("/", methods=["GET"])
def home():
    return "✅ PDF to Word API is running"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
