import pandas as pd
import requests
from collections import defaultdict
import plotly.express as px
import streamlit as st
import plotly.graph_objects as go

from api_pages.src.auth_services import SERVER_URL
from api_pages.src.company_pages import get_company_by_id
from api_pages.src.messages import movements_messages


async def get_companies(acc_token):
    url = SERVER_URL + "/api/company/"
    headers = {"Authorization": f"Bearer {acc_token}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        companies_list = data["items"]

        # Припустимо, що df - ваш датафрейм, а companies - ваш список словників
        companies_mapping = {company['id']: company['company_name'] for company in companies_list}
        return companies_mapping


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
        "limit": 5000
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
    # frame = frame[frame['name'] != 'Vakif vinov']
    # frame = frame[frame['name'] != 'QNB deposit']

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
    # frame = frame[frame['name'] != 'Vakif vinov']
    # frame = frame[frame['name'] != 'QNB deposit']

    # Сортуємо датафрейм за полем 'balance' у зростаючому порядку
    frame = frame.sort_values(by='balance')

    total_df = frame.groupby(['currency'])['balance'].sum().reset_index()
    st.write(movements_messages[language]["Total by currency"])
    return total_df


async def get_movements_by_bank(language, acc_token, params):
    url = SERVER_URL + "/api/movements/milti_filter/{filter_params}"  # Замените на фактические значения
    headers = {"Authorization": f"Bearer {acc_token}"}

    # Опциональные параметры запроса, если есть
    # params = params

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        full_list = data["items"]
        df = pd.DataFrame(full_list)

        # Указать ненужные столбцы
        columns_to_drop = ['id', 'user_id', 'created_at', 'updated_at', 'payment_way']
        new_df = df.drop(columns=columns_to_drop)
        return new_df


async def get_sankey_chart(language, df, acc_token, threshold, show_self):
    companies_mapping = await get_companies(acc_token)
    # Заміна значень в колонці company_id на відповідні значення з company_name
    df['company_id'] = df['company_id'].map(companies_mapping)

    if df.empty:
        st.write("No data available to display the chart.")
        return

    st.write(movements_messages[language]["Details"])
    st.write(df)

    df["sender"] = df.apply(lambda row: "pro oil yag" if row["operation_type"] == "debit" else row["company_id"],
                            axis=1)
    df["reciever"] = df.apply(lambda row: row["company_id"] if row["operation_type"] == "debit" else "pro oil yag",
                              axis=1)

    # Групування ланок за відправником та отримувачем
    grouped_df = df.groupby(['sender', 'reciever', 'currency']).agg({'sum': 'sum'}).reset_index()

    # Видалення рядків, де обидві колонки "відправник" та "отримувач" одночасно мають значення "My_company"
    if not show_self:
        grouped_df = grouped_df[~((grouped_df["sender"] == "pro oil yag") & (grouped_df["reciever"] == "pro oil yag"))]

    # Визначення порогів для кожної валюти
    thresholds = {'usd': 100, 'eur': 100, 'tl': threshold}  # Задайте пороги за потребою

    for currency, threshold in thresholds.items():
        filtered_df = grouped_df[grouped_df["currency"] == currency]

        if filtered_df.empty:
            st.write(f"No data available for {currency} currency.")
            continue

        # Видалення записів, які не відповідають порогу
        filtered_df = filtered_df[filtered_df['sum'] >= threshold]

        if filtered_df.empty:
            st.write(f"No data above threshold for {currency} currency.")
            continue

        # Створення вузлів та зв'язків
        nodes = pd.concat([filtered_df["sender"], filtered_df["reciever"]]).unique()
        nodes_dict = {node: idx for idx, node in enumerate(nodes)}

        links = []
        for i, row in filtered_df.iterrows():
            source_idx = nodes_dict[row["sender"]]
            target_idx = nodes_dict[row["reciever"]]
            links.append({"source": source_idx, "target": target_idx, "value": row["sum"]})

        # Створення Sankey діаграми
        fig = go.Figure(data=[go.Sankey(
            node=dict(
                pad=15,
                thickness=20,
                line=dict(
                    color="black",
                    width=0.5
                ),
                label=[str(node) for node in nodes]
            ),
            link=dict(
                source=[link["source"] for link in links],
                target=[link["target"] for link in links],
                value=[link["value"] for link in links],
            )
        )])

        # Налаштування діаграми
        fig.update_layout(
            title=f"{movements_messages[language]['Chart title']} ({currency})",
            font=dict(
                family="Arial",
                size=12
            ),
            width=800,
            height=600
        )
        st.plotly_chart(fig)

async def upload_csv(file, acc_token):
    api_url = f'{SERVER_URL}/api/movements/upload-csv/'
    headers = {"Authorization": f"Bearer {acc_token}"}
    files = {'file': file}
    response = requests.post(api_url, headers=headers, files=files)
    return response

async def get_movements_by_period(start_date, end_date, acc_token):
    url = SERVER_URL + "/api/movements/by_period"
    headers = {"Authorization": f"Bearer {acc_token}"}

    # Перетворення дат в рядковий формат YYYY-MM-DD
    start_date_str = start_date.strftime("%Y-%m-%d")
    end_date_str = end_date.strftime("%Y-%m-%d")

    params = {'start_date': start_date_str, 'end_date': end_date_str}
    response = requests.post(url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        full_list = data["items"]
        df = pd.DataFrame(full_list)
        return df
    else:
        return {response.status_code: response.text}


async def get_movement_by_id(movement_id, acc_token):
    url = f"{SERVER_URL}/api/movements/{movement_id}"
    headers = {"Authorization": f"Bearer {acc_token}"}

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Error fetching movement: {response.status_code}")
        return None


async def update_movement(movement_id, movement_data, acc_token):
    url = f"{SERVER_URL}/api/movements/{movement_id}"
    headers = {"Authorization": f"Bearer {acc_token}", "Content-Type": "application/json"}

    response = requests.put(url, headers=headers, json=movement_data)
    if response.status_code == 201:
        st.success("Movement updated successfully!")
        return response.json()
    else:
        st.error(f"Error updating movement: {response.status_code}")
        return None


async def create_movement(movement_data, acc_token):
    url = f"{SERVER_URL}/api/movements/"
    headers = {"Authorization": f"Bearer {acc_token}", "Content-Type": "application/json"}

    response = requests.post(url, headers=headers, json=movement_data)
    if response.status_code == 201:
        st.success("Movement created successfully!")
        return response.json()
    else:
        st.error(f"Error creating movement: {response.status_code}")
        return None


async def delete_movement(movement_id, acc_token):
    url = f"{SERVER_URL}/api/movements/{movement_id}"
    headers = {"Authorization": f"Bearer {acc_token}"}

    response = requests.delete(url, headers=headers)
    if response.status_code == 200:
        st.success("Movement deleted successfully!")
        return response.json()
    else:
        st.error(f"Error deleting movement: {response.status_code}")
        return None
