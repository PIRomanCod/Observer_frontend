from datetime import date, timedelta, datetime
import time
from decimal import Decimal

import extra_streamlit_components as stx

import pandas as pd
import calendar
import matplotlib.pyplot as plt
import seaborn as sns

import plotly.express as px
import plotly.subplots as sp
import plotly.graph_objects as go
import asyncio

import streamlit as st
import hydralit_components as hc

from api_pages.src.company_pages import get_company_by_id
from api_pages.src.balances_pages import (get_transaction_by_id, get_transaction_by_company, get_transactions_by_period,
                                          calculate_balance, get_turnovers, get_tables, get_plot_by_category,
                                          get_plot_by_companies, get_rate_by_date, get_debit_credit_tables,
                                          get_plot_by_separated_category, get_plot_by_separated_companies,
                                          create_exch_rate_api, delete_exch_rate_api, upload_csv_api, create_transaction_api,
                                          delete_transaction_api, update_transaction_api, upload_csv_transaction_api,
                                          get_transaction_by_id_for_update)
# from pages.src.auth_services import load_token, save_tokens, FILE_NAME
from api_pages.src.user_footer import footer
from api_pages.src.messages import balance_messages


async def company_balance(language, access_token):
    try:
        selected_company = st.selectbox(balance_messages[language]["choose"],
                                        get_company_by_id(access_token, "")["items"], key="Companies")
        company_name = selected_company["company_name"]
        company_id = selected_company["id"]

        if st.button("GO"):
            with hc.HyLoader('Now doing loading, wait please', hc.Loaders.pulse_bars):
                time.sleep(1)
            result = await get_transaction_by_company(language, access_token, company_id)
            balance_tl, balance_usd = await calculate_balance(result)
            st.write(f"{balance_messages[language]['current balance']} {company_name.capitalize()} : {balance_tl} TL")
            st.write(f"{balance_messages[language]['current balance']} {company_name.capitalize()} : {balance_usd} USD")
            transaction_list = pd.DataFrame(result["items"])
            columns_to_drop = ['eur_usd_rate', 'usd_tl_rate', 'is_deleted', 'user_id',
                               'accounting_type', 'document_type', 'operation_region']
            st.write(transaction_list.drop(columns=columns_to_drop))

    except KeyError as err:
        st.write(f"ReLogin {err}")

async def month_balance(language, access_token):
    with st.sidebar:
        # Вибір місяця та року користувачем
        selected_month = st.selectbox(balance_messages[language]["Choose month"], list(calendar.month_name)[1:])
        selected_year = st.selectbox(balance_messages[language]["Choose year"], range(2020, 2025))
        continiously = st.selectbox(balance_messages[language]["cumulative"], ["True", "False"])
        # Отримання числа місяця за його іменем
        month_number = list(calendar.month_name).index(selected_month)

        # Формування початкової та кінцевої дати

        start_date = pd.to_datetime(f"{selected_year}-{month_number:02d}-01")
        if continiously == "True":
            start_date = pd.to_datetime("2018-01-01")
        end_date = pd.to_datetime(
            f"{selected_year}-{month_number:02d}-{calendar.monthrange(selected_year, month_number)[1]}")

    if st.sidebar.button("GO"):
        with hc.HyLoader('Now doing loading, wait please', hc.Loaders.pulse_bars):
            time.sleep(1)
        response = get_company_by_id(access_token, "")
        if response.get("items", 0):
            companies = response["items"]
            while True:
                exchange_rate = await get_rate_by_date(language, access_token, end_date)
                # Check if exchange_rate exists for the current end_date
                if isinstance(exchange_rate, dict) and exchange_rate.get("usd_tl_rate") is not None:
                    break  # Exit the loop if exchange_rate exists for the current end_date
                # Move to the previous day
                end_date -= pd.Timedelta(days=1)

                # Add a check to prevent an infinite loop in case data is missing
                if end_date < pd.to_datetime("2023-01-01"):
                    break

            exchange_rate = exchange_rate["usd_tl_rate"]
            # exchange_rate = await get_rate_by_date(language, access_token, end_date)
            if type(exchange_rate) == str:
                st.write(balance_messages[language]["empty"])
            else:
                # exchange_rate = exchange_rate["usd_tl_rate"]
                # Получение данных из БД
                balances = await get_transactions_by_period(language, access_token, start_date, end_date)
                # Разделение данных по категориям и компаниям для анализа
                balance_by_category, balance_by_companies = await get_tables(exchange_rate, balances)
                # Углубленное разделение данных по категориям и компаниям для анализа
                positive_category_balances, negative_category_balances, positive_company_balances, negative_company_balances = \
                    await get_debit_credit_tables(exchange_rate, balances)
                # Замена company_id на имена компаний
                positive_company_balances['company_name'] = positive_company_balances['company_id'].replace(
                    {company['id']: company['company_name'] for company in companies}, inplace=True)
                positive_company_balances = positive_company_balances.query('balance_usd != 0').dropna(
                    subset=['balance_usd'])
                # Замена company_id на имена компаний
                negative_company_balances['company_name'] = negative_company_balances['company_id'].replace(
                    {company['id']: company['company_name'] for company in companies}, inplace=True)
                negative_company_balances = negative_company_balances.query('balance_usd != 0').dropna(
                    subset=['balance_usd'])

                # Удаление артефактов таблиц
                column_to_drop = ["company_name"]
                positive_company_balances = positive_company_balances.drop(columns=column_to_drop)
                negative_company_balances = negative_company_balances.drop(columns=column_to_drop)

                # Замена company_id на имена компаний
                balance_by_companies['company_name'] = balance_by_companies['company_id'].replace(
                    {company['id']: company['company_name'] for company in companies}, inplace=True)
                # Вывод курса
                st.write(balance_messages[language]["exchange_rate"], exchange_rate)

                # Вывод данных о дебиторской задолженности
                st.title(balance_messages[language]["recievbles"])
                await get_plot_by_separated_companies(language, positive_company_balances)
                await get_plot_by_separated_category(language, positive_category_balances)

                # Вывод данных о кредиторской задолженности
                st.title(balance_messages[language]["debts"])
                await get_plot_by_separated_companies(language, negative_company_balances)
                await get_plot_by_separated_category(language, negative_category_balances)

                # Удаление строк с balance_usd равным 0 или отсутствующим
                balance_by_companies = balance_by_companies.query('balance_usd != 0').dropna(subset=['balance_usd'])

                # Вывод данных об оборотах по дебиту и по кредиту
                await get_plot_by_companies(language, balance_by_companies)
                await get_plot_by_category(language, balance_by_category)

        else:
            # Отлавливание истечения срока токена
            st.write("ReLogin")

async def total_balance(language, access_token):
    current_date = pd.to_datetime("now")  # Set the current date
    end_date = current_date
    # end_date = pd.to_datetime(f"2023-12-31")
    response = get_company_by_id(access_token, "")
    if response.get("items", 0):
        companies = response["items"]
        while True:
            exchange_rate = await get_rate_by_date(language, access_token, end_date)
            # Check if exchange_rate exists for the current end_date
            if isinstance(exchange_rate, dict) and exchange_rate.get("usd_tl_rate") is not None:
                break  # Exit the loop if exchange_rate exists for the current end_date
            # Move to the previous day
            end_date -= pd.Timedelta(days=1)

            # Add a check to prevent an infinite loop in case data is missing
            if end_date < pd.to_datetime("2023-01-01"):
                break

        exchange_rate = exchange_rate["usd_tl_rate"]

        if st.button("GO"):
            with hc.HyLoader('Now doing loading, wait please', hc.Loaders.pulse_bars):
                time.sleep(1)
            balances = await get_turnovers(language, access_token)
            balance_by_category, balance_by_companies = await get_tables(exchange_rate, balances)

            # Замена company_id на имена компаний
            balance_by_companies['company_name'] = balance_by_companies['company_id'].replace(
                {company['id']: company['company_name'] for company in companies}, inplace=True)

            # Удаление строк с balance_usd равным 0 или отсутствующим
            balance_by_companies = balance_by_companies.query('balance_usd != 0').dropna(subset=['balance_usd'])
            st.write("exchange_rate", exchange_rate)
            await get_plot_by_companies(language, balance_by_companies)
            await get_plot_by_category(language, balance_by_category)
    else:
        st.write("Please LogIn to continue")

async def create_exch_rate_ui(access_token):
    with st.expander("Create Exchange Rate", expanded=False):
        date = st.date_input("Date", value=datetime.today())
        usd_tl_rate = st.number_input("USD to TL Rate", format="%.4f")
        eur_usd_rate = st.number_input("EUR to USD Rate", format="%.4f")

        if st.button("Create Exchange Rate"):
            rate_data = [
                {
                    "date": date.strftime("%Y-%m-%d"),
                    "usd_tl_rate": str(Decimal(usd_tl_rate)),
                    "eur_usd_rate": str(Decimal(eur_usd_rate)),
                }
            ]
            st.success(await create_exch_rate_api(access_token, rate_data))

async def delete_exch_rate_ui(access_token):
    with st.expander("Delete Exchange Rate", expanded=False):
        date = st.date_input("Date to Delete", value=datetime.today())

        if st.button("Delete Exchange Rate"):
            st.success(await delete_exch_rate_api(access_token, date))

async def upload_csv_ui(access_token):
    with st.expander("Upload Exchange Rates CSV", expanded=False):
        uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

        if uploaded_file:
            if st.button("Upload CSV"):
                st.success(await upload_csv_api(access_token, uploaded_file))

async def exrate_crud(access_token):
    await upload_csv_ui(access_token)
    await delete_exch_rate_ui(access_token)
    await create_exch_rate_ui(access_token)

async def delete_transaction_ui(access_token):
    with st.expander("Delete Transaction", expanded=False):
        transaction_id = st.number_input("Transaction ID", min_value=1, step=1)
        if st.button("Delete Transaction"):
            result = await delete_transaction_api(access_token, transaction_id)
            st.write(result)

async def create_transaction_ui(access_token):
    with st.expander("Create Transaction", expanded=False):
        transaction_data = {
            "date": st.date_input("Date", value=datetime.today()).strftime("%Y-%m-%d"),
            "expenses_category": st.selectbox("Expenses Category", ["buyer", "capital", "fixed", "interest", "investments",
                                                                    "old_debt", "invoice_job", "settlements", "variable", "other"]),
            "company_id": st.number_input("Company ID", min_value=1, step=1),
            "description": st.text_area("Description", value=""),
            "accounting_type": st.selectbox("Accounting Type", ["GR Baris", "ProOil"]),
            "operation_type": st.selectbox("Operation Type", ["debit", "credit"]),
            "document_type": st.selectbox("Document Type", ["payment", "invoice", "changes", "undefined"], index=3),
            "operation_region": st.selectbox("Operation Region", ["domestic", "export", "import"]),
            "currency": st.selectbox("Currency", ["tl", "eur", "usd"]),
            "sum": st.number_input("Sum", min_value=0.0, step=0.01),
            "usd_tl_rate": float(st.text_input("USD to TL Rate", value="0.0000")),
            "eur_usd_rate": float(st.text_input("EUR to USD Rate", value="0.0000")),
            "is_deleted": st.checkbox("Is Deleted"),
            "user_id": st.number_input("User ID", min_value=1, step=1)
        }

        if st.button("Create Transaction"):
            result = await create_transaction_api(access_token, transaction_data)
            st.write(result)

async def update_transaction_ui(access_token):
    with st.expander("Update Transaction", expanded=False):
        transaction_id = st.number_input("Transaction ID", min_value=1, step=1, key="delete id")
        if st.button("Fetch Transaction Data"):
            transaction_data = await get_transaction_by_id_for_update(transaction_id, access_token)
            if isinstance(transaction_data, dict):
                st.session_state["transaction_data"] = transaction_data
            else:
                st.write(transaction_data)

        if "transaction_data" in st.session_state:
            transaction_data = st.session_state["transaction_data"]

            transaction_data["date"] = st.date_input("Date", value=datetime.strptime(transaction_data["date"], '%Y-%m-%d').date() if isinstance(transaction_data["date"], str) else transaction_data["date"]).strftime("%Y-%m-%d")
            transaction_data["expenses_category"] = st.selectbox("Expenses Category", ["buyer", "capital", "fixed", "interest", "investments", "old_debt", "invoice_job", "settlements", "variable", "other"], index=["buyer", "capital", "fixed", "interest", "investments", "old_debt", "invoice_job", "settlements", "variable", "other"].index(transaction_data["expenses_category"]))
            transaction_data["company_id"] = st.number_input("Company ID", value=transaction_data["company_id"], min_value=1, step=1)
            transaction_data["description"] = st.text_area("Description", value=transaction_data["description"])
            transaction_data["accounting_type"] = st.selectbox("Accounting Type", ["GR Baris", "ProOil"], index=["GR Baris", "ProOil"].index(transaction_data["accounting_type"]))
            transaction_data["operation_type"] = st.selectbox("Operation Type", ["debit", "credit"], index=["debit", "credit"].index(transaction_data["operation_type"]), key="fetch operation_type")
            transaction_data["document_type"] = st.selectbox("Document Type", ["payment", "invoice", "changes", "undefined"], index=["payment", "invoice", "changes", "undefined"].index(transaction_data["document_type"] or "undefined"), key="document_type")
            transaction_data["operation_region"] = st.selectbox("Operation Region", ["domestic", "export", "import"], index=["domestic", "export", "import"].index(transaction_data["operation_region"]), key="fetch operation_region")
            transaction_data["currency"] = st.selectbox("Currency", ["tl", "eur", "usd"], index=["tl", "eur", "usd"].index(transaction_data["currency"]), key="fetch currency")
            transaction_data["sum"] = st.number_input("Sum", value=transaction_data["sum"], step=0.01)
            transaction_data["usd_tl_rate"] = float(st.text_input("USD to TL Rate", value=str(transaction_data["usd_tl_rate"])))
            transaction_data["eur_usd_rate"] = float(st.text_input("EUR to USD Rate", value=str(transaction_data["eur_usd_rate"])))
            transaction_data["is_deleted"] = st.checkbox("Is Deleted", value=transaction_data["is_deleted"], key="fetch is_deleted")
            transaction_data["user_id"] = st.number_input("User ID", value=transaction_data["user_id"], min_value=1, step=1)

            if st.button("Update Transaction"):
                result = await update_transaction_api(transaction_id, transaction_data, access_token)
                st.write(result)

async def load_csv_transaction_ui(access_token):
    with st.expander("Upload Transactions CSV", expanded=False):
        uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
        if uploaded_file:
            if st.button("Upload CSV"):
                result = await upload_csv_transaction_api(access_token, uploaded_file)
                st.write(result)

async def transaction_crud(language, access_token):
    await delete_transaction_ui(access_token)
    await create_transaction_ui(access_token)
    await update_transaction_ui(access_token)
    await load_csv_transaction_ui(access_token)


async def run_balances_app():
    footer()
    access_token, refresh_token = None, None
    access_token = st.session_state.get("access_token", "")

    language = st.session_state.get("selected_language", "english_name")

    st.sidebar.title(balance_messages[language]["title"])
    page = st.sidebar.selectbox(balance_messages[language]["Choose action"],
                                [balance_messages[language]["Balance per period"],
                                 balance_messages[language]["Balance per company"],
                                balance_messages[language]["Total balance"],

                                 ]
                                )

    if page == balance_messages[language]["Balance per company"]:
        await company_balance(language, access_token)
        user_level = st.session_state["role"]
        if user_level == "admin":
            st.write("!!!You can edit the data!!!")
            await transaction_crud(language, access_token)

    elif page == balance_messages[language]["Balance per period"]:
        await month_balance(language, access_token)


    elif page == balance_messages[language]["Total balance"]:
        user_level = st.session_state["role"]
        if user_level == "admin":
            st.write("!!!You can edit the data!!!")
            await exrate_crud(access_token)

        await total_balance(language, access_token)



if __name__ == '__main__':
    # run_app()
    asyncio.run(run_balances_app())