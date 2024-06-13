from datetime import date, timedelta, datetime
import time
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
from api_pages.src.movements_pages import (get_movements_by_multifilter, get_accounts, get_chart, get_total,
                                           get_movements_by_bank, get_sankey_chart, upload_csv,
                                           get_movements_by_period, get_movement_by_id, update_movement,
                                           create_movement, delete_movement)

from api_pages.src.user_footer import footer
from api_pages.src.messages import movements_messages, stock_messages, deals_messages


async def get_rest(language, access_token):
    if st.button("GO"):
        try:
            with hc.HyLoader('Now doing loading, wait please', hc.Loaders.pulse_bars):
                time.sleep(1)

            result = await get_movements_by_multifilter(language, access_token)
            st.write(await get_total(language, result))
            await get_chart(language, result)
            st.write(movements_messages[language]["Details"])
            st.write(result)
        except TypeError as error:
            st.write("ReLogin", error)

async def get_all(language, access_token):
    with st.sidebar:
        start_date = st.date_input(stock_messages[language]["start date"],
                                   min_value=date(2024, 1, 1),
                                   max_value=date.today(), value=pd.to_datetime(date.today() - timedelta(days=10)))
        end_date = st.date_input(stock_messages[language]["end date"], min_value=date(2024, 1, 1),
                                 max_value=date.today(), value=date.today())

        threshold = st.slider(movements_messages[language]["Threshold for tl"], 0, 100000, 5000)
        show_self = st.radio(movements_messages[language]["Show self movements?"], [False, True], key="Self")

        params = {
            "offset": 0,
            "limit": 2000,
            "start_date": start_date,
            "end_date": end_date,
        }
    try:
        result = await get_movements_by_bank(language, access_token, params)
        await get_sankey_chart(language, result, access_token, threshold, show_self)
    except KeyError as error:
        st.write(stock_messages[language]["empty data"], error)

async def get_one(language, access_token):
    with st.sidebar:
        banks = await get_accounts(access_token)
        # Обрані ключі, які вам потрібні
        selected_keys = ["id", "name"]

        # Застосування фільтру до кожного словника у списку
        filtered_banks = [{key: value for key, value in dct.items() if key in selected_keys} for dct in
                          banks]

        selected_payment_way = st.selectbox(movements_messages[language]["Payment_way"], filtered_banks,
                                            key="Payment_way")
        # st.write(selected_payment_way)
        start_date = st.date_input(stock_messages[language]["start date"],
                                   min_value=date(2024, 1, 1),
                                   max_value=date.today(), value=pd.to_datetime(date.today() - timedelta(days=10)))
        end_date = st.date_input(stock_messages[language]["end date"], min_value=date(2024, 1, 1),
                                 max_value=date.today(), value=date.today())

        threshold = st.slider(movements_messages[language]["Threshold for tl"], 0, 100000, 5000)
        show_self = st.radio(movements_messages[language]["Show self movements?"], [False, True], key="Self")

        params = {
            "offset": 0,
            "limit": 2000,
            "start_date": start_date,
            "end_date": end_date,
            "payment_way": selected_payment_way.get("id", None)
        }
    try:
        result = await get_movements_by_bank(language, access_token, params)
        await get_sankey_chart(language, result, access_token, threshold, show_self)
    except KeyError as error:
        st.write(stock_messages[language]["empty data"], error)


async def upload_csv_ui(acc_token):
    with st.expander("Upload CSV File", expanded=False):
        uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
        if uploaded_file is not None:
            if st.button("Upload"):
                progress_bar = st.progress(0)
                status_text = st.empty()
                for percent_complete in range(100):
                    time.sleep(0.1)  # Штучна затримка для симуляції завантаження
                    progress_bar.progress(percent_complete + 1)
                    status_text.text(f"Uploading... {percent_complete + 1}%")

                # Завантажуємо файл на сервер та отримуємо відповідь
                response = await upload_csv(uploaded_file, acc_token)

                status_text.text("Upload complete!")
                st.write(response.json())

async def get_movements(access_token, language):
    with st.expander("Get movements for period", expanded=False):
        # Формування початкової та кінцевої дати
        start_date = st.date_input(
            "Start Date",
            min_value=date(2024, 1, 1),
            max_value=date.today(),
            value=pd.to_datetime(date.today() - timedelta(days=30))
        )

        end_date = st.date_input(
            "End Date",
            min_value=date(2024, 1, 1),
            max_value=date.today(),
            value=pd.to_datetime(date.today())
        )

        if st.button("Fetch Movements Data"):
            data = await get_movements_by_period(start_date, end_date, access_token)
            st.write(data)
async def create_movements(access_token):
    with st.expander("Create Movement", expanded=False):
        template_id = st.number_input("Template Movement ID", min_value=1, step=1)

        if st.button("Fetch Template Data"):
            template_data = await get_movement_by_id(template_id, access_token)
            if isinstance(template_data, dict) and "error" not in template_data:
                st.session_state["template_data"] = template_data
            else:
                st.write(template_data)

        if "template_data" in st.session_state:
            template_data = st.session_state["template_data"]

            template_data["date"] = st.date_input("Date", value=datetime.strptime(template_data["date"],
                                                                                  '%Y-%m-%d').date() if isinstance(
                template_data["date"], str) else template_data["date"], key="temp id")
            template_data["operation_type"] = st.selectbox("Operation Type", ["debit", "credit"],
                                                           index=["debit", "credit"].index(
                                                               template_data["operation_type"]), key="temp type")
            template_data["company_id"] = st.number_input("Company ID", value=template_data["company_id"], key="temp company_id")
            template_data["description"] = st.text_area("Description", value=template_data.get("description", ""), key="temp description")
            template_data["account_type"] = st.text_input("Account Type", value=template_data["account_type"], key="temp account_type")
            template_data["currency"] = st.text_input("Currency", value=template_data["currency"], key="temp currency")
            template_data["sum"] = st.number_input("Sum", value=template_data["sum"], step=0.01, key="temp sum")
            template_data["payment_way"] = st.number_input("Payment Way", value=template_data["payment_way"], key="temp way")
            template_data["user_id"] = st.number_input("User ID", value=template_data["user_id"], key="temp user_id")

            if st.button("Create Movement"):
                movement_data = {
                    "date": template_data["date"].isoformat() if isinstance(template_data["date"], date) else
                    template_data["date"],
                    "company_id": template_data["company_id"],
                    "description": template_data["description"],
                    "account_type": template_data["account_type"],
                    "operation_type": template_data["operation_type"],
                    "currency": template_data["currency"],
                    "sum": template_data["sum"],
                    "payment_way": template_data["payment_way"],
                    "user_id": template_data["user_id"]
                }
                result = await create_movement(movement_data, access_token)
                st.write(result)

async def update_movements(acc_token):
    with st.expander("Edit Movement", expanded=False):
        movement_id = st.number_input("Enter Movement ID", min_value=1, step=1)

        if st.button("Fetch Movement Data"):
            movement_data = await get_movement_by_id(movement_id, acc_token)
            if isinstance(movement_data, dict):
                st.session_state["movement_data"] = movement_data
            else:
                st.write(movement_data)

        if "movement_data" in st.session_state:
            movement_data = st.session_state["movement_data"]

            movement_data["date"] = st.date_input("Date", value=datetime.strptime(movement_data["date"], '%Y-%m-%d').date() if isinstance(movement_data["date"], str) else movement_data["date"])
            movement_data["company_id"] = st.number_input("Company ID", value=movement_data["company_id"])
            movement_data["description"] = st.text_area("Description", value=movement_data.get("description", ""))
            movement_data["account_type"] = st.text_input("Account Type", value=movement_data["account_type"])
            movement_data["operation_type"] = st.selectbox("Operation Type", ["debit", "credit"],
                                                           index=["debit", "credit"].index(movement_data["operation_type"]))
            movement_data["currency"] = st.text_input("Currency", value=movement_data["currency"])
            movement_data["sum"] = st.number_input("Sum", value=movement_data["sum"], step=0.01)
            movement_data["payment_way"] = st.number_input("Payment Way", value=movement_data["payment_way"])
            movement_data["user_id"] = st.number_input("User ID", value=movement_data["user_id"])

            if st.button("Update Movement"):
                # Перетворення дати у строку
                if isinstance(movement_data["date"], date):
                    movement_data["date"] = movement_data["date"].isoformat()
                result = await update_movement(movement_id, movement_data, acc_token)
                st.write(result)

async def delete_movements(access_token):
    with st.expander("Delete Movement", expanded=False):
        movement_id = st.number_input("Enter Movement ID to delete", min_value=1, step=1)

        if st.button("Delete Movement"):
            result = await delete_movement(movement_id, access_token)
            st.write(result)

async def movements_crud(access_token, language):
    await get_movements(access_token, language)
    await update_movements(access_token)
    await create_movements(access_token)
    await delete_movements(access_token)
    await upload_csv_ui(access_token)

async def run_movements_app():
    footer()
    access_token, refresh_token = None, None
    access_token = st.session_state.get("access_token", "")
    language = st.session_state.get("selected_language", "english_name")

    user_level = st.session_state["role"]
    if user_level == "admin":
        st.write("!!!You can edit the data!!!")
        await movements_crud(access_token, language)


    st.sidebar.title(movements_messages[language]["title"])
    page = st.sidebar.selectbox(movements_messages[language]["Choose action"],
                                [movements_messages[language]["Rests for now"],
                                 movements_messages[language]["All for period"],
                                 movements_messages[language]["Movements by bank"]
                                 ]
                                )

    if page == movements_messages[language]["Rests for now"]:
        await get_rest(language, access_token)

    elif page == movements_messages[language]["All for period"]:
        await get_all(language, access_token)

    elif page == movements_messages[language]["Movements by bank"]:
        await get_one(language, access_token)

if __name__ == '__main__':
    asyncio.run(run_movements_app())