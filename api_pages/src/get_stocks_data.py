import os
import json
import pathlib

import requests
from dotenv import load_dotenv

from src.config.config import settings
from api_pages.src.auth_services import SERVER_URL


def post_stocks_data(params, acc_token):

    api_url = SERVER_URL + '/api/stocks/list'
    data = params
    # data_json = json.dumps(data)
    data_json = params["product_ids"]
    headers = {
        "Authorization": f"Bearer {acc_token}",
        'Content-Type': 'application/json'
    }
    response = requests.post(api_url, params=data, json=data_json, headers=headers)
    if response.status_code == 200:
        # Отримати дані у форматі JSON
        data = response.json()
        return data
    else:
        return f"Запит завершився з помилкою {response.status_code}: {response.text} Please login, time is gone"


def get_product_data(language, acc_token):

    api_url = SERVER_URL + '/api/products'
    params = {"language": language}
    headers = {
        "Authorization": f"Bearer {acc_token}",
        'Content-Type': 'application/json'
    }
    response = requests.get(api_url, params=params, headers=headers)
    if response.status_code == 200:
        # Отримати дані у форматі JSON
        data = response.json()
        return data
    else:
        return f"Запит завершився з помилкою {response.status_code}: {response.text} Please login, time is gone"


def del_stocks_by_date(target_date, acc_token):
    api_url = SERVER_URL + f'/api/stocks/date/{target_date.strftime("%Y-%m-%d")}'
    headers = {
        "Authorization": f"Bearer {acc_token}",
        'Content-Type': 'application/json'
    }
    response = requests.delete(api_url, headers=headers)
    if response.status_code == 200:
        # Отримати дані у форматі JSON
        data = response.json()
        return data
    else:
        return f"Запит завершився з помилкою {response.status_code}: {response.text} Please login, time is gone"

def create_new_stock_note(data, acc_token):

    api_url = SERVER_URL + '/api/stocks/'
    payload = {
        "date": data["date"].strftime('%Y-%m-%d'),  # Перетворіть дату у строку
        "product_id": data["product_id"],
        "quantity": data["quantity"]
    }    # data_json = json.dumps(data)
    headers = {
        "Authorization": f"Bearer {acc_token}",
        'Content-Type': 'application/json'
    }
    response = requests.post(api_url, json=payload, headers=headers)
    if response.status_code == 200:
        # Отримати дані у форматі JSON
        data = response.json()
        return data
    else:
        return f"Запит завершився з помилкою {response.status_code}: {response.text} Please login, time is gone"

def upload_file_to_server(uploaded_file, acc_token):
    api_url = f"{SERVER_URL}/api/stocks/upload_csv"
    headers = {
        "Authorization": f"Bearer {acc_token}"
    }

    files = {'file': (uploaded_file.name, uploaded_file.getvalue(), 'text/csv')}
    response = requests.post(api_url, files=files, headers=headers)

    if response.status_code == 200:
        "File successfully uploaded and processed"
        return response.json()
    else:
        "Failed to upload and process file"
        return response.json()

