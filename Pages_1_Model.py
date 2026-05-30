import streamlit as st
import pandas as pd

from utils.calculation_engine import (
    create_calculation
)

from utils.storage import (
    save_model
)

st.title("Model")

uploaded_file = st.file_uploader(
    "Upload CSV / Excel",
    type=["csv", "xlsx"]
)

if uploaded_file:

    if uploaded_file.name.endswith(".csv"):

        df = pd.read_csv(
            uploaded_file
        )

    else:

        df = pd.read_excel(
            uploaded_file
        )

    dimensions = []
    measures = []

    for col in df.columns:

        if (
            pd.api.types.is_numeric_dtype(
                df[col]
            )
            and "id" not in col.lower()
        ):

            measures.append(col)

        else:

            dimensions.append(col)

    st.subheader(
        "Detected Model Structure"
    )

    left, right = st.columns(2)

    with left:

        st.markdown(
            "### Dimensions"
        )

        st.json(dimensions)

    with right:

        st.markdown(
            "### Measures"
        )

        st.json(measures)

    st.divider()

    st.subheader(
        "Calculated Measure"
    )

    if measures:

        measure = st.selectbox(
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
                "Contribution %"
            ]
        )

        new_column = st.text_input(
            "New Measure Name",
            f"{measure}_{calc_type}"
        )

        if st.button(
            "Create Calculation"
        ):

            df = create_calculation(
                df,
                calc_type,
                measure,
                new_column
            )

            st.success(
                "Calculation Created"
            )

    st.divider()

    st.subheader(
        "SAC Style Table"
    )

    display_df = df.copy()

    ordered_columns = (
        dimensions
        +
        [
            col
            for col in display_df.columns
            if col not in dimensions
        ]
    )

    display_df = display_df[
        ordered_columns
    ]

    st.dataframe(
        display_df,
        use_container_width=True,
        height=500
    )

    st.divider()

    model_name = st.text_input(
        "Model Name",
        "Sales_Model"
    )

    if st.button(
        "💾 Save Model"
    ):

        model_object = {
            "dimensions": dimensions,
            "measures": measures,
            "data": display_df
        }

        save_model(
            model_name,
            model_object
        )

        st.success(
            f"{model_name} Saved"
        )
