from st_pages import hide_pages
from time import sleep
import streamlit as st
import globals 
from start import initialize

df_items,df_full,df_pref,df_logusers,df_users=initialize()


def log_out():
    st.session_state["logged_in"] = False
    st.success("Logged out!")
    sleep(0.5)


if not st.session_state.get("logged_in", False):
    hide_pages(["page1","page2"])
    username = st.text_input("Username", key="username")
    password = st.text_input("Password", key="password", type="password") 
    list_users_passwords=df_logusers
    user_exists = ((list_users_passwords['User'] == username) & (list_users_passwords['Password'] == password)).any()

    if user_exists:
        user=list_users_passwords[(list_users_passwords['User'] == username) & (list_users_passwords['Password'] == password)].index.tolist()
        print(user)
        globals.user=user[0]
        st.session_state["logged_in"] = True
        st.success("Logged in!")
        hide_pages([])
        sleep(0.5)
        st.switch_page("pages/page1.py")

    if st.button('Registrar'):
        st.switch_page("pages/page2.py")
else:
    st.write("Logged in!")
    st.button("log out", on_click=log_out)


