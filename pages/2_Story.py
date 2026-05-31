import streamlit as st
import pandas as pd
import plotly.express as px

from utils.storage import (
    get_models,
    load_model,
    save_widget
)
from ui import load_ui

load_ui("Story")
st.title("📊 Story")

# =====================================================
# LOAD MODEL
# =====================================================

models = get_models()

if not models:
    st.warning("No Saved Models Found")
    st.stop()

selected_model = st.selectbox(
    "Select Model",
    models,
    key="selected_model"
)

model = load_model(selected_model)

if model is None:
    st.error("Unable to load model")
    st.stop()

df = model["data"]
dimensions = model["dimensions"]

# Include calculated measures too
measures = [
    c
    for c in df.columns
    if c not in dimensions
]

# =====================================================
# VALIDATION
# =====================================================

if len(dimensions) == 0:
    st.error("No dimensions found in model.")
    st.stop()

if len(measures) == 0:
    st.error("No measures found in model.")
    st.stop()

# =====================================================
# KPI SECTION
# =====================================================

st.subheader("KPI Dashboard")

selected_kpi = st.selectbox(
    "KPI Measure",
    measures,
    key="kpi_measure"
)

k1, k2, k3, k4 = st.columns(4)

with k1:
    st.metric(
        "Total",
        round(df[selected_kpi].sum(), 2)
    )

with k2:
    st.metric(
        "Average",
        round(df[selected_kpi].mean(), 2)
    )

with k3:
    st.metric(
        "Maximum",
        round(df[selected_kpi].max(), 2)
    )

with k4:
    st.metric(
        "Minimum",
        round(df[selected_kpi].min(), 2)
    )

# =====================================================
# FILTERS
# =====================================================

st.divider()

st.subheader("Filters")

filter_df = df.copy()

filter_dimension = st.selectbox(
    "Filter Dimension",
    dimensions,
    key="filter_dimension"
)

values = st.multiselect(
    "Select Values",
    filter_df[filter_dimension].astype(str).unique(),
    default=filter_df[filter_dimension].astype(str).unique(),
    key="filter_values"
)

filter_df = filter_df[
    filter_df[filter_dimension].astype(str).isin(values)
]

# =====================================================
# CHART BUILDER
# =====================================================

st.divider()

st.subheader("Chart Builder")

c1, c2, c3 = st.columns(3)

with c1:
    x_axis = st.selectbox(
        "Dimension",
        dimensions,
        key="chart_dimension"
    )

with c2:
    y_axis = st.selectbox(
        "Measure",
        measures,
        key="chart_measure"
    )

with c3:
    chart_type = st.selectbox(
        "Chart Type",
        [
            "Bar",
            "Line",
            "Area",
            "Pie",
            "Scatter"
        ],
        key="chart_type"
    )

# =====================================================
# BUILD CHART
# =====================================================

fig = None

if chart_type == "Bar":

    fig = px.bar(
        filter_df,
        x=x_axis,
        y=y_axis
    )

elif chart_type == "Line":

    fig = px.line(
        filter_df,
        x=x_axis,
        y=y_axis
    )

elif chart_type == "Area":

    fig = px.area(
        filter_df,
        x=x_axis,
        y=y_axis
    )

elif chart_type == "Pie":

    fig = px.pie(
        filter_df,
        names=x_axis,
        values=y_axis
    )

elif chart_type == "Scatter":

    fig = px.scatter(
        filter_df,
        x=x_axis,
        y=y_axis
    )

# Main Chart
st.plotly_chart(
    fig,
    use_container_width=True,
    key="main_chart"
)

# =====================================================
# SAVE CHART
# =====================================================

chart_name = st.text_input(
    "Chart Name",
    "Revenue_Chart",
    key="chart_name"
)

if st.button(
    "💾 Save Chart",
    key="save_chart_btn"
):

    save_widget(
        chart_name,
        {
            "type": "chart",
            "chart_type": chart_type,
            "x": x_axis,
            "y": y_axis,
            "model": selected_model
        }
    )

    st.success("Chart Saved")

# =====================================================
# TABLE BUILDER
# =====================================================

st.divider()

st.subheader("Table Builder")

table_columns = st.multiselect(
    "Select Columns",
    df.columns.tolist(),
    default=df.columns.tolist(),
    key="table_columns"
)

table_df = filter_df[table_columns]

st.dataframe(
    table_df,
    use_container_width=True,
    height=450
)

# =====================================================
# SAVE TABLE
# =====================================================

table_name = st.text_input(
    "Table Name",
    "Sales_Table",
    key="table_name"
)

if st.button(
    "💾 Save Table",
    key="save_table_btn"
):

    save_widget(
        table_name,
        {
            "type": "table",
            "columns": table_columns,
            "model": selected_model
        }
    )

    st.success("Table Saved")

# =====================================================
# STORY PREVIEW
# =====================================================

st.divider()

st.subheader("Story Preview")

left, right = st.columns([2, 1])

with left:

    st.plotly_chart(
        fig,
        use_container_width=True,
        key="preview_chart"
    )

with right:

    st.dataframe(
        table_df.head(10),
        use_container_width=True,
        height=300
    )
