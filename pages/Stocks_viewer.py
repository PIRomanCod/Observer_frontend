import pickle
import time
from datetime import date, timedelta

import hydralit_components as hc
import pandas as pd
import plotly.express as px
import streamlit as st
from pages.src.auth_services import FILE_NAME
from pages.src.get_stocks_data import post_stocks_data, get_product_data
from pages.src.user_footer import footer
from pages.src.messages import stock_messages as messages, seeded_id, languages_id
from pages.src.general_services import get_query_params, get_db_data


st.set_page_config(page_title="Stocks",
                   page_icon=":articulated_lorry:")

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


def main(access_token, language):
    with st.sidebar:

        selected_products = st.multiselect(messages[language]["goods"], get_product_data(language, access_token),
                                           key="Products")
        date_or_dynamic = st.radio(messages[language]["type"], [messages[language]["dynamic"],
                                                                messages[language]["day"],
                                                                ], key="Dynamic")

    if date_or_dynamic == messages[language]["dynamic"]:
        with st.sidebar:
            start_date = st.date_input(messages[language]["start date"],
                                       min_value=date(2019, 12, 17),
                                       max_value=date.today(), value=pd.to_datetime(date.today()-timedelta(days=30)))
            end_date = st.date_input(messages[language]["end date"], min_value=date(2019, 12, 17),
                                     max_value=date.today(), value=date.today())
        parameters = get_query_params(language, selected_products, start_date, end_date)
        if st.sidebar.button("GO"):
            data_from_db = get_db_data(access_token, parameters)
            # a dedicated single loader
            with hc.HyLoader('Now doing loading, wait please', hc.Loaders.pulse_bars):
                time.sleep(1)
            if data_from_db:
                for entry in data_from_db:
                    entry['product'] = entry['product']['name']

                df = pd.DataFrame(data_from_db)
                # st.write(df)

                # Побудова графіка
                fig = px.line(df, x='date', y='quantity', color='product', title=messages[language]["dynamic graf title"])
                st.plotly_chart(fig)
            else:
                st.write(messages[language]["empty data"])

    if date_or_dynamic == messages[language]["day"]:
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


def run_app():
    footer()
    access_token = None
    with open(FILE_NAME, "rb") as fh:
        access_token, refresh_token = pickle.load(fh)

    if access_token:
        language = menu_id
        st.write(messages[language]["about"])
        st.text(messages[language]["instruction"])
        main(access_token, language)
    else:
        st.write("Please LogIn to continue")


if __name__ == '__main__':
    run_app()
