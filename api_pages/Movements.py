from datetime import date, timedelta
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
from api_pages.src.movements_pages import get_movements_by_multifilter, get_accounts, get_chart, get_total, \
    get_movements_by_bank, get_sankey_chart
from api_pages.src.user_footer import footer
from api_pages.src.messages import movements_messages, stock_messages


async def run_movements_app():
    footer()
    access_token, refresh_token = None, None
    access_token = st.session_state.get("access_token", "")
    language = st.session_state.get("selected_language", "english_name")

    user_level = st.session_state["role"]
    if user_level == "admin":
        st.title("!!!You can edit data!!!")

    st.sidebar.title(movements_messages[language]["title"])
    page = st.sidebar.selectbox(movements_messages[language]["Choose action"],
                                [movements_messages[language]["Rests for now"],
                                 movements_messages[language]["All for period"],
                                 movements_messages[language]["Movements by bank"]
                                 ]
                                )

    if page == movements_messages[language]["Rests for now"]:
        if st.button("GO"):
            try:
                with hc.HyLoader('Now doing loading, wait please', hc.Loaders.pulse_bars):
                    time.sleep(1)

                result = await get_movements_by_multifilter(language, access_token)
                st.write(await get_total(language, result))
                await get_chart(language, result)
                st.write(movements_messages[language]["Details"])
                st.write(result)
            except TypeError:
                st.write("ReLogin")

    elif page == movements_messages[language]["All for period"]:
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
        except KeyError:
            st.write(stock_messages[language]["empty data"])

    elif page == movements_messages[language]["Movements by bank"]:
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
        except KeyError:
            st.write(stock_messages[language]["empty data"])


if __name__ == '__main__':
    asyncio.run(run_movements_app())