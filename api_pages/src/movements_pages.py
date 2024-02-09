import pandas as pd
import requests
from collections import defaultdict
import plotly.express as px
import streamlit as st

from api_pages.src.auth_services import SERVER_URL
from api_pages.src.company_pages import get_company_by_id
from api_pages.src.messages import movements_messages


async def get_accounts(acc_token):
    url = SERVER_URL + "/api/accounts/"
    headers = {"Authorization": f"Bearer {acc_token}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        banks_list = data["items"]
        return banks_list


async def get_movements_by_multifilter(language, acc_token):
    url = SERVER_URL + "/api/movements/milti_filter/{filter_params}"  # Замените на фактические значения
    headers = {"Authorization": f"Bearer {acc_token}"}

    # Опциональные параметры запроса, если есть
    params = {
        "offset": 0,
        "limit": 2000#,
        #"currency": "usd"
        # ,
        # "payment_way": 16
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        full_list = data["items"]
        df = pd.DataFrame(full_list)

        # # Перетворюємо колонку 'date' в тип datetime
        # df['date'] = pd.to_datetime(df['date'])

        # Знаходимо максимальну дату
        max_date = df['date'].max()

        # Виводимо результат
        st.write(movements_messages[language]["Last date of movements"], max_date)

        # Групуємо за payment_way, operation_type та currency та підраховуємо суму
        result_df = df.groupby(['payment_way', 'operation_type', 'currency'])['sum'].sum().reset_index()

        # Розділяємо на окремі DataFrames за operation_type
        debit_df = result_df[result_df['operation_type'] == 'debit'].copy()
        credit_df = result_df[result_df['operation_type'] == 'credit'].copy()

        # Об'єднуємо дві таблиці по колонках payment_way, currency
        merged_df = pd.merge(debit_df, credit_df, on=['payment_way', 'currency'], suffixes=('_debit', '_credit'),
                             how='outer')

        # Заповнюємо NaN значення нулями
        merged_df = merged_df.fillna(0)

        # Додаємо нову колонку balance
        merged_df['balance'] = merged_df['sum_credit'] - merged_df['sum_debit']

        # Видаляємо зайві колонки
        merged_df = merged_df.drop(['operation_type_credit', 'operation_type_debit'], axis=1)

        banks = await get_accounts(acc_token)
        banks = pd.DataFrame(banks)
        banks = banks.drop(['user_id', 'created_at', 'updated_at'], axis=1)

        # Об'єднуємо DataFrames за умовою payment_way == id
        result_df = pd.merge(merged_df, banks, left_on='payment_way', right_on='id')

        # Задаємо новий порядок колонок
        new_order = ['id', 'name', 'currency', 'sum_debit', 'sum_credit', 'balance']

        # Застосовуємо новий порядок колонок
        result_df = result_df[new_order]

        return result_df

    else:
        return f"Error: {response.status_code}, {response.text}"


async def get_chart(language, frame):
    frame = frame[frame['name'] != 'Vakif vinov']
    frame = frame[frame['name'] != 'QNB deposit']

    # Сортуємо датафрейм за полем 'balance' у зростаючому порядку
    frame = frame.sort_values(by='balance')

    fig = px.bar(frame, x='name', y='balance', color='currency', barmode='stack',
                 labels={'balance': 'Balance'},
                 title=movements_messages[language]['Rest by Banks'])

    # Відображаємо діаграму
    st.plotly_chart(fig)

    # Створюємо стовпчату діаграму з накопиченням за валютами
    fig2 = px.bar(frame, x='currency', y='balance',
                 color='name',
                 # barmode='stack',  # Накопичення стовбців
                 labels={'balance': 'Balance'},
                 title=movements_messages[language]['Rest by Currency'])

    st.plotly_chart(fig2)


async def get_total(language, frame):
    frame = frame[frame['name'] != 'Vakif vinov']
    frame = frame[frame['name'] != 'QNB deposit']

    # Сортуємо датафрейм за полем 'balance' у зростаючому порядку
    frame = frame.sort_values(by='balance')

    total_df = frame.groupby(['currency'])['balance'].sum().reset_index()
    st.write(movements_messages[language]["Total by currency"])
    return total_df
