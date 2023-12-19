from decimal import Decimal

import pandas as pd
import streamlit as st
import configparser
import matplotlib.pyplot as plt
import seaborn as sns

import plotly.express as px
import plotly.subplots as sp
import plotly.graph_objects as go

import requests

config = configparser.ConfigParser()
config.read("config.ini")

FILE_NAME = config.get("DEV", "token_name")
from api_pages.src.auth_services import SERVER_URL
from api_pages.src.company_pages import get_company_by_id
from api_pages.src.messages import balance_messages


def get_transaction_by_id(language, acc_token, id):
    api_url = SERVER_URL + f'/api/transaction/{id}'
    headers = {
        "Authorization": f"Bearer {acc_token}",
        'Content-Type': 'application/json'
    }
    response = requests.get(api_url, headers=headers)
    if response.status_code == 200:
        # Отримати дані у форматі JSON
        data = response.json()
        company_id = data["company_id"]
        company = get_company_by_id(acc_token, company_id)
        data["company"] = company['company_name']
        return data
    else:
        return f"{balance_messages[language]['error_response']} {response.status_code}: {response.text}"


async def get_transaction_by_company(language, acc_token, company_id):
    api_url = SERVER_URL + f'/api/transactions/by_company/{company_id}'
    headers = {
        "Authorization": f"Bearer {acc_token}",
        'Content-Type': 'application/json'
    }
    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        return f"{balance_messages[language]['error_response']} {response.status_code}: {response.text}"


async def get_transactions_by_period(language, acc_token, start_date, end_date):
    api_url = SERVER_URL + '/api/transactions/turnover/by_period'
    headers = {
        "Authorization": f"Bearer {acc_token}",
        'Content-Type': 'application/json'
    }

    # Перетворення дат в рядковий формат YYYY-MM-DD
    start_date_str = start_date.strftime("%Y-%m-%d")
    end_date_str = end_date.strftime("%Y-%m-%d")

    params = {'start_date': start_date_str, 'end_date': end_date_str}
    response = requests.get(api_url, headers=headers, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        return f"{balance_messages[language]['error_response']} {response.status_code}: {response.text}"


async def get_turnovers(language, acc_token):
    api_url = SERVER_URL + f'/api/transactions/turnover/'
    headers = {
        "Authorization": f"Bearer {acc_token}",
        'Content-Type': 'application/json'
    }
    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        return f"{balance_messages[language]['error_response']} {response.status_code}: {response.text}"


async def get_rate_by_date(language, acc_token, date):
    date_str = date.strftime("%Y-%m-%d")
    api_url = SERVER_URL + f'/api/rates/{date_str}'
    headers = {
        "Authorization": f"Bearer {acc_token}",
        'Content-Type': 'application/json'
    }

    # Перетворення дат в рядковий формат YYYY-MM-DD

    # params = {'date': date_str}
    response = requests.get(api_url, headers=headers)#, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        return f"{balance_messages[language]['error_response']} {response.status_code}: {response.text}"


async def calculate_balance(data):
    tl_balance = 0
    usd_balance = 0

    for item in data.get("items", []):
        sum_value = Decimal(item.get("sum", 0))
        currency = item.get("currency", "").lower()
        usd_tl_rate = Decimal(item.get("usd_tl_rate", 1))

        if currency == "usd":
            if item.get("operation_type", "").lower() == "debit":
                usd_balance += sum_value
            elif item.get("operation_type", "").lower() == "credit":
                usd_balance -= sum_value

        if currency == "tl":
            if item.get("operation_type", "").lower() == "debit":
                tl_balance += sum_value
            elif item.get("operation_type", "").lower() == "credit":
                tl_balance -= sum_value

    eval_to_tl = usd_balance*usd_tl_rate+tl_balance
    eval_to_usd = usd_balance+tl_balance/usd_tl_rate

    return round(eval_to_tl, 2), round(eval_to_usd, 2)

#
# async def calculate_balance_usd(language, data):
#     usd_balance = 0
#
#     for item in data.get("items", []):
#         print(item)
#         sum_value = Decimal(item.get("sum", 0))
#         currency = item.get("currency", "").lower()
#
#         # Convert to TL if currency is USD or EUR
#         if currency in ["tl", "eur"]:
#             usd_tl_rate = Decimal(item.get("usd_tl_rate", 1))
#             eur_usd_rate = Decimal(item.get("eur_usd_rate", 1))
#             if currency == "tl":
#                 sum_value = sum_value/usd_tl_rate
#             elif currency == "eur":
#                 sum_value = sum_value * eur_usd_rate
#
#         if item.get("operation_type", "").lower() == "debit":
#             usd_balance += sum_value
#         elif item.get("operation_type", "").lower() == "credit":
#             usd_balance -= sum_value
#         print(usd_balance)
#     return round(usd_balance, 2)


async def get_tables(exchange_rate, data):
    df = pd.DataFrame(data["items"])

    # Преобразование валюты
    df["debit_turnover_target_usd"] = (
            df["debit_turnover_tl"] / exchange_rate + df["debit_turnover_usd"]
    )
    df["credit_turnover_target_usd"] = (
            df["credit_turnover_tl"] / exchange_rate + df["credit_turnover_usd"]
    )

    # Группировка по "expenses_category"
    grouped_df = df.groupby("expenses_category").agg({
        "debit_turnover_tl": "sum",
        "credit_turnover_tl": "sum",
        "debit_turnover_usd": "sum",
        "credit_turnover_usd": "sum",
        "debit_turnover_target_usd": "sum",
        "credit_turnover_target_usd": "sum"
    }).reset_index()

    # Расчет балансов
    grouped_df["balance_tl"] = (
            grouped_df["debit_turnover_tl"] - grouped_df["credit_turnover_tl"]
            + (grouped_df["debit_turnover_usd"] - grouped_df["credit_turnover_usd"]) * exchange_rate
    )

    grouped_df["balance_usd"] = (
            (grouped_df["debit_turnover_tl"] - grouped_df["credit_turnover_tl"]) / exchange_rate
            + grouped_df["debit_turnover_usd"] - grouped_df["credit_turnover_usd"]
    )

    # Добавление строк итогов
    totals_df = pd.DataFrame({
        "expenses_category": ["Total"],
        "debit_turnover_tl": [grouped_df["debit_turnover_tl"].sum()],
        "credit_turnover_tl": [grouped_df["credit_turnover_tl"].sum()],
        "debit_turnover_usd": [grouped_df["debit_turnover_usd"].sum()],
        "credit_turnover_usd": [grouped_df["credit_turnover_usd"].sum()],
        "debit_turnover_target_usd": [grouped_df["debit_turnover_target_usd"].sum()],
        "credit_turnover_target_usd": [grouped_df["credit_turnover_target_usd"].sum()],

        "balance_tl": [grouped_df["balance_tl"].sum()],
        "balance_usd": [grouped_df["balance_usd"].sum()]
    })

    grouped_df = pd.concat([grouped_df, totals_df], ignore_index=True)

    # Группировка по "company_id"
    grouped_df1 = df.groupby("company_id").agg({
        "debit_turnover_tl": "sum",
        "credit_turnover_tl": "sum",
        "debit_turnover_usd": "sum",
        "credit_turnover_usd": "sum",
        "debit_turnover_target_usd": "sum",
        "credit_turnover_target_usd": "sum"
    }).reset_index()

    # Расчет балансов
    grouped_df1["balance_tl"] = (
            grouped_df1["debit_turnover_tl"] - grouped_df1["credit_turnover_tl"]
            + (grouped_df1["debit_turnover_usd"] - grouped_df1["credit_turnover_usd"]) * exchange_rate
    )

    grouped_df1["balance_usd"] = (
            (grouped_df1["debit_turnover_tl"] - grouped_df1["credit_turnover_tl"]) / exchange_rate
            + grouped_df1["debit_turnover_usd"] - grouped_df1["credit_turnover_usd"]
    )

    # Добавление строк итогов
    totals_df1 = pd.DataFrame({
        "company_id": ["Total"],
        "debit_turnover_tl": [grouped_df1["debit_turnover_tl"].sum()],
        "credit_turnover_tl": [grouped_df1["credit_turnover_tl"].sum()],
        "debit_turnover_usd": [grouped_df1["debit_turnover_usd"].sum()],
        "credit_turnover_usd": [grouped_df1["credit_turnover_usd"].sum()],
        "debit_turnover_target_usd": [grouped_df1["debit_turnover_target_usd"].sum()],
        "credit_turnover_target_usd": [grouped_df1["credit_turnover_target_usd"].sum()],
        "balance_tl": [grouped_df1["balance_tl"].sum()],
        "balance_usd": [grouped_df1["balance_usd"].sum()]
    })

    grouped_df1 = pd.concat([grouped_df1, totals_df1], ignore_index=True)
    # Вывод DataFrame с новыми строками итогов

    return grouped_df, grouped_df1


async def get_plot_by_category(language, data):
    st.title(balance_messages[language]["category"])
    st.write(balance_messages[language]["graph"])
    # Визуализация с помощью plotly.subplots
    fig = sp.make_subplots(rows=1, cols=2, specs=[[{'type': 'pie'}, {'type': 'pie'}]],
                           subplot_titles=balance_messages[language]["subplot_titles"])

    # By tl
    trace_product = (px.pie(
        data.query('expenses_category != "Total"'),
        values='debit_turnover_target_usd',
        names='expenses_category',
        hole=0.2,
        color_discrete_sequence=px.colors.qualitative.Set1,
    )).update_traces(name=balance_messages[language]["debit_usd"])
    fig.add_trace(trace_product.data[0], row=1, col=1)

    # By usd
    trace_product = (px.pie(
        data.query('expenses_category != "Total"'),
        values='credit_turnover_target_usd',
        names='expenses_category',
        hole=0.2,
        color_discrete_sequence=px.colors.qualitative.Vivid,
    )).update_traces(name=balance_messages[language]["credit_usd"])
    fig.add_trace(trace_product.data[0], row=1, col=2)

    fig.update_layout()

    # Визуализация с помощью plotly.express
    fig2 = px.bar(
        data.query('expenses_category != "Total"'),
        x='expenses_category',
        y=['balance_usd'],
        barmode='group',
        color_discrete_sequence=['green'],
        labels={'balance_usd': 'Баланс'},
        title=balance_messages[language]["category_balance"]
    )

    # Вывод графика
    st.plotly_chart(fig2)
    # Вывод графика
    st.plotly_chart(fig)

    # Указать ненужные столбцы
    columns_to_drop = ['debit_turnover_target_usd', 'credit_turnover_target_usd']
    st.write(balance_messages[language]["turnovers"])
    st.write(data.drop(columns=columns_to_drop))


async def get_plot_by_companies(language, data):
    st.title(balance_messages[language]["by_company"])
    st.write(balance_messages[language]["graph"])
    min_balance_usd = 1000
    # Удаление строк с абсолютным значением balance_usd меньше min_absolute_balance_usd
    data_for_graph = data.query(f'abs(balance_usd) >= {min_balance_usd}')

    # data_for_graph = data.query(f'balance_usd >= {min_balance_usd}')

    # Визуализация с помощью plotly.subplots
    fig = sp.make_subplots(rows=1, cols=2, specs=[[{'type': 'pie'}, {'type': 'pie'}]],
                           subplot_titles=balance_messages[language]["subplot_titles"])

    # By tl
    trace_product = (px.pie(
        data_for_graph.query('company_id != "Total"'),
        values='debit_turnover_target_usd',
        names='company_id',
        hole=0.2,
        color_discrete_sequence=px.colors.qualitative.Set1,
    )).update_traces(name=balance_messages[language]["debit_usd"])
    fig.add_trace(trace_product.data[0], row=1, col=1)

    # By usd
    trace_product = (px.pie(
        data_for_graph.query('company_id != "Total"'),
        values='credit_turnover_target_usd',
        names='company_id',
        hole=0.2,
        color_discrete_sequence=px.colors.qualitative.Vivid,
    )).update_traces(name=balance_messages[language]["credit_usd"])
    fig.add_trace(trace_product.data[0], row=1, col=2)

    fig.update_layout()

    # Визуализация с помощью plotly.express
    fig2 = px.bar(
        data_for_graph.query('company_id != "Total"'),
        x='company_id',
        y=['balance_usd'],
        barmode='group',
        color_discrete_sequence=['green'],
        labels={'balance_usd': 'Баланс'},
        title=balance_messages[language]["Balance per company"]
    )

    # Вывод графика
    st.plotly_chart(fig2)
    # Вывод графика
    st.plotly_chart(fig)

    # Указать ненужные столбцы
    columns_to_drop = ['debit_turnover_target_usd', 'credit_turnover_target_usd', 'company_name']
    st.write(balance_messages[language]["turnovers"])
    st.write(data.drop(columns=columns_to_drop))
