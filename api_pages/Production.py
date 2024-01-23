import asyncio
import streamlit as st
import hydralit_components as hc
import calendar

import time
from datetime import date, timedelta
import pandas as pd

from api_pages.src.company_pages import get_company_by_id
from api_pages.src.goods_pages import get_goods_by_id
from api_pages.src.deals_pages import get_deal_by_id, get_deals_by_product, get_deals_by_company, get_deals_by_period
from api_pages.src.user_footer import footer
from api_pages.src.get_stocks_data import get_product_data
from api_pages.src.messages import stock_messages, deals_messages
from api_pages.src.general_services import get_query_params, get_db_data


# st.set_page_config(page_title="Production",
#                    page_icon=":factory:")


async def run_production_app():
    try:
        footer()
        access_token = None
        access_token = st.session_state.get("access_token", "")
        language = st.session_state.get("selected_language", "english_name")

        with st.sidebar:
            selected_products = st.multiselect(stock_messages[language]["goods"], get_product_data(language, access_token),
                                               key="Products")
            # Вибір місяця та року користувачем
            selected_month = st.selectbox(deals_messages[language]["Choose month"], list(calendar.month_name)[1:])
            selected_year = st.selectbox(deals_messages[language]["Choose year"], range(2020, 2025))

            # Отримання числа місяця за його іменем
            month_number = list(calendar.month_name).index(selected_month)

            # Формування початкової та кінцевої дати
            start_date = pd.to_datetime(f"{selected_year}-{month_number:02d}-01")
            end_date = pd.to_datetime(
                f"{selected_year}-{month_number:02d}-{calendar.monthrange(selected_year, month_number)[1]}")
            # Додати один день до кінцевої дати
            start_date_for_stocks = start_date - timedelta(days=1)
            end_date_for_stocks = end_date + timedelta(days=1)

        parameters = get_query_params(language, selected_products, start_date_for_stocks.strftime('%Y-%m-%d'), end_date_for_stocks.strftime('%Y-%m-%d'))

        if st.sidebar.button("GO"):
            stock_data_from_db = get_db_data(access_token, parameters)
            # a dedicated single loader
            with hc.HyLoader('Now doing loading, wait please', hc.Loaders.pulse_bars):
                time.sleep(1)
            if stock_data_from_db:
                # st.write("stock_data_from_db data", stock_data_from_db)
                for entry in stock_data_from_db:
                    # print(entry)
                    entry['product'] = entry['product']['name']
                    # entry['product'] = entry['product']['id']


                stocks_data = pd.DataFrame(stock_data_from_db)
                # Перетворення колонок з датами в тип datetime
                stocks_data['date'] = pd.to_datetime(stocks_data['date'])
                # Сортування за датою
                stocks_data = stocks_data.sort_values(by='date')

                # st.write("Stocks data")
                # st.write(stocks_data)

            deals_data_from_db = get_deals_by_period(access_token, start_date, end_date)
            if len(deals_data_from_db["items"]) > 1:
                deals_data = pd.DataFrame(deals_data_from_db["items"])

                # Перетворення колонок з датами в тип datetime
                deals_data['date'] = pd.to_datetime(deals_data['date'])
                # Сортування за датою
                deals_data = deals_data.sort_values(by='date')
                # Отримання назв товарів
                products_data = get_product_data(language, access_token) #"english_name"
                products_dict = {product["id"]: product["name"] for product in products_data}
                deals_data["product"] = deals_data["product_id"].map(products_dict)

                # Відфільтрувати df2 за значенням стовпця "product" з df1
                # deals_data = deals_data.loc[deals_data['product'].isin(stocks_data['product'])]
                # deals_data = deals_data.loc[deals_data['product_id'].isin(stocks_data['product'])]


                # Побудова таблиці
                selected_columns = ["date", "operation_type", "product", "quantity", "product_id"]
                # selected_columns = ["date", "operation_type", "product_id", "quantity"]
                deals_data = deals_data[selected_columns]

                # Пошук товарів що не мають залишків на складі
                # Список ідентифікаторів товарів, по яким потрібно відфільтрувати щоб виключити торгівельні операції
                selected_product_ids = [18, 12]  # додайте всі необхідні ідентифікатори

                non_stock_deals_row1 = deals_data[
                    (deals_data['product_id'].isin(selected_product_ids))]

                # Підрахунок суми за стовпцем "quantity" для знайдених рядків
                total_quantity_for_minus = non_stock_deals_row1['quantity'].sum()
                # st.write(non_stock_deals_row1)
                # st.write(total_quantity_for_minus)


                # Список ідентифікаторів товарів, по яким потрібно відфільтрувати щоб додати до виробництва
                selected_product_ids2 = [21]  # додайте всі необхідні ідентифікатори
                non_stock_deals_row2 = deals_data[
                    (deals_data['product_id'].isin(selected_product_ids2))]

                # Підрахунок суми за стовпцем "quantity" для знайдених рядків
                total_quantity_for_plus = non_stock_deals_row2['quantity'].sum()
                # st.write(non_stock_deals_row2)
                # st.write(total_quantity_for_plus)

                # st.write("Deals data")
                # st.write(deals_data)

            # Створення нового стовпця для виробництва
            stocks_data['production'] = 0.0

            # Цикл для обчислення виробництва за кожну транзакцію
            for index, deal in stocks_data.iterrows():
                date = deal['date']
                product_id = deal['product']
                # operation_type = deal['operation_type']

                # Знаходження відповідного рядка у stocks_data за датою та товаром
                stocks_row = stocks_data[(stocks_data['date'] == date) & (stocks_data['product'] == product_id)]
                # st.write("current", stocks_row)
                # Знаходження попереднього дня
                prev_date = date - pd.DateOffset(1)
                # Знаходження відповідного рядка у stocks_data за попередній день та товаром
                prev_stocks_row = stocks_data[(stocks_data['date'] == prev_date) & (stocks_data['product'] == product_id)]
                # prev_deals_row = deals_data[(deals_data['date'] == prev_date) & (deals_data['product_id'] == product_id)]
                prev_deals_rows = deals_data[(deals_data['date'] == prev_date) & (deals_data['product'] == product_id)]

                # st.write("prev_stocks", prev_stocks_row)
                today_stock = stocks_row.iloc[0]["quantity"]
                # st.write("today stock", today_stock)
                if not prev_stocks_row.empty:
                    before_stock = prev_stocks_row.iloc[0]["quantity"]
                    # st.write("before stock", before_stock)
                    stocks_data.loc[(stocks_data['date'] >= date) & (
                                stocks_data['product'] == product_id), 'production'] = today_stock - before_stock

                if not prev_deals_rows.empty:
                    for _, prev_deals_row in prev_deals_rows.iterrows():
                        operation_type = prev_deals_row['operation_type']
                        quantity = prev_deals_row['quantity']
                        # print(quantity)

                        # Оновлення виробництва за алгоритмом
                        if operation_type == 'income':
                            stocks_data.loc[(stocks_data['date'] >= date) & (
                                    stocks_data['product'] == product_id), 'production'] -= quantity
                        elif operation_type == 'outcome':
                            stocks_data.loc[(stocks_data['date'] >= date) & (
                                    stocks_data['product'] == product_id), 'production'] += quantity


            # Друк оновленого DataFrame з виробництвом
            st.write("Approximate production")

            # Групуємо за товаром та обчислюємо суму production
            total_production = stocks_data.groupby('product')['production'].sum().reset_index()

            # # Додаємо суму total_quantity_for_minus до виробництва продуктів з ідентифікаторами 18 та 12
            total_production.loc[total_production['product'].isin(["Crude sunoil", "Сира соняшникова олія",
            "Сырое подсолнечное масло", "ham ayçi̇cek yağ"]), 'production'] -= total_quantity_for_minus

            # Додаємо суму total_quantity_for_plus до виробництва продуктів з ідентифікатором 21
            total_production.loc[total_production['product'].isin(["Crude sunoil", "Сира соняшникова олія",
            "Сырое подсолнечное масло", "ham ayçi̇cek yağ"]), 'production'] += total_quantity_for_plus


            # Додаємо рядок "total" в групований датафрейм та обчислюємо суму для 'production'
            total_value = total_production['production'].sum()
            total_row = pd.DataFrame({'product': ['total'], 'production': [total_value]})
            total_production = pd.concat([total_production, total_row], ignore_index=True)

            st.write(total_production)
            # st.write(stocks_data)


    except TypeError as e:
        st.write(f"ReLogin / {e}")

# st.write(st.session_state)

if __name__ == '__main__':
    asyncio.run(run_production_app())
