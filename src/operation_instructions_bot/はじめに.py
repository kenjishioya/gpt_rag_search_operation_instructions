import streamlit as st
from views.common import init_screen

st.set_page_config(layout='wide')
init_screen()
with open('./assets/introduction.md', 'r') as f:
    readme = f.read()
st.markdown(readme)