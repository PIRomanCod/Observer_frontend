import streamlit as st
import requests
import asyncio
from datetime import datetime, timedelta


import os
import dotenv
import configparser
import json
dotenv.load_dotenv()

config = configparser.ConfigParser()
config.read("config.ini")

SERVER_URL = os.getenv("APP_URL")


class AuthenticationApp:
    def __init__(self):
        self.access_token = None
        self.refresh_token = None
        self.last_refresh_time = None

    async def get_current_user(self):
        headers = {"Authorization": f"Bearer {self.access_token}"}
        response = requests.get(f"{SERVER_URL}/api/users/me/", headers=headers)
        if response.status_code == 200:
            return response.json()
        return None

    async def refresh_access_token(self):
        headers = {"Authorization": f"Bearer {self.refresh_token}"}
        response = requests.get(f"{SERVER_URL}/api/auth/refresh_token", headers=headers)
        if response.status_code == 200:
            if response.json().get("access_token"):
                return response.json()["access_token"], response.json()["refresh_token"]
            return None, None
        else:
            return None


    async def main_auth(self):
        # Set the page title
        # st.set_page_config(page_title="Authentication App")

        # # Add a header to the page
        # st.header("Authentication App")

        # Add a sidebar to the page
        sidebar = st.sidebar
        sidebar.title("Actions")
        action = sidebar.radio("Choose an action", ["Login", "Register", "Logout"])

        # Handle the login action
        if action == "Login":
            # Add a form for user login
            if self.access_token:
                st.write("You are already In")
            else:
                with st.form("login_form"):
                    email = st.text_input("Email")
                    password = st.text_input("Password", type="password")
                    submit_button = st.form_submit_button("Log In")

                    if submit_button:
                        try:
                            data = {"username": email, "password": password}
                            response = requests.post(f"{SERVER_URL}/api/auth/login", data=data)
                            if response.status_code == 200:
                                access_token = response.json()["access_token"]
                                refresh_token = response.json()["refresh_token"]
                                # Save the access token and refresh token in the object
                                self.access_token = access_token
                                self.refresh_token = refresh_token
                                self.last_refresh_time = datetime.now()
                                st.session_state["access_token"] = self.access_token
                                st.session_state["refresh_token"] = self.refresh_token
                                st.success("Login successful")

                            elif response.json().get("detail") == "Email not confirmed":
                                return "Email not confirmed"
                            # else:
                            #     st.error("An error occurred while logging in")
                        except requests.exceptions.RequestException as e:
                            st.error("An error occurred while logging in")


        # Handle the registration action
        elif action == "Register":
            # Add a form for user registration
            with st.form("signup_form"):
                username = st.text_input("Username")
                email = st.text_input("Email")
                password = st.text_input("Password", type="password")
                password_confirm = st.text_input("Confirm password", type="password")

                submit_button = st.form_submit_button("Sign Up")

                if submit_button:
                    try:
                        if password == password_confirm:
                            data = {"username": username, "email": email, "password": password}
                            response = requests.post(f"{SERVER_URL}/api/auth/signup", data=json.dumps(data))
                            if response.json().get("id"):
                                st.success(f"Success. Check email: {email} and verify")
                            else:
                                st.error(f"{response.json()['detail']}")

                        else:
                            st.error("Password not match")

                    except requests.exceptions.RequestException as e:
                        st.error("An error occurred while registering")

                        return response.json()


        # Handle the logout action
        elif action == "Logout":
            # Delete the access token and refresh token from the object
            self.access_token = None
            self.refresh_token = None
            self.last_refresh_time = None
            st.session_state["username"] = None
            st.session_state["access_token"] = None
            st.session_state["refresh_token"] = None
            st.success("Logged out successfully")

        # Check if the user is logged in
        if self.access_token and self.refresh_token:
            # Get the current user
            user = await self.get_current_user()

            # Display the user's information
            if user:
                st.session_state["username"] = user['username']
                st.write(f"Welcome, {user['username']}!")

                # Refresh the access token every 25 minutes
                now = datetime.now()
                if now - self.last_refresh_time > timedelta(minutes=25):
                    new_tokens = await self.refresh_access_token()
                    if new_tokens:
                        self.access_token = new_tokens[0]
                        self.refresh_token = new_tokens[1]
                        self.last_refresh_time = now
                        st.session_state["access_token"] = self.access_token
                        st.session_state["refresh_token"] = self.refresh_token

    def run_auth_app(self):
        asyncio.run(self.main_auth())


auth_manager = None


async def main_auth():
    # Використання глобального об'єкта auth_manager
    global auth_manager
    if auth_manager is None:
        auth_manager = AuthenticationApp()
    await auth_manager.main_auth()


if __name__ == '__main__':
    asyncio.run(main_auth())

