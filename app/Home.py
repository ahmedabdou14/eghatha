import streamlit as st
from PIL import Image
import pathlib

try:
    im = Image.open(pathlib.Path("./app/public/eghatha.jpg").absolute())
except Exception:
    im = Image.open(pathlib.Path("./public/eghatha.jpg").absolute())

st.set_page_config(
    page_title="Eghatha",
    page_icon=im,
    layout="centered",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": "https://www.extreme.com",
        "Report a bug": "https://www.extreme.com",
        "About": "https://www.extreme.com",
    },
)

def main():
    st.markdown("<center> <h1>Eghatha</h1> </center>", unsafe_allow_html=True)

main()