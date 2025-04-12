from flask import Flask, request, jsonify
import re
from passporteye import read_mrz
import os

app = Flask(__name__)

def reformat_date(date):
    match = re.match(r"(\d{2})(\d{2})(\d{2})", date)
    if match:
        year, month, day = match.groups()
        return f"{day}/{month}/{year}"
    return date

def extract_mrz_data(image_path):
    mrz = read_mrz(image_path)
    if mrz is not None:
        mrz_data = mrz.to_dict()
        return {
            "Tipo de Documento": mrz_data.get('type', 'N/A'),
            "País de Emissão": mrz_data.get('country', 'N/A'),
            "Nome(s)": mrz_data.get('names', 'N/A'),
            "Sobrenome": mrz_data.get('surname', 'N/A'),
            "Número do Documento": mrz_data.get('number', 'N/A'),
            "Nacionalidade": mrz_data.get('nationality', 'N/A'),
            "Data de Nascimento": reformat_date(mrz_data.get('date_of_birth', 'N/A')),
            "Sexo": mrz_data.get('sex', 'N/A'),
            "Data de Validade": reformat_date(mrz_data.get('expiration_date', 'N/A')),
            "Número de Controle": mrz_data.get('optional_data', 'N/A')
        }
    return None

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if file:
        file_path = os.path.join('uploads', file.filename)
        file.save(file_path)
        mrz_data = extract_mrz_data(file_path)
        if mrz_data:
            return jsonify(mrz_data), 200
        else:
            return jsonify({"error": "MRZ não foi encontrado ou não pôde ser lido."}), 400

if __name__ == '__main__':
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    app.run(debug=True)
