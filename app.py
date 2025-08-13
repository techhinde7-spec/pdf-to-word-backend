from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from pdf2docx import Converter
import os
import tempfile

app = Flask(__name__)
CORS(app)  # Allow frontend from any domain

@app.route('/convert', methods=['POST'])
def convert_pdf_to_word():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "Empty filename"}), 400

    try:
        # Save PDF temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
            file.save(temp_pdf.name)
            temp_pdf_path = temp_pdf.name

        # Create temporary output DOCX path
        temp_docx_path = temp_pdf_path.replace(".pdf", ".docx")

        # Convert PDF to DOCX
        cv = Converter(temp_pdf_path)
        cv.convert(temp_docx_path)
        cv.close()

        # Send the converted file
        return send_file(
            temp_docx_path,
            as_attachment=True,
            download_name="converted.docx"
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        # Cleanup temporary files
        try:
            os.remove(temp_pdf_path)
            if os.path.exists(temp_docx_path):
                os.remove(temp_docx_path)
        except:
            pass


@app.route('/', methods=['GET'])
def home():
    return "PDF to Word Converter Backend is Running!"


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
