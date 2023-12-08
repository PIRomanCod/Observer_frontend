from pages.src.get_stocks_data import post_stocks_data


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
