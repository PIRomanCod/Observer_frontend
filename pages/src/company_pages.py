import streamlit as st
import json
import os
import pickle
import configparser
import dotenv


import requests

# dotenv.load_dotenv()

config = configparser.ConfigParser()
config.read("config.ini")

FILE_NAME = config.get("DEV", "token_name")
SERVER_URL = config.get("DEV", "APP_URL")


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
        return f"Запит завершився з помилкою {response.status_code}: {response.text} Please login, time is done"