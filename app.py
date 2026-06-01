import streamlit as st
from ui import load_ui

load_ui("SAC Analytics Cloud")


try:
    with open("styles.css") as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )
except:
    pass

st.markdown("""
<div style="
display:flex;
align-items:center;
gap:15px;
margin-bottom:20px;
">
    <img src="https://upload.wikimedia.org/wikipedia/commons/5/59/SAP_2011_logo.svg"
         width="90">
    <h1 style="
        margin:0;
        color:#32363a;
        font-size:38px;
        font-weight:700;
    ">
        SAC Analytics Cloud
    </h1>
</div>
""", unsafe_allow_html=True)
st.markdown("""
### Available Modules

Use the left navigation menu:

- Model
- Story
- Planning
- Story Builder
- Content Library

Create SAC-style Models, Stories and Planning applications.
""")
