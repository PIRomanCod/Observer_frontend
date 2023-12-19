from datetime import date, timedelta
import time

import pandas as pd
import calendar
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.subplots as sp
import extra_streamlit_components as stx

import streamlit as st
import hydralit_components as hc

from api_pages.src.company_pages import get_company_by_id
from api_pages.src.goods_pages import get_goods_by_id
from api_pages.src.deals_pages import get_deal_by_id, get_deals_by_product, get_deals_by_company, get_deals_by_period
from api_pages.src.auth_services import load_token, save_tokens, FILE_NAME
from api_pages.src.user_footer import footer
from api_pages.src.messages import deals_messages

from api_pages.src.get_stocks_data import get_product_data


st.set_page_config(page_title="Deals",
                   page_icon=":bar_chart:")

# cookie_manager = stx.CookieManager()
# cookies = cookie_manager.get_all()

# menu_data = [
#     {'id': 'english_name', 'label': "english"},
#     {'id': 'ukrainian_name', 'label': "українська"},
#     {'id': 'russian_name', 'label': "русский"},
#     {'id': 'turkish_name', 'label': "türkçe"},
# ]
#
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
#

def get_plots(language, df_income_grouped, df_income_grouped_company, df_income_grouped_quantity):
    fig_income = sp.make_subplots(rows=1, cols=3, specs=[[{"type": "pie"}, {"type": "pie"}, {"type": "pie"}]],
                                  subplot_titles=deals_messages[language]["subplot_titles"])
    # By Product
    trace_product = (px.pie(
        df_income_grouped,
        values='sum_total_usd',
        names='product_name',
        hole=0.2,
        color_discrete_sequence=px.colors.qualitative.Vivid,
    )).update_traces(name='Товари, USD', legendgroup='group1', secondary_y=True)
    fig_income.add_trace(trace_product.data[0], row=1, col=1)

    # By Company
    trace_company = (px.pie(
        df_income_grouped_company,
        values='sum_total_usd',
        names='company_name',
        hole=0.2,
        color_discrete_sequence=px.colors.qualitative.Set1,
    )).update_traces(name='Компанії, USD', legendgroup='group2', secondary_y=True)
    fig_income.add_trace(trace_company.data[0], row=1, col=2)

    # By Quantity
    trace_quantity = (px.pie(
        df_income_grouped_quantity,
        values='quantity',
        names='product_name',
        hole=0.2,
        color_discrete_sequence=px.colors.qualitative.Vivid,
    )).update_traces(name='Товари, тн', legendgroup='group3', secondary_y=True)
    fig_income.add_trace(trace_quantity.data[0], row=1, col=3)

    # Налаштування легенди
    # fig_income.update_layout(legend=dict(orientation="h", yanchor="bottom", y=-2.5, xanchor="center", x=1))
    # fig_income.update_layout(legend=dict(orientation="h", yanchor="bottom", y=-2, xanchor="center", x=0.5))
    fig_income.update_layout(legend=dict(orientation="h", itemclick=False, itemdoubleclick=False))
    return fig_income


def run_deals_app():
    footer()
    access_token = None
    # access_token, refresh_token = load_token(FILE_NAME)
    # access_token, refresh_token = cookies.get("access_token"), cookies.get("refresh_token")
    # refresh_token = st.session_state.get("refresh_token", "")
    access_token = st.session_state.get("access_token", "")
    # language = menu_id
    language = st.session_state.get("selected_language", "english_name")

    st.sidebar.title(deals_messages[language]["title"])
    page = st.sidebar.selectbox(deals_messages[language]["Choose action"],
                                [deals_messages[language]["Monthly report"],
                                 deals_messages[language]["Company list"],]
                                )

    if page == deals_messages[language]["Company list"]:
        company_id = st.text_input("Enter id")
        if st.button("GO"):
            with hc.HyLoader('Now doing loading, wait please', hc.Loaders.pulse_bars):
                time.sleep(1)
            result = get_company_by_id(access_token, company_id)
            if result.get("401"):
                st.write("ReLogin")
            else:
                st.write(result)

    elif page == deals_messages[language]["Monthly report"]:
        with st.sidebar:
            # Вибір місяця та року користувачем
            selected_month = st.selectbox(deals_messages[language]["Choose month"], list(calendar.month_name)[1:])
            selected_year = st.selectbox(deals_messages[language]["Choose year"], range(2020, 2024))

            # Отримання числа місяця за його іменем
            month_number = list(calendar.month_name).index(selected_month)

            # Формування початкової та кінцевої дати
            start_date = pd.to_datetime(f"{selected_year}-{month_number:02d}-01")
            end_date = pd.to_datetime(
                f"{selected_year}-{month_number:02d}-{calendar.monthrange(selected_year, month_number)[1]}")

        if st.sidebar.button("GO"):
            with hc.HyLoader('Now doing loading, wait please', hc.Loaders.pulse_bars):
                time.sleep(1)
            try:
                result = get_deals_by_period(access_token, start_date, end_date)
                if len(result["items"]) > 1:
                # Побудова таблиці
                    df = pd.DataFrame(result["items"])

                    # Вибір лише деяких стовбців та зміна порядку
                    selected_columns = ["date", "product_id", "company_id", "quantity", "sum_total_tl", "sum_total_usd",
                                        "operation_type", "cost_per_mt_tl", "cost_per_mt_usd"]
                    df_selected = df[selected_columns]

                    # Зміна порядку стовбців
                    df_selected = df_selected[
                        ["date", "operation_type", "company_id", "product_id", "quantity", "sum_total_tl", "sum_total_usd",
                         "cost_per_mt_tl", "cost_per_mt_usd"]]

                    # Розділення даних за типом операції
                    df_income = df_selected[df_selected["operation_type"] == "income"]
                    df_outcome = df_selected[df_selected["operation_type"] == "outcome"]

                    df_income = df_income.drop("operation_type", axis=1)
                    df_outcome = df_outcome.drop("operation_type", axis=1)

                    # Отримання назв товарів та компаній
                    products_data = get_product_data("english_name", access_token)
                    products_dict = {product["id"]: product["name"] for product in products_data}
                    companies_data = {company["id"]: company["company_name"].capitalize() for company in
                                      get_company_by_id(access_token, "")["items"]}

                    # Заміна ідентифікаторів назвами в DataFrame
                    df_income["product_name"] = df_income["product_id"].map(products_dict)
                    df_income["company_name"] = df_income["company_id"].map(companies_data)

                    df_outcome["product_name"] = df_outcome["product_id"].map(products_dict)
                    df_outcome["company_name"] = df_outcome["company_id"].map(companies_data)

                    # Вибір лише деяких стовбців та зміна порядку
                    selected_columns_2 = ["date", "product_name", "company_name", "quantity", "sum_total_tl", "sum_total_usd",
                                        "cost_per_mt_usd"]
                    df_income = df_income[selected_columns_2]
                    df_outcome = df_outcome[selected_columns_2]

                    # Зміна порядку стовбців
                    df_income = df_income[["date", "company_name", "product_name", "quantity", "sum_total_tl", "sum_total_usd",
                         "cost_per_mt_usd"]]
                    df_outcome = df_outcome[["date", "company_name", "product_name", "quantity", "sum_total_tl", "sum_total_usd",
                         "cost_per_mt_usd"]]

                    # Додати новий стовбець для середньозваженої ціни

                    # Обчисліть загальну вартість та загальну вагу для кожного товару
                    total_cost_in = df_income.groupby('product_name')['sum_total_usd'].sum().reset_index()
                    total_weights_in = df_income.groupby('product_name')['quantity'].sum().reset_index()
                    # Злиття двох датафреймів по назві товару
                    merged_df_income = pd.merge(total_cost_in, total_weights_in, on='product_name', suffixes=('_cost', '_weight'))
                    # Додати новий стовпець для середньозваженої ціни
                    merged_df_income['avg_price, usd'] = merged_df_income['sum_total_usd'] / merged_df_income['quantity']

                    # Обчисліть загальну вартість та загальну вагу для кожного товару
                    total_cost_out = df_outcome.groupby('product_name')['sum_total_usd'].sum().reset_index()
                    total_weights_out = df_outcome.groupby('product_name')['quantity'].sum().reset_index()
                    # Злиття двох датафреймів по назві товару
                    merged_df_outcome = pd.merge(total_cost_out, total_weights_out, on='product_name',
                                                 suffixes=('_cost', '_weight'))
                    # Додати новий стовпець для середньозваженої ціни
                    merged_df_outcome['avg_price, usd'] = merged_df_outcome['sum_total_usd'] / merged_df_outcome['quantity']


                    # Підготовка даних для графіка по витратам на товари
                    df_income_grouped = df_income.groupby(['date', 'product_name'])['sum_total_usd'].sum().reset_index()
                    df_outcome_grouped = df_outcome.groupby(['date', 'product_name'])['sum_total_usd'].sum().reset_index()

                    # Підготовка даних для графіка по компаніям
                    df_income_grouped_company = df_income.groupby(['date', 'company_name'])['sum_total_usd'].sum().reset_index()
                    df_outcome_grouped_company = df_outcome.groupby(['date', 'company_name'])['sum_total_usd'].sum().reset_index()

                    # Підготовка даних для графіка по вазі товарів
                    df_income_grouped_quantity = df_income.groupby(['date', 'product_name'])['quantity'].sum().reset_index()
                    df_outcome_grouped_quantity = df_outcome.groupby(['date', 'product_name'])['quantity'].sum().reset_index()


                    st.title(deals_messages[language]["buy"])
                    # Побудова графіка в Plotly для df_income_grouped
                    fig_income = get_plots(language, df_income_grouped, df_income_grouped_company, df_income_grouped_quantity)
                    # Відображення графіка в Streamlit
                    st.plotly_chart(fig_income)

                    st.write(deals_messages[language]["price"])
                    st.write(merged_df_income)

                    st.write(deals_messages[language]["full"])
                    st.dataframe(df_income)

                    st.title(deals_messages[language]["sell"])
                   # Побудова графіків в Plotly для df_income_grouped
                    fig_outcome = get_plots(language, df_outcome_grouped, df_outcome_grouped_company, df_outcome_grouped_quantity)
                    # Відображення графіка в Streamlit
                    st.plotly_chart(fig_outcome)

                    st.write(deals_messages[language]["price"])
                    st.write(merged_df_outcome)

                    st.write(deals_messages[language]["full"])
                    st.dataframe(df_outcome)
                else:
                    st.write(deals_messages[language]["empty"])
            except TypeError:
                st.write("ReLogin")

    # save_tokens(access_token, refresh_token)


if __name__ == '__main__':
    run_deals_app()


