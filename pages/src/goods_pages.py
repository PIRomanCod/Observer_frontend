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


def get_goods_by_id(id):
    st.write("WTF", id)
