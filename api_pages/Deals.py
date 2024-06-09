from datetime import date, timedelta, datetime
import time
import asyncio

import pandas as pd
import calendar
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.subplots as sp
import extra_streamlit_components as stx

import streamlit as st
import hydralit_components as hc

from api_pages.src.company_pages import (get_company_by_id, create_company_api, update_company_api,
                                         delete_company_api, search_companies_by_name, upload_company_csv)
from api_pages.src.goods_pages import get_goods_by_id
from api_pages.src.deals_pages import (get_deal_by_id, get_deals_by_product, get_deals_by_company, get_deals_by_period,
                                       create_purchase, update_purchase, delete_purchase, get_purchase_by_id,
                                       upload_csv, delete_purchases)

from api_pages.src.auth_services import load_token, save_tokens, FILE_NAME
from api_pages.src.user_footer import footer
from api_pages.src.messages import deals_messages

from api_pages.src.get_stocks_data import get_product_data


async def get_plots(language, df_income_grouped, df_income_grouped_company, df_income_grouped_quantity):
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

async def create_company(access_token):
    with st.expander("Create New Company", expanded=False):
        company_name = st.text_input("Company Name", key="name")
        additional_info = st.text_input("Prefered role", key="pref_role")
        favorite_role = st.text_input("Expenses Category", key="category")

        new_company_data = {
            "company_name": company_name,
            "additional_info": additional_info,
            "favorite_role": favorite_role,
            }
        if st.button("Create Company", key="confirm edit"):
            creation_response = await create_company_api(access_token, new_company_data)
            st.write(creation_response)

async def update_company(access_token):
    with st.expander("Update exist Company", expanded=False):
        update_company_id = st.number_input("Enter Company ID to Update", min_value=1, key="update_id")
        new_company_name = st.text_input("Company Name", key="updated_name")
        new_additional_info = st.text_input("Prefered role", key="updated_role")
        new_favorite_role = st.text_input("Expenses Category", key="updated_category")

        updated_company_data  = {
            "company_name": new_company_name,
            "additional_info": new_additional_info,
            "favorite_role": new_favorite_role,
            }
        if st.button("Update Company", key="confirm update"):
            update_response = await update_company_api(access_token, update_company_id, updated_company_data )
            st.write(update_response)

async def delete_company(access_token):
    with st.expander("Delete exist Company", expanded=False):
        delete_company_id = st.number_input("Enter Company ID to delete", min_value=1, key="delete_id")

        if st.button("Are you sure to delete Company?", key="confirm delete"):
            delete_response  = await delete_company_api(access_token, delete_company_id)
            st.write(delete_response)

async def get_company(access_token):
    company_id = st.text_input("Enter id", key="id input")
    if st.button("READ EXIST"):
        with hc.HyLoader('Now doing loading, wait please', hc.Loaders.pulse_bars):
            time.sleep(1)
        result = get_company_by_id(access_token, company_id)
        if result.get("401"):
            st.write("ReLogin")
        else:
            st.write(result)

    company_name = st.text_input("Search by company name")
    if st.button("SEARCH EXIST"):
        with hc.HyLoader('Now doing loading, wait please', hc.Loaders.pulse_bars):
            time.sleep(1)
        result = await search_companies_by_name(access_token, company_name)
        if isinstance(result, list):
            for company in result:
                st.write(company)
        else:
            st.write("Error: ", result)

async def upload_company_csv_ui(acc_token):
    with st.expander("Upload company from CSV File", expanded=False):
        uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
        if uploaded_file is not None:
            if st.button("Upload"):
                progress_bar = st.progress(0)
                status_text = st.empty()
                for percent_complete in range(100):
                    time.sleep(0)  # Штучна затримка для симуляції завантаження
                    progress_bar.progress(percent_complete + 1)
                    status_text.text(f"Uploading... {percent_complete + 1}%")
                # Код для завантаження CSV файлу і отримання відповіді від сервера
                response = await upload_company_csv(uploaded_file, acc_token)
                status_text.text("Upload complete!")
                st.write(response.json())



async def company_crud(access_token):
    await get_company(access_token)
    await create_company(access_token)
    await update_company(access_token)
    await delete_company(access_token)
    await upload_company_csv_ui(access_token)

async def do_deals_report(language, access_token):
    with st.sidebar:
        # Вибір місяця та року користувачем
        selected_month = st.selectbox(deals_messages[language]["Choose month"], list(calendar.month_name)[1:])
        selected_year = st.selectbox(deals_messages[language]["Choose year"], range(2020, 2025))

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
            result = await get_deals_by_period(access_token, start_date, end_date)
            if len(result["items"]) > 1:
                # Побудова таблиці
                df = pd.DataFrame(result["items"])

                # Вибір лише деяких стовбців та зміна порядку
                selected_columns = ["date", "product_id", "company_id", "quantity", "sum_total_tl", "sum_total_usd",
                                    "operation_type", "cost_per_mt_tl", "cost_per_mt_usd", "id"]
                df_selected = df[selected_columns]

                # Зміна порядку стовбців
                df_selected = df_selected[
                    ["date", "operation_type", "company_id", "product_id", "quantity", "sum_total_tl", "sum_total_usd",
                     "cost_per_mt_tl", "cost_per_mt_usd", "id"]]

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
                selected_columns_2 = ["date", "product_name", "company_name", "quantity", "sum_total_tl",
                                      "sum_total_usd",
                                      "cost_per_mt_usd", "id"]
                df_income = df_income[selected_columns_2]
                df_outcome = df_outcome[selected_columns_2]

                # Зміна порядку стовбців
                df_income = df_income[
                    ["date", "company_name", "product_name", "quantity", "sum_total_tl", "sum_total_usd",
                     "cost_per_mt_usd", "id"]]
                df_outcome = df_outcome[
                    ["date", "company_name", "product_name", "quantity", "sum_total_tl", "sum_total_usd",
                     "cost_per_mt_usd", "id"]]

                # Додати новий стовбець для середньозваженої ціни

                # Обчисліть загальну вартість та загальну вагу для кожного товару
                total_cost_in = df_income.groupby('product_name')['sum_total_usd'].sum().reset_index()
                total_weights_in = df_income.groupby('product_name')['quantity'].sum().reset_index()
                # Злиття двох датафреймів по назві товару
                merged_df_income = pd.merge(total_cost_in, total_weights_in, on='product_name',
                                            suffixes=('_cost', '_weight'))
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
                df_income_grouped_company = df_income.groupby(['date', 'company_name'])[
                    'sum_total_usd'].sum().reset_index()
                df_outcome_grouped_company = df_outcome.groupby(['date', 'company_name'])[
                    'sum_total_usd'].sum().reset_index()

                # Підготовка даних для графіка по вазі товарів
                df_income_grouped_quantity = df_income.groupby(['date', 'product_name'])['quantity'].sum().reset_index()
                df_outcome_grouped_quantity = df_outcome.groupby(['date', 'product_name'])[
                    'quantity'].sum().reset_index()

                st.title(deals_messages[language]["buy"])
                # Побудова графіка в Plotly для df_income_grouped
                fig_income = await get_plots(language, df_income_grouped, df_income_grouped_company,
                                             df_income_grouped_quantity)
                # Відображення графіка в Streamlit
                st.plotly_chart(fig_income)

                st.write(deals_messages[language]["price"])
                st.write(merged_df_income)

                st.write(deals_messages[language]["full"])
                st.dataframe(df_income)

                st.title(deals_messages[language]["sell"])
                # Побудова графіків в Plotly для df_income_grouped
                fig_outcome = await get_plots(language, df_outcome_grouped, df_outcome_grouped_company,
                                              df_outcome_grouped_quantity)
                # Відображення графіка в Streamlit
                st.plotly_chart(fig_outcome)

                st.write(deals_messages[language]["price"])
                st.write(merged_df_outcome)

                st.write(deals_messages[language]["full"])
                st.dataframe(df_outcome)
            else:
                st.write(deals_messages[language]["empty"])
        except TypeError as error:
            st.write("Please LogIn to continue", error)

async def create_purchase_ui(acc_token):
    with st.expander("Create Purchase", expanded=False):

        purchase_data = {
            "date": st.date_input("Date", key="new_date"),
            "operation_type": st.selectbox("Operation Type", ["income", "outcome"], key="new_operation_type"),
            "quantity": st.number_input("Quantity", min_value=0.0, key="new_quantity"),
            "company_id": st.number_input("Company ID", min_value=1, step=1, key="new_company_id"),
            "product_id": st.number_input("Product ID", min_value=1, step=1, key="new_product_id"),
            "price_tl": st.number_input("Price TL", min_value=0.0, key="new_v"),
            "transfer_cost": st.number_input("Transfer Cost", min_value=0.0, value=0.0, key="new_transfer_cost"),
            "commission_duties": st.number_input("Commission Duties", min_value=0.0, value=0.0, key="commission_duties"),
            "sum_total_tl": st.number_input("Sum Total TL", min_value=0.0, key="new_sum_total_tl"),
            "appr_ex_rate": st.number_input("Approx. Exchange Rate", min_value=0.0, key="new_appr_ex_rate"),
            "sum_total_usd": st.number_input("Sum Total USD", min_value=0.0, key="new_sum_total_usd"),
            "account_type": st.text_input("Account Type", key="new_account_type"),
            "cost_per_mt_tl": st.number_input("Cost per MT TL", min_value=0.0, key="new_cost_per_mt_tl"),
            "cost_per_mt_usd": st.number_input("Cost per MT USD", min_value=0.0, key="new_cost_per_mt_usd"),
            "user_id": st.number_input("User ID", min_value=1, step=1, key="new_user_id")
        }

        if st.button("Create Purchase"):
            purchase_data["date"] = purchase_data["date"].isoformat()
            result = await create_purchase(purchase_data, acc_token)
            st.write(result)

async def update_purchase_ui(acc_token):
    with st.expander("Update Purchase", expanded=False):
        purchase_id = st.number_input("Purchase ID", min_value=1, step=1)

        if st.button("Fetch Purchase Data"):
            purchase_data = await get_purchase_by_id(purchase_id, acc_token)
            if isinstance(purchase_data, dict):
                st.session_state["purchase_data"] = purchase_data
            else:
                st.write(purchase_data)

        if "purchase_data" in st.session_state:
            purchase_data = st.session_state["purchase_data"]

            purchase_data["date"] = st.date_input("Date", value=datetime.strptime(purchase_data["date"],
             '%Y-%m-%d').date() if isinstance(purchase_data["date"], str) else purchase_data["date"])
            purchase_data["operation_type"] = st.selectbox("Operation Type", ["income", "outcome"],
                                                           index=["income", "outcome"].index(
                                                               purchase_data["operation_type"]))
            purchase_data["quantity"] = st.number_input("Quantity", value=purchase_data["quantity"])
            purchase_data["company_id"] = st.number_input("Company ID", value=purchase_data["company_id"])
            purchase_data["product_id"] = st.number_input("Product ID", value=purchase_data["product_id"])
            purchase_data["price_tl"] = st.number_input("Price TL", value=purchase_data["price_tl"])
            purchase_data["transfer_cost"] = st.number_input("Transfer Cost",
                                                             value=purchase_data["transfer_cost"] or 0.0)
            purchase_data["commission_duties"] = st.number_input("Commission Duties",
                                                                 value=purchase_data["commission_duties"] or 0.0)
            purchase_data["sum_total_tl"] = st.number_input("Sum Total TL", value=purchase_data["sum_total_tl"])
            purchase_data["appr_ex_rate"] = st.number_input("Approx. Exchange Rate",
                                                            value=purchase_data["appr_ex_rate"])
            purchase_data["sum_total_usd"] = st.number_input("Sum Total USD", value=purchase_data["sum_total_usd"])
            purchase_data["account_type"] = st.text_input("Account Type", value=purchase_data["account_type"])
            purchase_data["cost_per_mt_tl"] = st.number_input("Cost per MT TL", value=purchase_data["cost_per_mt_tl"])
            purchase_data["cost_per_mt_usd"] = st.number_input("Cost per MT USD",
                                                               value=purchase_data["cost_per_mt_usd"])
            # purchase_data["user_id"] = int(st.session_state["user"]["id"])

            if st.button("Update Purchase"):
                # Перетворення дати у строку
                if isinstance(purchase_data["date"], date):
                    purchase_data["date"] = purchase_data["date"].isoformat()
                result = await update_purchase(purchase_id, purchase_data, acc_token)
                st.write(result)

async def delete_purchase_ui(acc_token):
    with st.expander("Delete Purchase", expanded=False):
        purchase_id = st.number_input("Purchase ID to delete", min_value=1, step=1)
        if st.button("Delete Purchase"):
            result = await delete_purchase(purchase_id, acc_token)
            st.write(result)

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
                # Код для завантаження CSV файлу і отримання відповіді від сервера
                response = await upload_csv(uploaded_file, acc_token)
                status_text.text("Upload complete!")
                st.write(response.json())

async def delete_purchases_ui(acc_token):
    with st.expander("Delete Purchases for period", expanded=False):
        start_date = st.date_input("Start Date", value=date.today())
        end_date = st.date_input("End Date", value=date.today())
        if st.button("Delete Purchases"):
            if start_date > end_date:
                st.error("Start date cannot be after end date")
            else:
                params = {
                    'start_date': start_date.isoformat(),
                    'end_date': end_date.isoformat()
                }
                result = await delete_purchases(params, acc_token)
                if isinstance(result, dict):
                    st.success(result.get("detail"))
                    st.write(f"Deleted purchases: {result.get('deleted_count')}")
                else:
                    st.error(result)

async def purchase_crud(access_token):
    await create_purchase_ui(access_token)
    await update_purchase_ui(access_token)
    await delete_purchase_ui(access_token)
    await upload_csv_ui(access_token)
    await delete_purchases_ui(access_token)

async def run_deals_app():
    footer()
    access_token = None
    access_token = st.session_state.get("access_token", "")
    language = st.session_state.get("selected_language", "english_name")

    st.sidebar.title(deals_messages[language]["title"])
    page = st.sidebar.selectbox(deals_messages[language]["Choose action"],
                                [deals_messages[language]["Monthly report"],
                                 deals_messages[language]["Company list"],]
                                )

    if page == deals_messages[language]["Company list"]:
        await company_crud(access_token)

    elif page == deals_messages[language]["Monthly report"]:
        await do_deals_report(language, access_token)

        user_level = st.session_state["role"]
        if user_level == "admin":
            st.write("!!!You can edit the data!!!")
            await purchase_crud(access_token)


if __name__ == '__main__':
    asyncio.run(run_deals_app())


