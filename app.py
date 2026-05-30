import streamlit as st

st.set_page_config(
    page_title="SAC Analytics Cloud",
    page_icon="📊",
    layout="wide"
)

with open("styles.css") as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )

st.title("📊 SAC Analytics Cloud")

st.markdown("""
### Modules

Use left navigation menu:

- Model
- Story
- Planning
- Story Builder
- Content Library
""")
