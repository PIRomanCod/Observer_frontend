import streamlit as st
import hydralit_components as hc
import extra_streamlit_components as stx
import asyncio

from htmlTemplates import css
from api_pages.src.user_footer import footer
from api_pages.src.backgroung import back
from api_pages.src.messages import hello_messages
from api_pages.src.auth_pages import profile_page
from api_pages.Deals import run_deals_app
from api_pages.Authorization import main_auth
from api_pages.Balances import run_balances_app
from api_pages.Stocks_viewer import run_stocks_app
from api_pages.Production import run_production_app
from api_pages.Movements import run_movements_app


st.write(css, unsafe_allow_html=True)

menu_data = [
    {'id': 'home', 'label': "Home"},
    {'id': 'auth', 'label': "LogIn"},
    {'id': 'stocks', 'label': "Stocks"},
    {'id': 'production', 'label': "Production"},
    {'id': 'deals', 'label': "Deals"},
    {'id': 'balances', 'label': "Balances"},
    {'id': 'movements', 'label': "Movements"},

]

menu_id = hc.nav_bar(
    menu_definition=menu_data,
    first_select=0,
    key="stock_nav",
    home_name=None,
    login_name={'id': "login_name", 'label': st.session_state.get("username", None), 'icon': "fa fa-user-circle", 'ttip': "username"},
    override_theme={'txc_inactive': 'white', 'menu_background': 'green', 'txc_active': 'yellow',
                    'option_active': 'blue'},
    sticky_nav=True,#False,
    force_value=None,
    use_animation=True,
    hide_streamlit_markers=True,
    sticky_mode=None,
    option_menu=True)

# Отримання значення з st.session_state або встановлення значення за замовчуванням
selected_language = st.session_state.get("selected_language", "english_name")

auth_manager = None


def main():
    st.sidebar.image("static/pro-logo.png", width=150)
    # back()
    # language = menu_id
    footer()
    st.session_state["role"] = None
    if menu_id == "home":
        with st.sidebar:
            # Відображення кнопки вибору (radio button) або випадаючого списку (selectbox) зі значеннями
            selected_language = st.radio("Select Language:",
                                         ["english_name", "ukrainian_name", "russian_name", "turkish_name"])

            # Оновлення значення в st.session_state
            st.session_state["selected_language"] = selected_language

            # Виведення обраного значення
            st.write("Selected Language:", selected_language)
            language = st.session_state.get("selected_language", "english_name")

        st.title(hello_messages[language]["title"])
        st.text(hello_messages[language]["instruction"])
    elif menu_id == 'auth':
        asyncio.run(main_auth())
    elif menu_id == 'stocks':
        asyncio.run(run_stocks_app())
    elif menu_id == 'production':
        asyncio.run(run_production_app())
    elif menu_id == 'deals':
        asyncio.run(run_deals_app())
    elif menu_id == 'balances':
        asyncio.run(run_balances_app())
    elif menu_id == 'movements':
        asyncio.run(run_movements_app())
    elif menu_id == 'login_name':
        profile_page(st.session_state.get("access_token", ""))


if __name__ == '__main__':
    main()
