import streamlit as st
import pandas as pd

from utils.storage import save_model
from utils.calculation_engine import (
    apply_calculation,
    custom_formula
)

st.set_page_config(layout="wide")

st.title("📦 Model")

# =====================================================
# UPLOAD
# =====================================================

uploaded_file = st.file_uploader(
    "Upload CSV / Excel",
    type=["csv", "xlsx"]
)

if uploaded_file:

    # =================================================
    # READ FILE
    # =================================================

    try:

        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)

        else:
            df = pd.read_excel(uploaded_file)

    except Exception as e:

        st.error(f"File Error: {e}")
        st.stop()

    # =================================================
    # DETECT DIMENSIONS / MEASURES
    # =================================================

    dimensions = []
    measures = []

    for col in df.columns:

        if (
            pd.api.types.is_numeric_dtype(df[col])
            and "id" not in col.lower()
        ):

            measures.append(col)

        else:

            dimensions.append(col)

    # =================================================
    # MODEL STRUCTURE
    # =================================================

    st.subheader("Model Structure")

    left, right = st.columns(2)

    with left:

        st.markdown("### Dimensions")

        for d in dimensions:

            st.markdown(
                f"""
                <div class='dimension-item'>
                    {d}
                </div>
                """,
                unsafe_allow_html=True
            )

    with right:

        st.markdown("### Measures")

        for m in measures:

            st.markdown(
                f"""
                <div class='measure-item'>
                    {m}
                </div>
                """,
                unsafe_allow_html=True
            )

    st.divider()

    # =================================================
    # CALCULATED MEASURE
    # =================================================

    st.subheader("Calculated Measures")

    if measures:

        calc_measure = st.selectbox(
            "Measure",
            measures
        )

        calc_type = st.selectbox(
            "Calculation",
            [
                "Running Total",
                "Moving Average",
                "Growth %",
                "Rank",
                "Contribution %",
                "Min",
                "Max",
                "Average",
                "Variance",
                "Standard Deviation"
            ]
        )

        new_measure = st.text_input(
            "New Measure Name",
            f"{calc_measure}_{calc_type}"
        )

        if st.button(
            "Create Calculated Measure"
        ):

            df = apply_calculation(
                df,
                calc_type,
                calc_measure,
                new_measure
            )

            if new_measure not in measures:
                measures.append(new_measure)

            st.success(
                f"{new_measure} Created"
            )

    st.divider()

    # =================================================
    # CUSTOM FORMULA
    # =================================================

    st.subheader("Custom Formula")

    st.info(
        "Example: Sales - Cost"
    )

    formula = st.text_input(
        "Formula"
    )

    custom_measure = st.text_input(
        "Calculated Column Name",
        "Custom_Calculation"
    )

    if st.button(
        "Apply Formula"
    ):

        if formula:

            df = custom_formula(
                df,
                formula,
                custom_measure
            )

            if custom_measure not in measures:
                measures.append(custom_measure)

            st.success(
                f"{custom_measure} Created"
            )

    st.divider()

    # =================================================
    # SAC TABLE VIEW
    # =================================================

    st.subheader("SAC Style Table")

    ordered_columns = (
        dimensions
        +
        [
            c
            for c in df.columns
            if c not in dimensions
        ]
    )

    table_df = df[
        ordered_columns
    ]

    # -------------------------------------------------
    # DISPLAY MODEL STRUCTURE ABOVE TABLE
    # -------------------------------------------------

    c1, c2 = st.columns([1, 1])

    with c1:

        st.markdown("### Dimensions")

        st.json(dimensions)

    with c2:

        st.markdown("### Measures")

        st.json(
            [
                c
                for c in table_df.columns
                if c not in dimensions
            ]
        )

    # -------------------------------------------------
    # DATA TABLE
    # -------------------------------------------------

    st.dataframe(
        table_df,
        use_container_width=True,
        height=500
    )

    st.divider()

    # =================================================
    # SAVE MODEL
    # =================================================

    st.subheader("Save Model")

    model_name = st.text_input(
        "Model Name",
        "Sales_Model"
    )

    if st.button(
        "💾 Save Model"
    ):

        model_object = {

            "dimensions": dimensions,

            "measures": [
                c
                for c in table_df.columns
                if c not in dimensions
            ],

            "data": table_df
        }

        save_model(
            model_name,
            model_object
        )

        st.success(
            f"{model_name} Saved Successfully"
        )

        st.balloons()

else:

    st.info(
        "Upload CSV or Excel File"
    )
