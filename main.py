import streamlit as st
from register_authenticate import register_authenticate

def load_css_file(css_file_path):
    with open(css_file_path) as f:
        return st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# --- PAGE CONFIG ---
st.set_page_config(
    page_title="A Software by Geoline",
    page_icon=":star:",
    layout="centered",
)

register_authenticate()






