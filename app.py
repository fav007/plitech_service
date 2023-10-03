import pickle
from pathlib import Path

import streamlit_authenticator as stauth
import streamlit as st 

import yaml
from yaml.loader import SafeLoader


st.set_page_config(
   page_title="Plitech Service",
   page_icon="🧊",
)


hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 


file_path = Path(__file__).parent / "config.yaml"

with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

    
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

name, authentication_status,username = authenticator.login("Login","main")

if authentication_status == False:
    st.error("Username/password is incorrect")
    
if authentication_status == None:
    st.warning("Please enter your username and password")
    
if authentication_status:
    st.title("Welcome")
    
    
    
authenticator.logout("Logout","sidebar")
st.sidebar.title(f"Welcome {name}")

 







