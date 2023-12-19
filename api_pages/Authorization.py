# import streamlit as st
#
# from pages.src.auth_pages import login_page, signup_page, start_page, profile_page
# from pages.src.auth_pages import  reset_password_page, request_mail_page, change_avatar_page
# from pages.src.auth_services import load_token, save_token, FILE_NAME
# from pages.src.user_footer import footer
#
#
# st.set_page_config(
#     page_title="Auth",
#     page_icon="lock",
# )
#
#
# def run_app():
#     footer()
#     access_token, refresh_token = load_token(FILE_NAME)
#     st.sidebar.title("Navigation")
#     page = st.sidebar.selectbox("Choose action",
#                                 ["SignUp",
#                                  "Login",
#                                  "My Profile",
#                                  "Resending email signup confirmation",
#                                  "Reset password via email",
#                                  "Change avatar",
#                                  "Logout"]
#                                 )
#
#     if page == "Login":
#         if access_token:
#             profile_page(access_token, refresh_token)
#             access_token, refresh_token = load_token(FILE_NAME)
#         else:
#             access_token, refresh_token = login_page()
#
#     elif page == "SignUp":
#         if access_token:
#             st.write("You are already in. Press Logout for SignUp")
#         else:
#             signup_page()
#
#     elif page == "My Profile":
#         if access_token:
#             profile_page(access_token, refresh_token)
#             access_token, refresh_token = load_token(FILE_NAME)
#         else:
#             start_page()
#
#     elif page == "Resending email signup confirmation":
#         if access_token:
#             st.text("You already confirm email")
#         else:
#             request_mail_page()
#
#     elif page == "Reset password via email":
#         reset_password_page()
#
#     elif page == "Change avatar":
#         if access_token:
#             change_avatar_page(access_token, refresh_token)
#         else:
#             start_page()
#
#     if access_token:
#         if st.button("Logout"):
#             access_token, refresh_token = None, None
#             save_token(access_token, refresh_token)
#             st.rerun()
#
#     save_token(access_token, refresh_token)
#
#
# if __name__ == '__main__':
#     run_app()
#
#
# import streamlit as st
# from pages.src.auth_pages import (
#     login_page, signup_page, start_page,
#     profile_page, reset_password_page,
#     request_mail_page, change_avatar_page
# )
# from pages.src.auth_services import load_token, save_token, FILE_NAME, get_refresh_token
# from pages.src.user_footer import footer
#
#
# class AuthManager:
#     def __init__(self):
#         self.access_token, self.refresh_token = load_token(FILE_NAME)
#
#     def login(self):
#         if self.access_token:
#             profile_page(self.access_token, self.refresh_token)
#             self.access_token, self.refresh_token = load_token(FILE_NAME)
#         else:
#             self.access_token, self.refresh_token = login_page()
#
#     def signup(self):
#         if self.access_token:
#             st.write("You are already in. Press Logout for SignUp")
#         else:
#             signup_page()
#
#     def profile(self):
#         if self.access_token:
#             profile_page(self.access_token, self.refresh_token)
#             self.access_token, self.refresh_token = load_token(FILE_NAME)
#         else:
#             start_page()
#
#     def resend_confirmation(self):
#         if self.access_token:
#             st.text("You already confirmed your email")
#         else:
#             request_mail_page()
#
#     def reset_password(self):
#         reset_password_page()
#
#     def change_avatar(self):
#         if self.access_token:
#             change_avatar_page(self.access_token, self.refresh_token)
#         else:
#             start_page()
#
#     def logout(self):
#         if self.access_token:
#             self.access_token, self.refresh_token = None, None
#             save_token(self.access_token, self.refresh_token)
#             if self.access_token:
#                 if st.button("Logout"):
#                     access_token, refresh_token = None, None
#                     save_token(access_token, refresh_token)
#                     st.rerun()
#             st.rerun()
#
#     def save_token(self):
#         save_token(self.access_token, self.refresh_token)
#
#     def run_app(self):
#         footer()
#         st.sidebar.title("Navigation")
#         page = st.sidebar.selectbox(
#             "Choose action",
#             ["SignUp", "Login", "My Profile", "Resending email signup confirmation",
#              "Reset password via email", "Change avatar", "Logout"]
#         )
#
#         if hasattr(self, page.lower()):
#             getattr(self, page.lower())()
#
#         self.save_token()
#
#     def refresh_token_with_api(self):
#         # Виклик /api/auth/refresh_token для оновлення токенів
#         get_refresh_token(self.refresh_token)
#
#
# if __name__ == '__main__':
#     auth_manager = AuthManager()
#     auth_manager.run_app()

#####################################################################################3
# import streamlit as st
# import time
# import asyncio
# from pages.src.auth_pages import (
#     login_page, signup_page, start_page,
#     profile_page, reset_password_page,
#     request_mail_page, change_avatar_page
# )
# from pages.src.auth_services import load_token, save_tokens, FILE_NAME, get_refresh_token
# from pages.src.user_footer import footer
#
#
# class AuthManager:
#     def __init__(self):
#         self.access_token, self.refresh_token = None, None #= load_token(FILE_NAME)
#         # self.refresh_checkbox = st.empty()
#
#     def login(self):
#         if self.access_token:
#             profile_page(self.access_token)
#             if not profile_page:
#                 self.refresh_token_in_background()
#             self.access_token, self.refresh_token = load_token(FILE_NAME)
#         else:
#             self.access_token, self.refresh_token = login_page()
#             # st.write(self.access_token, self.refresh_token)
#             self.save_token()
#
#     def signup(self):
#         if self.access_token:
#             st.write("You are already in. Press Logout for SignUp")
#         else:
#             signup_page()
#
#     def profile(self):
#         if self.access_token:
#             profile_page(self.access_token, self.refresh_token)
#             self.access_token, self.refresh_token = load_token(FILE_NAME)
#         else:
#             start_page()
#
#     def resend_confirmation(self):
#         if self.access_token:
#             st.text("You already confirmed your email")
#         else:
#             request_mail_page()
#
#     def reset_password(self):
#         reset_password_page()
#
#     def change_avatar(self):
#         if self.access_token:
#             change_avatar_page(self.access_token, self.refresh_token)
#         else:
#             start_page()
#
#     def logout(self):
#         if self.access_token:
#             self.access_token, self.refresh_token = None, None
#             save_tokens(self.access_token, self.refresh_token)
#             st.rerun()
#
#     def save_token(self):
#         save_tokens(self.access_token, self.refresh_token)
#
#     async def run_app(self):
#         footer()
#         st.sidebar.title("Navigation")
#         page = st.sidebar.selectbox(
#             "Choose action",
#             [
#                 "SignUp",
#                 "Login",
#                 # "My Profile",
#                 "Resending email signup confirmation",
#                 "Reset password via email",
#                 # "Change avatar",
#                 "Logout"
#              ]
#         )
#
#         if hasattr(self, page.lower()):
#             getattr(self, page.lower())()
#
#         # Оновлення токенів при виборі користувачем
#         # if self.refresh_checkbox.checkbox("Automatically refresh tokens"):
#         self.refresh_token_in_background()
#
#         self.save_token()
#
#     def refresh_token_in_background(self):
#         # Оновлення токенів через /api/auth/refresh_token
#         self.access_token, self.refresh_token = load_token(FILE_NAME)
#         if self.refresh_token:
#             self.access_token, self.refresh_token = get_refresh_token(self.refresh_token)
#             save_tokens(self.access_token, self.refresh_token)
#
#
# if __name__ == '__main__':
#     auth_manager = AuthManager()
#     asyncio.run(auth_manager.run_app())
#####################################################################################3

import streamlit as st
import extra_streamlit_components as stx
import asyncio
from datetime import datetime
import hydralit_components as hc

from api_pages.src.auth_pages import login_page, signup_page, start_page, profile_page, reset_password_page, request_mail_page, change_avatar_page
from api_pages.src.auth_services import load_token, save_tokens, get_refresh_token, FILE_NAME
from api_pages.src.user_footer import footer


# cookie_manager = stx.CookieManager(key="key01")
# cookies = cookie_manager.get_all(key="key02")
# cookies["access_token"] = None
# st.write(cookies)

# menu_data = [
#     {'id': 'english_name', 'label': "english"},
#     {'id': 'ukrainian_name', 'label': "українська"},
#     {'id': 'russian_name', 'label': "русский", },
#     {'id': 'turkish_name', 'label': "türkçe", },
#
# ]
#
#
# menu_id = hc.nav_bar(
#     menu_definition=menu_data,
#     first_select=0,
#     key=None,
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



class AuthManager:
    def __init__(self):
        self.access_token, self.refresh_token = None, None#st.session_state["access_token"], st.session_state["refresh_token"]# None, None


    async def refresh(self):
        await asyncio.sleep(3500)
        print(f"UPSSS{datetime.now()}")
        new_access_token, new_refresh_token = get_refresh_token(st.session_state["refresh_token"])
        if new_access_token and new_refresh_token:
            self.access_token, self.refresh_token = new_access_token, new_refresh_token
            st.session_state["access_token"] = new_access_token
            st.session_state["refresh_token"] = new_refresh_token
        else:
            st.write("Where are tokens")

    async def login(self):
        if self.access_token and self.refresh_token:
            await profile_page(self.access_token)
        else:
            acc_token, ref_token = login_page()
            if acc_token and ref_token:
                self.access_token, self.refresh_token = acc_token, ref_token
                st.session_state["access_token"] = acc_token
                st.session_state["refresh_token"] = ref_token
                st.write(self.access_token)
                try:
                    await profile_page(self.access_token)
                except TypeError:
                    pass

    async def signup(self):
        if self.access_token:
            st.write("You are already in. Press Logout for SignUp")
        else:
            signup_page()

    async def logout(self):
        # if self.access_token:
        if st.button("Log Out"):
            st.session_state["access_token"] = ""
            st.session_state["refresh_token"] = ""
            st.session_state["username"] = ""
            # cookie_manager.set("refresh_token", "", key="key2")
            # cookie_manager.set("username", "", key="key3")
            self.access_token, self.refresh_token = None, None
            st.write("Login for use all features")
            st.rerun()

    async def run_auth_app(self):
        footer()
        st.sidebar.title("Navigation")
        page = st.sidebar.selectbox(
            "Choose action",
            [
                "SignUp",
                "Login",
                "Logout",
             ]
        )

        if hasattr(self, page.lower()):
            await getattr(self, page.lower())()
        # asyncio.run(self.refresh())
        # st.write(self.access_token, self.refresh_token)


async def main_auth():
    auth_manager = AuthManager()
    await auth_manager.run_auth_app()
    # await auth_manager.refresh()
    # st.write(auth_manager.access_token)


    st.write(st.session_state)

if __name__ == '__main__':
    # main()
    asyncio.run(main_auth())

