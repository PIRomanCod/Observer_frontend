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
from api_pages.src.balances_pages import get_transaction_by_id, get_transaction_by_company, get_transactions_by_period, \
    calculate_balance, get_turnovers, get_tables, get_plot_by_category, get_plot_by_companies, get_rate_by_date, \
    get_debit_credit_tables, get_plot_by_separated_category, get_plot_by_separated_companies
# from pages.src.auth_services import load_token, save_tokens, FILE_NAME
from api_pages.src.user_footer import footer
from api_pages.src.messages import balance_messages



# st.set_page_config(page_title="Deals",
#                    page_icon=":bar_chart:")


# cookie_manager = stx.CookieManager()
# cookies = cookie_manager.get_all()

#
# menu_data = [
#     {'id': 'english_name', 'label': "english"},
#     {'id': 'ukrainian_name', 'label': "українська"},
#     {'id': 'russian_name', 'label': "русский"},
#     {'id': 'turkish_name', 'label': "türkçe"},
# ]
#
# menu_id = hc.nav_bar(
#     menu_definition=menu_data,
#     first_select=0,
#     key="stock_nav",
#     home_name=None,
#     login_name={'id': "login_name", 'label': st.session_state.get("username", None), 'icon': "fa fa-user-circle", 'ttip': "username"},
#     override_theme={'txc_inactive': 'white', 'menu_background': 'green', 'txc_active': 'yellow',
#                     'option_active': 'blue'},
#     sticky_nav=True,
#     force_value=None,
#     use_animation=True,
#     hide_streamlit_markers=True,
#     sticky_mode=None,
#     option_menu=True)


async def run_balances_app():
    footer()
    access_token, refresh_token = None, None

    # access_token, refresh_token = cookies.get("access_token"), cookies.get("refresh_token")
    # st.write(access_token)
    # access_token, refresh_token = load_token(FILE_NAME)
    # refresh_token = st.session_state["refresh_token"]
    access_token = st.session_state.get("access_token", "")
    # if access_token:
    # st.write(refresh_token)
    # language = menu_id
    language = st.session_state.get("selected_language", "english_name")

    st.sidebar.title(balance_messages[language]["title"])
    page = st.sidebar.selectbox(balance_messages[language]["Choose action"],
                                [balance_messages[language]["Balance per period"],
                                 balance_messages[language]["Balance per company"],
                                balance_messages[language]["Total balance"],

                                 ]
                                )

    if page == balance_messages[language]["Balance per company"]:
        try:
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
        except KeyError:
            st.write("ReLogin")
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
            response = get_company_by_id(access_token, "")
            if response.get("items", 0):
                companies = response["items"]
                exchange_rate = await get_rate_by_date(language, access_token, end_date)
                if type(exchange_rate) == str:
                    st.write(balance_messages[language]["empty"])
                else:
                    exchange_rate = exchange_rate["usd_tl_rate"]
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
                    positive_company_balances = positive_company_balances.query('balance_usd != 0').dropna(subset=['balance_usd'])
                    # Замена company_id на имена компаний
                    negative_company_balances['company_name'] = negative_company_balances['company_id'].replace(
                        {company['id']: company['company_name'] for company in companies}, inplace=True)
                    negative_company_balances = negative_company_balances.query('balance_usd != 0').dropna(subset=['balance_usd'])

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

    elif page == balance_messages[language]["Total balance"]:
        end_date = pd.to_datetime(f"2023-12-31")
        response = get_company_by_id(access_token, "")
        if response.get("items", 0):
            companies = response["items"]
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
        else:
            st.write("ReLogin")
    # else:
    #     auth_manager.refresh_token_in_background()
    #     access_token, refresh_token = auth_manager.get_tokens()
    #     st.session_state["refresh_token"] = refresh_token
    #     st.session_state["access_token"] = access_token
    # save_tokens(access_token, refresh_token)


if __name__ == '__main__':
    # run_app()
    asyncio.run(run_balances_app())