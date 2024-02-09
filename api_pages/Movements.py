from datetime import date, timedelta
import time
import extra_streamlit_components as stx

import pandas as pd
import calendar
import matplotlib.pyplot as plt
import seaborn as sns

import plotly.express as px
import plotly.subplots as sp
import plotly.graph_objects as go
import asyncio

import streamlit as st
import hydralit_components as hc

from api_pages.src.company_pages import get_company_by_id
from api_pages.src.movements_pages import get_movements_by_multifilter, get_accounts, get_chart, get_total
from api_pages.src.user_footer import footer
from api_pages.src.messages import movements_messages


async def run_movements_app():
    footer()
    access_token, refresh_token = None, None
    access_token = st.session_state.get("access_token", "")
    language = st.session_state.get("selected_language", "english_name")

    st.sidebar.title(movements_messages[language]["title"])
    page = st.sidebar.selectbox(movements_messages[language]["Choose action"],
                                [movements_messages[language]["Rests for now"],

                                 ]
                                )

    if page == movements_messages[language]["Rests for now"]:
        if st.button("GO"):
            with hc.HyLoader('Now doing loading, wait please', hc.Loaders.pulse_bars):
                time.sleep(1)

            result = await get_movements_by_multifilter(language, access_token)
            st.write(await get_total(language, result))
            await get_chart(language, result)
            st.write(movements_messages[language]["Details"])
            st.write(result)


if __name__ == '__main__':
    asyncio.run(run_movements_app())