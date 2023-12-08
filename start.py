import streamlit as st
import hydralit_components as hc

from htmlTemplates import css
from pages.src.user_footer import footer
from pages.src.messages import hello_messages

st.set_page_config(page_title="Company observer",
                   page_icon="chart_with_upwards_trend")

st.write(css, unsafe_allow_html=True)


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


def main():
    st.sidebar.image("static/pro-logo.png", width=200)
    language = menu_id
    st.title(hello_messages[language]["title"])
    st.text(hello_messages[language]["instruction"])
    footer()


if __name__ == '__main__':
    main()
