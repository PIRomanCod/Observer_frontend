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

from pages.src.auth_pages import login_page, signup_page, start_page, profile_page, reset_password_page, request_mail_page, change_avatar_page
from pages.src.auth_services import load_token, save_tokens, get_refresh_token, FILE_NAME
from pages.src.user_footer import footer

cookie_manager = stx.CookieManager()
cookies = cookie_manager.get_all()
# st.write(cookies)


class AuthManager:
    def __init__(self):
        self.access_token, self.refresh_token = None, None
        # self.session_id = cookie_manager.get("ajs_anonymous_id")
        # if not self.access_token:
        #     start_page()
    #     self.loop = asyncio.get_event_loop()
    #     self.run_refresh_loop()
    #
    # def run_refresh_loop(self):
    #     self.loop.create_task(self.refresh_loop())
    #
    # async def refresh_loop(self):
    #     print("WTFFF1")
    #
    #     while True:
    #         print("WTFFF2")
    #         await asyncio.sleep(10)
    #         await self.refresh_token_in_background()

    async def refresh(self):
        await asyncio.sleep(60)
        print(f"UPSSS{datetime.now()}")
        new_access_token, new_refresh_token = get_refresh_token(cookie_manager.get("refresh_token"))
        if new_access_token and new_refresh_token:
            self.access_token, self.refresh_token = new_access_token, new_refresh_token
            cookie_manager.set("refresh_token", new_refresh_token, key="key2")
            cookie_manager.set("access_token", new_access_token, key="key1")
        else:
            st.write("Where are tokens")

    def login(self):
        acc_token, ref_token = login_page()
        if acc_token and ref_token:
            self.access_token, self.refresh_token = acc_token, ref_token
            cookie_manager.set("refresh_token", self.refresh_token, key="key2")
            cookie_manager.set("access_token", self.access_token, key="key1")

    def signup(self):
        if self.access_token:
            st.write("You are already in. Press Logout for SignUp")
        else:
            signup_page()

    def logout(self):
        # if self.access_token:
        if st.button("Log Out"):
            self.access_token, self.refresh_token = None, None
            cookie_manager.set("access_token", "", key="key1")
            cookie_manager.set("refresh_token", "", key="key2")
            st.write("Login for use all features")
            st.rerun()

    def run_app(self):
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
            getattr(self, page.lower())()
        asyncio.run(self.refresh())
        # st.write(self.access_token, self.refresh_token)


def main():
    auth_manager = AuthManager()
    auth_manager.run_app()
    # st.write(auth_manager.access_token)


if __name__ == '__main__':
    main()
    # asyncio.run(main())
