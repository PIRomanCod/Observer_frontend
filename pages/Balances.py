from datetime import date, timedelta
import time

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

from pages.src.company_pages import get_company_by_id
from pages.src.goods_pages import get_goods_by_id
from pages.src.balances_pages import get_transaction_by_id, get_transaction_by_company, get_transactions_by_period, \
    calculate_balance, get_turnovers, get_tables, get_plot_by_category, get_plot_by_companies, get_rate_by_date
from pages.src.auth_services import load_token, save_token, FILE_NAME
from pages.src.user_footer import footer
from pages.src.messages import balance_messages

from pages.src.get_stocks_data import get_product_data


st.set_page_config(page_title="Deals",
                   page_icon=":bar_chart:")


menu_data = [
    {'id': 'english_name', 'label': "english"},
    {'id': 'ukrainian_name', 'label': "українська"},
    {'id': 'russian_name', 'label': "русский"},
    {'id': 'turkish_name', 'label': "türkçe"},
]

menu_id = hc.nav_bar(
    menu_definition=menu_data,
    first_select=0,
    key=None,
    home_name=None,
    login_name=None,
    override_theme={'txc_inactive': 'white', 'menu_background': 'green', 'txc_active': 'yellow',
                    'option_active': 'blue'},
    sticky_nav=True,
    force_value=None,
    use_animation=True,
    hide_streamlit_markers=True,
    sticky_mode=None,
    option_menu=True)


async def run_app():
    footer()
    access_token, refresh_token = None, None
    access_token, refresh_token = load_token(FILE_NAME)
    language = menu_id
    st.sidebar.title(balance_messages[language]["title"])
    page = st.sidebar.selectbox(balance_messages[language]["Choose action"],
                                [balance_messages[language]["Balance per company"],
                                balance_messages[language]["Total balance"],
                                balance_messages[language]["Balance per period"],

                                 ]
                                )

    if page == balance_messages[language]["Balance per company"]:
        selected_company = st.selectbox(balance_messages[language]["choose"], get_company_by_id(access_token, "")["items"], key="Companies")
        company_name = selected_company["company_name"]
        company_id = selected_company["id"]

        if st.button("GO"):
            with hc.HyLoader('Now doing loading, wait please', hc.Loaders.pulse_bars):
                time.sleep(1)
            result = await get_transaction_by_company(language, access_token, company_id)
            balance_tl, balance_usd = await calculate_balance(result)
            st.write(f"{balance_messages[language]['current balance']} {company_name.capitalize()} : {balance_tl} TL")
            st.write(f"{balance_messages[language]['current balance']} {company_name.capitalize()} : {balance_usd} USD")

    elif page == balance_messages[language]["Balance per period"]:
        with st.sidebar:
            # Вибір місяця та року користувачем
            selected_month = st.selectbox(balance_messages[language]["Choose month"], list(calendar.month_name)[1:])
            selected_year = st.selectbox(balance_messages[language]["Choose year"], range(2020, 2024))
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
            companies = get_company_by_id(access_token, "")["items"]
            exchange_rate = await get_rate_by_date(language, access_token, end_date)
            if type(exchange_rate) == str:
                st.write(balance_messages[language]["empty"])
            else:
                exchange_rate = exchange_rate["usd_tl_rate"]

                # Замена company_id на имена компаний
                balances = await get_transactions_by_period(language, access_token, start_date, end_date)

                balance_by_category, balance_by_companies = await get_tables(exchange_rate, balances)

                balance_by_companies['company_name'] = balance_by_companies['company_id'].replace(
                    {company['id']: company['company_name'] for company in companies}, inplace=True)

                # Удаление строк с balance_usd равным 0 или отсутствующим
                balance_by_companies = balance_by_companies.query('balance_usd != 0').dropna(subset=['balance_usd'])
                st.write(balance_messages[language]["exchange_rate"], exchange_rate)
                await get_plot_by_companies(language, balance_by_companies)
                await get_plot_by_category(language, balance_by_category)

    elif page == balance_messages[language]["Total balance"]:
        end_date = pd.to_datetime(f"2023-11-30")
        companies = get_company_by_id(access_token, "")["items"]
        exchange_rate = await get_rate_by_date(language, access_token, end_date)
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

    save_token(access_token, refresh_token)


if __name__ == '__main__':
    # run_app()
    asyncio.run(run_app())