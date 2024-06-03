import pickle
import time
from datetime import date, timedelta
# import extra_streamlit_components as stx
import asyncio

import hydralit_components as hc
import pandas as pd
import plotly.express as px
import streamlit as st
# from pages.src.auth_services import FILE_NAME
from api_pages.src.get_stocks_data import (post_stocks_data, get_product_data, del_stocks_by_date,
                                           create_new_stock_note, upload_file_to_server)
from api_pages.src.user_footer import footer
from api_pages.src.messages import stock_messages as messages, seeded_id, languages_id
from api_pages.src.general_services import get_query_params, get_db_data

#
# st.set_page_config(page_title="Stocks",
#                    page_icon=":articulated_lorry:")

#
# cookie_manager = stx.CookieManager()
# cookies = cookie_manager.get_all()


#
# menu_data = [
#     {'id': 'english_name', 'label': "english", 'icon': ":flag-gb:"},
#     {'id': 'ukrainian_name', 'label': "українська"},
#     {'id': 'russian_name', 'label': "русский"},
#     {'id': 'turkish_name', 'label': "türkçe", 'icon': ":flag-tr:"},
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
async def add_stocks(access_token, language):
    with st.expander("Add new stock report", expanded=False):
        data = {}
        data["date"] = st.date_input(messages[language]["start date"],
                                               min_value=date(2019, 12, 17),
                                               max_value=date.today(), value=pd.to_datetime(date.today()-timedelta(days=30)), key="stock date")
        data["product_id"] = st.text_input(label="product_id", key="product_id")
        data["quantity"] = st.number_input(label="quantity", key="quantity")
        if st.button("GO", key="stock go"):
            create_new_stock_note(data, access_token)

async def del_stocks(access_token, language):
    with st.expander("Delete notes for date", expanded=False):
        data = st.date_input(messages[language]["start date"],
                                               min_value=date(2019, 12, 17),
                                               max_value=date.today(), value=pd.to_datetime(date.today()-timedelta(days=30)), key="delete stock date")

        if st.button("GO", key="del_stock go"):
            del_stocks_by_date(data, access_token)

async def upload_csv_file(access_token):
    with st.expander("Upload CSV file to load stocks", expanded=False):
        uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

        if uploaded_file is not None:
            if st.button("Upload"):
                response = upload_file_to_server(uploaded_file, access_token)
                st.write(response)

async def do_dynamic(selected_products, language, access_token):
    with st.sidebar:
        start_date = st.date_input(messages[language]["start date"],
                                   min_value=date(2019, 12, 17),
                                   max_value=date.today(), value=pd.to_datetime(date.today() - timedelta(days=30)))
        end_date = st.date_input(messages[language]["end date"], min_value=date(2019, 12, 17),
                                 max_value=date.today(), value=date.today())
    parameters = get_query_params(language, selected_products, start_date, end_date)
    if st.sidebar.button("GO"):
        data_from_db = get_db_data(access_token, parameters)
        # st.write(data_from_db)
        # a dedicated single loader
        with hc.HyLoader('Now doing loading, wait please', hc.Loaders.pulse_bars):
            time.sleep(1)
        if data_from_db:
            for entry in data_from_db:
                entry['product'] = entry['product']['name']

            df = pd.DataFrame(data_from_db)
            # st.write(df)

            # Побудова графіка
            fig = px.line(df, x='date', y='quantity', color='product', title=messages[language]["dynamic graf title"],
                            labels={
                                'date': 'Date',
                                'quantity': 'Quantity',
                                'product': 'Product'
                            },
                            text='quantity')
            # Налаштування осі Y для відображення кількості
            fig.update_traces(textposition='top center')
            fig.update_yaxes(tickprefix="", title="Quantity")

            st.plotly_chart(fig)
        else:
            st.write(messages[language]["empty data"])


async def do_day_statistic(selected_products, language, access_token):
    with st.sidebar:
        chosen_date = st.date_input(messages[language]["one date"], min_value=date(2019, 12, 17),
                                    max_value=date.today(), value=pd.to_datetime(date.today()))
    if st.sidebar.button("GO"):
        data_from_db = None
        spinner = hc.HyLoader('Now doing loading, wait please', hc.Loaders.pulse_bars)
        while not data_from_db:
            with spinner:
                time.sleep(1)
            parameters = get_query_params(language, selected_products, chosen_date, chosen_date)
            data_from_db = get_db_data(access_token, parameters)

            if not data_from_db:
                st.write(messages[language]["empty data"])
                break

            # Get data for the previous date
            previous_date = chosen_date - timedelta(days=1)
            previous_date_params = get_query_params(language, selected_products, previous_date, previous_date)
            previous_date_data = get_db_data(access_token, previous_date_params)

            while not previous_date_data:
                previous_date = previous_date - timedelta(days=1)
                previous_date_params = get_query_params(language, selected_products, previous_date, previous_date)
                previous_date_data = get_db_data(access_token, previous_date_params)

            if previous_date_data:
                # Комбінуємо дані для вибраної дати та попередньої дати
                combined_data = pd.concat([pd.DataFrame(data_from_db), pd.DataFrame(previous_date_data)])

                # Розпаковка словника 'product' у окремі стовпці
                combined_data[['id', 'name']] = combined_data['product'].apply(pd.Series)

                # Видалення старого стовпця 'product'
                combined_data = combined_data.drop('product', axis=1)

                # Сортування за датою
                combined_data = combined_data.sort_values(by='date')

                # Створення стовбця з різницею кількості товару між поточним та попереднім днем
                combined_data['quantity_difference'] = combined_data.groupby('name')['quantity'].diff()
                combined_data = combined_data[combined_data['date'] == str(chosen_date)]
                combined_data = combined_data[['date', 'name', 'quantity', 'quantity_difference']]

                # Створіть словник з назвами стовпців для кожної мови
                column_names = {
                    'date': messages[language]["date"],
                    'name': messages[language]["name"],
                    'quantity': messages[language]["quantity"],
                    'quantity_difference': f'{messages[language]["quantity_difference"]} {previous_date}'
                }

                # Перейменуйте стовпці відповідно до словника
                combined_data = combined_data.rename(columns=column_names)

                # Вивід результатів
                st.write(messages[language]["daily table title"], combined_data)

                # Побудова кругової діаграми
                fig = px.pie(
                    combined_data,
                    values=messages[language]["quantity"],
                    names=messages[language]["name"],
                    hole=0.2,
                    color_discrete_sequence=px.colors.qualitative.Vivid
                )
                st.plotly_chart(fig)

async def main(access_token, language):
    try:
        with st.sidebar:

            selected_products = st.multiselect(messages[language]["goods"], get_product_data(language, access_token),
                                               key="Products")
            date_or_dynamic = st.radio(messages[language]["type"], [messages[language]["dynamic"],
                                                                    messages[language]["day"],
                                                                    ], key="Dynamic")

        if date_or_dynamic == messages[language]["dynamic"]:
            await do_dynamic(selected_products, language, access_token)

        if date_or_dynamic == messages[language]["day"]:
            await do_day_statistic(selected_products, language, access_token)

        user_level = st.session_state["role"]
        if user_level == "admin":
            st.write("!!!You can edit the data: load from file, delete, etc.!!!")
            await add_stocks(access_token, language)
            await del_stocks(access_token, language)
            await upload_csv_file(access_token)

    except TypeError as err:
        st.write("ReLogin", err)

async def run_stocks_app():
    footer()
    access_token = None
    # with open(FILE_NAME, "rb") as fh:
    #     access_token, refresh_token = pickle.load(fh)
    # access_token, refresh_token = cookies.get("access_token"), cookies.get("refresh_token")
    access_token = st.session_state.get("access_token", "")
    if access_token:
        # language = menu_id
        language = st.session_state.get("selected_language", "english_name")

        st.write(messages[language]["about"])
        st.text(messages[language]["instruction"])
        await main(access_token, language)
    else:
        st.write("Please LogIn to continue")


if __name__ == '__main__':
    asyncio.run(run_stocks_app())
