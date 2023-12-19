from api_pages.src.get_stocks_data import post_stocks_data
import hydralit_components as hc
import extra_streamlit_components as stx

# cookie_manager = stx.CookieManager()
# cookies = cookie_manager.get_all()


def get_query_params(language, product_ids, start_date, end_date):
    id_list = [item['id'] for item in product_ids]
    start_date = start_date
    end_date = end_date
    language = language
    product_ids = id_list
    limit = 250
    offset = 0

    # Формування параметрів для використання у вашому коді
    params = {
        "start_date": str(start_date),
        "end_date": str(end_date),
        "language": language,
        "product_ids": product_ids,
        "limit": limit,
        "offset": offset
    }
    return params


def get_db_data(access_token, params):
    result = post_stocks_data(params, access_token)
    return result



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
