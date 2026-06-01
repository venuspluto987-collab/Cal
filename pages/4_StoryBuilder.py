import streamlit as st
import pandas as pd
import plotly.express as px

from utils.storage import (
    load_models,
    load_story_objects,
    load_planning_objects
)
from ui import load_ui

load_ui("Story Builder")


st.title("📖 Story Builder")

# =====================================================
# LOAD DATA
# =====================================================

models = load_models()
story_objects = load_story_objects()
planning_objects = load_planning_objects()

# =====================================================
# HEADER SETTINGS
# =====================================================

st.sidebar.header("Story Settings")

story_title = st.sidebar.text_input(
    "Story Name",
    "Executive Dashboard"
)

header_color = st.sidebar.color_picker(
    "Header Color",
    "#0F62FE"
)

layout_type = st.sidebar.selectbox(
    "Layout",
    [
        "1 Column",
        "2 Columns",
        "3 Columns"
    ]
)

# =====================================================
# HEADER
# =====================================================

st.markdown(
    f"""
    <div style="
        background:{header_color};
        padding:15px;
        border-radius:10px;
        color:white;
        font-size:30px;
        font-weight:bold;
        margin-bottom:20px;
    ">
        {story_title}
    </div>
    """,
    unsafe_allow_html=True
)

# =====================================================
# AVAILABLE OBJECTS
# =====================================================

available_widgets = []

for x in story_objects.keys():
    available_widgets.append(x)

for x in planning_objects.keys():
    available_widgets.append(x)

if len(available_widgets) == 0:

    st.warning(
        "No Saved Story or Planning Objects Found"
    )

    st.stop()

selected_widgets = st.multiselect(
    "Select Widgets",
    available_widgets,
    default=available_widgets
)

# =====================================================
# RENDER FUNCTION
# =====================================================

def render_widget(widget_name):

    # -----------------------------------
    # STORY OBJECTS
    # -----------------------------------

    if widget_name in story_objects:

        obj = story_objects[widget_name]

        model_name = obj["model"]

        if model_name not in models:
            return

        df = pd.DataFrame(
            models[model_name]["data"]
        )

        # ================================
        # TABLE
        # ================================

        if obj["type"] == "table":

            st.subheader(widget_name)

            cols = obj["columns"]

            st.dataframe(
                df[cols],
                use_container_width=True
            )

        # ================================
        # CHART
        # ================================

        elif obj["type"] == "chart":

            x = obj["x"]
            y = obj["y"]
            chart_type = obj["chart_type"]

            chart_df = (
                df.groupby(x)[y]
                .sum()
                .reset_index()
            )

            fig = None

            if chart_type == "Bar":

                fig = px.bar(
                    chart_df,
                    x=x,
                    y=y
                )

            elif chart_type == "Line":

                fig = px.line(
                    chart_df,
                    x=x,
                    y=y
                )

            elif chart_type == "Area":

                fig = px.area(
                    chart_df,
                    x=x,
                    y=y
                )

            elif chart_type == "Pie":

                fig = px.pie(
                    chart_df,
                    names=x,
                    values=y
                )

            elif chart_type == "Scatter":

                fig = px.scatter(
                    chart_df,
                    x=x,
                    y=y
                )

            st.subheader(widget_name)

            st.plotly_chart(
                fig,
                use_container_width=True
            )

    # -----------------------------------
    # PLANNING OBJECTS
    # -----------------------------------

    elif widget_name in planning_objects:

        obj = planning_objects[
            widget_name
        ]

        st.subheader(widget_name)

        if "data" in obj:

            plan_df = pd.DataFrame(
                obj["data"]
            )

            st.dataframe(
                plan_df,
                use_container_width=True
            )

# =====================================================
# LAYOUT RENDER
# =====================================================

if layout_type == "1 Column":

    for widget in selected_widgets:

        render_widget(widget)

elif layout_type == "2 Columns":

    col1, col2 = st.columns(2)

    for i, widget in enumerate(
        selected_widgets
    ):

        if i % 2 == 0:

            with col1:

                render_widget(widget)

        else:

            with col2:

                render_widget(widget)

elif layout_type == "3 Columns":

    col1, col2, col3 = st.columns(3)

    for i, widget in enumerate(
        selected_widgets
    ):

        if i % 3 == 0:

            with col1:

                render_widget(widget)

        elif i % 3 == 1:

            with col2:

                render_widget(widget)

        else:

            with col3:

                render_widget(widget)

# =====================================================
# KPI SECTION
# =====================================================

st.divider()

st.subheader("KPI Widgets")

selected_model = st.selectbox(
    "Model",
    list(models.keys()),
    key="kpi_model"
)

df = pd.DataFrame(
    models[selected_model]["data"]
)

numeric_cols = list(
    df.select_dtypes(
        include="number"
    ).columns
)

if len(numeric_cols) > 0:

    selected_measure = st.selectbox(
        "Measure",
        numeric_cols
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Total",
        round(
            df[selected_measure].sum(),
            2
        )
    )

    c2.metric(
        "Average",
        round(
            df[selected_measure].mean(),
            2
        )
    )

    c3.metric(
        "Maximum",
        round(
            df[selected_measure].max(),
            2
        )
    )

    c4.metric(
        "Minimum",
        round(
            df[selected_measure].min(),
            2
        )
    )

from fpdf import FPDF
import tempfile

# =====================================================
# EXPORT DASHBOARD
# =====================================================

st.divider()

if st.button("Generate PDF"):

    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, story_title, ln=True)

    pdf.ln(5)

    pdf.set_font("Arial", "", 12)

    pdf.cell(0, 8, f"Layout: {layout_type}", ln=True)

    pdf.ln(5)

    pdf.cell(0, 8, "Widgets:", ln=True)

    for widget in selected_widgets:
        pdf.cell(0, 8, f"- {widget}", ln=True)

    pdf_bytes = bytes(pdf.output(dest="S"))

    st.download_button(
        label="⬇ Export Dashboard PDF",
        data=pdf_bytes,
        file_name="dashboard.pdf",
        mime="application/pdf"
    )
