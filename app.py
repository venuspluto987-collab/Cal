import streamlit as st

st.set_page_config(
    page_title="SAC Analytics Cloud",
    page_icon="📊",
    layout="wide"
)

try:
    with open("styles.css") as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )
except:
    pass

st.title("📊 SAC Analytics Cloud")

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
