import os
import subprocess
import uuid
from flask import Flask, request, send_file, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "/tmp/uploads"
OUTPUT_FOLDER = "/tmp/outputs"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route("/")
def home():
    return "✅ PDF to Word Converter Backend is running!"

@app.route("/convert", methods=["POST"])
def convert_pdf():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    # Save uploaded file
    input_path = os.path.join(UPLOAD_FOLDER, f"{uuid.uuid4()}.pdf")
    file.save(input_path)

    # Generate output path
    output_filename = f"{uuid.uuid4()}.docx"
    output_path = os.path.join(OUTPUT_FOLDER, output_filename)

    try:
        # Run LibreOffice conversion
        subprocess.run([
            "libreoffice", "--headless", "--convert-to", "docx", "--outdir",
            OUTPUT_FOLDER, input_path
        ], check=True)

        # Find converted file (LibreOffice keeps same base name)
        converted_path = os.path.join(
            OUTPUT_FOLDER,
            os.path.splitext(os.path.basename(input_path))[0] + ".docx"
        )

        if not os.path.exists(converted_path):
            return jsonify({"error": "Conversion failed"}), 500

        return send_file(
            converted_path,
            mimetype="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            as_attachment=True,
            download_name="converted.docx"
        )

    except subprocess.CalledProcessError as e:
        return jsonify({"error": f"Conversion failed: {str(e)}"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
