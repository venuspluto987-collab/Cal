import streamlit as st

def load_ui(page_title):

    st.set_page_config(
        page_title=page_title,
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
