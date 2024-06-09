import streamlit as st
import json
import os
import pickle
import configparser
import dotenv


import requests
# from pages.Authorization import auth_manager
from api_pages.src.auth_services import FILE_NAME, SERVER_URL
# dotenv.load_dotenv()

#
# config = configparser.ConfigParser()
# config.read("config.ini")
#
# FILE_NAME = config.get("DEV", "token_name")
# SERVER_URL = config.get("DEV", "APP_URL")


# def get_company_by_id(id):
#     st.write("WTF", id)
def get_company_by_id(acc_token, id):

    api_url = SERVER_URL + f'/api/company/{id}'
    headers = {
        "Authorization": f"Bearer {acc_token}",
        'Content-Type': 'application/json'
    }
    response = requests.get(api_url, headers=headers)
    if response.status_code == 200:
        # Отримати дані у форматі JSON
        data = response.json()
        return data
    else:
        return {response.status_code: response.text}


async def create_company_api(acc_token, company_data):
    api_url = SERVER_URL + '/api/company/'
    headers = {
        "Authorization": f"Bearer {acc_token}",
        'Content-Type': 'application/json'
    }
    response = requests.post(api_url, json=company_data, headers=headers)
    if response.status_code == 201:
        data = response.json()
        return data
    else:
        return {response.status_code: response.text}

async def update_company_api(acc_token, company_id, company_data):
    api_url = SERVER_URL + f'/api/company/{company_id}'
    headers = {
        "Authorization": f"Bearer {acc_token}",
        'Content-Type': 'application/json'
    }
    response = requests.put(api_url, json=company_data, headers=headers)
    if response.status_code == 201:
        data = response.json()
        return data
    else:
        return {response.status_code: response.text}

async def delete_company_api(acc_token, company_id):
    api_url = SERVER_URL + f'/api/company/{company_id}'
    headers = {
        "Authorization": f"Bearer {acc_token}",
        'Content-Type': 'application/json'
    }
    response = requests.delete(api_url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return {response.status_code: response.text}

async def search_companies_by_name(acc_token, company_name):
    api_url = SERVER_URL + '/api/company/search/'
    headers = {
        "Authorization": f"Bearer {acc_token}",
        'Content-Type': 'application/json'
    }
    params = {"company_name": company_name}
    response = requests.get(api_url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        return data["items"]
    else:
        return {response.status_code: response.text}

async def upload_company_csv(file, acc_token):
    api_url = f'{SERVER_URL}/api/company/upload-csv/'
    headers = {"Authorization": f"Bearer {acc_token}"}
    files = {'file': file}
    response = requests.post(api_url, headers=headers, files=files)
    return response
