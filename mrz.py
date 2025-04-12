import re
from passporteye import read_mrz
import os

image_path = input("Enter the path to the MRZ image: ")

while not os.path.exists(image_path):
    print("File not found. Please try again.")
    image_path = input("Enter the path to the MRZ image: ")

def reformat_date(date):
    match = re.match(r"(\d{2})(\d{2})(\d{2})", date)
    if match:
        year, month, day = match.groups()
        return f"{day}/{month}/{year}"
    return date

mrz = read_mrz(image_path)

if mrz is not None:
    mrz_data = mrz.to_dict()
    print("MRZ extraído com sucesso!")
    print("Tipo de Documento:", mrz_data.get('type', 'N/A'))
    print("País de Emissão:", mrz_data.get('country', 'N/A'))
    print("Nome(s):", mrz_data.get('names', 'N/A'))
    print("Sobrenome:", mrz_data.get('surname', 'N/A'))
    print("Número do Documento:", mrz_data.get('number', 'N/A'))
    print("Nacionalidade:", mrz_data.get('nationality', 'N/A'))
    date_of_birth = mrz_data.get('date_of_birth', 'N/A')
    expiration_date = mrz_data.get('expiration_date', 'N/A')
    print("Data de Nascimento:", reformat_date(date_of_birth))
    print("Sexo:", mrz_data.get('sex', 'N/A'))
    print("Data de Validade:", reformat_date(expiration_date))
    print("Número de Controle:", mrz_data.get('optional_data', 'N/A'))
else:
    print("MRZ não foi encontrado ou não pôde ser lido.")
