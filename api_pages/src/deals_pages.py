from datetime import date, datetime

import streamlit as st
import json
import os
import pickle
import configparser
import dotenv


import requests

# dotenv.load_dotenv()

# config = configparser.ConfigParser()
# config.read("config.ini")
#
# FILE_NAME = config.get("DEV", "token_name")
from api_pages.src.auth_services import SERVER_URL, FILE_NAME
from api_pages.src.get_stocks_data import get_product_data
from api_pages.src.company_pages import get_company_by_id


async def get_deal_by_id(acc_token, id):
    api_url = SERVER_URL + f'/api/purchase/{id}'
    headers = {
        "Authorization": f"Bearer {acc_token}",
        'Content-Type': 'application/json'
    }
    response = requests.get(api_url, headers=headers)
    if response.status_code == 200:
        # Отримати дані у форматі JSON
        data = response.json()
        goods_id = data["product_id"]
        company_id = data["company_id"]
        goods = get_product_data("english_name", acc_token)
        company = get_company_by_id(acc_token, company_id)
        data["product"] = next((product['name'] for product in goods if product['id'] == goods_id), None)
        data["company"] = company['company_name']
        return data
    else:
        return f"Запит завершився з помилкою {response.status_code}: {response.text} Please login, time is done"

async def get_deals_by_product(acc_token, product_id):
    api_url = SERVER_URL + '/api/purchase/by_product'
    headers = {
        "Authorization": f"Bearer {acc_token}",
        'Content-Type': 'application/json'
    }
    params = {'product_id': product_id}
    response = requests.post(api_url, headers=headers, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        return f"Запит завершився з помилкою {response.status_code}: {response.text} Please login, time is done"

async def get_deals_by_company(acc_token, company_id):
    api_url = SERVER_URL + '/api/purchase/by_company'
    headers = {
        "Authorization": f"Bearer {acc_token}",
        'Content-Type': 'application/json'
    }
    params = {'company_id': company_id}
    response = requests.get(api_url, headers=headers, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        return f"Запит завершився з помилкою {response.status_code}: {response.text} Please login, time is done"

async def get_deals_by_period(acc_token, start_date, end_date):
    api_url = SERVER_URL + '/api/purchase/by_period'
    headers = {
        "Authorization": f"Bearer {acc_token}",
        'Content-Type': 'application/json'
    }

    # Перетворення дат в рядковий формат YYYY-MM-DD
    start_date_str = start_date.strftime("%Y-%m-%d")
    end_date_str = end_date.strftime("%Y-%m-%d")

    params = {'start_date': start_date_str, 'end_date': end_date_str}
    response = requests.post(api_url, headers=headers, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        return f"Запит завершився з помилкою {response.status_code}: {response.text} Please login, time is done"

async def get_company_list(access_token):
    company_id = st.text_input("Enter id")
    return get_company_by_id(access_token, company_id)

async def create_purchase(purchase_data, acc_token):
    api_url = SERVER_URL + '/api/purchase/'
    headers = {
        "Authorization": f"Bearer {acc_token}",
        'Content-Type': 'application/json'
    }
    response = requests.post(api_url, json=purchase_data, headers=headers)
    if response.status_code == 201:
        return response.json()
    else:
        return f"Запит завершився з помилкою {response.status_code}: {response.text}"


async def update_purchase(purchase_id, purchase_data, acc_token):
    api_url = f'{SERVER_URL}/api/purchase/{purchase_id}'
    headers = {
        "Authorization": f"Bearer {acc_token}",
        'Content-Type': 'application/json'
    }
    response = requests.put(api_url, data=json.dumps(purchase_data), headers=headers)
    if response.status_code == 201:
        return response.json()
    else:
        return f"Запит завершився з помилкою {response.status_code}: {response.text}"

async def delete_purchase(purchase_id, acc_token):
    api_url = SERVER_URL + f'/api/purchase/{purchase_id}'
    headers = {
        "Authorization": f"Bearer {acc_token}",
        'Content-Type': 'application/json'
    }
    response = requests.delete(api_url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return f"Запит завершився з помилкою {response.status_code}: {response.text}"

async def get_purchase_by_id(purchase_id, acc_token):
    api_url = SERVER_URL + f'/api/purchase/{purchase_id}'
    headers = {
        "Authorization": f"Bearer {acc_token}",
        'Content-Type': 'application/json'
    }
    response = requests.get(api_url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return f"Запит завершився з помилкою {response.status_code}: {response.text}"

async def upload_csv(file, acc_token):
    api_url = f'{SERVER_URL}/api/purchase/upload-csv/'
    headers = {"Authorization": f"Bearer {acc_token}"}
    files = {'file': file}
    response = requests.post(api_url, headers=headers, files=files)
    return response

async def delete_purchases(params, acc_token):
    headers = {"Authorization": f"Bearer {acc_token}"}
    response = requests.delete(SERVER_URL + "/api/purchase/purchases/", params=params, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return f"Запит завершився з помилкою {response.status_code}: {response.text}"


