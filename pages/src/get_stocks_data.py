import os
import json
import pathlib

import requests
from dotenv import load_dotenv

from src.config.config import settings
from pages.src.auth_services import SERVER_URL


def post_stocks_data(params, acc_token):

    api_url = SERVER_URL + '/api/stocks'
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
        return f"Запит завершився з помилкою {response.status_code}: {response.text} Please login, time is done"


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
        return f"Запит завершився з помилкою {response.status_code}: {response.text} Please login, time is done"