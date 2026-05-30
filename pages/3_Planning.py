import streamlit as st
import pandas as pd

from utils.storage import (
    load_models,
    save_planning_object
)

st.set_page_config(
    page_title="Planning",
    layout="wide"
)

st.title("📈 Planning")

# =====================================================
# LOAD MODELS
# =====================================================

models = load_models()

if len(models) == 0:

    st.warning(
        "No Models Available"
    )

    st.stop()

# =====================================================
# MODEL SELECTION
# =====================================================

model_name = st.selectbox(
    "Select Model",
    list(models.keys())
)

model = models[model_name]

df = pd.DataFrame(
    model["data"]
)

measures = model["measures"]
dimensions = model["dimensions"]

# =====================================================
# PLANNING ACTIONS
# =====================================================

planning_action = st.selectbox(
    "Planning Action",
    [
        "Copy Model",
        "Allocation",
        "Fact Deletion",
        "Cross Model",
        "Version Copy",
        "Editable Planning Table"
    ]
)

# =====================================================
# COPY MODEL
# =====================================================

if planning_action == "Copy Model":

    st.subheader("Copy Measure")

    source_measure = st.selectbox(
        "Source Measure",
        measures,
        key="copy_source"
    )

    target_measure = st.text_input(
        "Target Measure",
        "Copied_Value"
    )

    increase_pct = st.number_input(
        "Increase %",
        value=0.0
    )

    if st.button("Run Copy"):

        result_df = df.copy()

        result_df[target_measure] = (
            result_df[source_measure]
            * (1 + increase_pct / 100)
        ).round(2)

        st.success("Copy Complete")

        st.dataframe(
            result_df,
            use_container_width=True
        )

        if st.button("Save Result"):

            save_planning_object(
                target_measure,
                {
                    "type": "copy_model",
                    "data": result_df.to_dict("records")
                }
            )

# =====================================================
# ALLOCATION
# =====================================================

elif planning_action == "Allocation":

    st.subheader("Allocation")

    driver_measure = st.selectbox(
        "Driver",
        measures,
        key="driver_measure"
    )

    allocation_amount = st.number_input(
        "Allocation Amount",
        value=100000.0
    )

    target_column = st.text_input(
        "Allocated Column",
        "Allocated_Value"
    )

    if st.button("Run Allocation"):

        result_df = df.copy()

        total = result_df[
            driver_measure
        ].sum()

        result_df[target_column] = (
            (
                result_df[driver_measure]
                / total
            )
            * allocation_amount
        ).round(2)

        st.success("Allocation Complete")

        st.dataframe(
            result_df,
            use_container_width=True
        )

        if st.button("Save Allocation"):

            save_planning_object(
                target_column,
                {
                    "type": "allocation",
                    "data": result_df.to_dict("records")
                }
            )

# =====================================================
# FACT DELETION
# =====================================================

elif planning_action == "Fact Deletion":

    st.subheader("Fact Deletion")

    delete_measure = st.selectbox(
        "Measure",
        measures,
        key="delete_measure"
    )

    condition = st.selectbox(
        "Condition",
        [
            "<",
            ">",
            "="
        ]
    )

    threshold = st.number_input(
        "Threshold",
        value=1000.0
    )

    if st.button("Run Deletion"):

        result_df = df.copy()

        if condition == "<":

            result_df = result_df[
                result_df[
                    delete_measure
                ] >= threshold
            ]

        elif condition == ">":

            result_df = result_df[
                result_df[
                    delete_measure
                ] <= threshold
            ]

        elif condition == "=":

            result_df = result_df[
                result_df[
                    delete_measure
                ] != threshold
            ]

        st.success(
            f"{len(df)-len(result_df)} rows removed"
        )

        st.dataframe(
            result_df,
            use_container_width=True
        )

        if st.button("Save Deletion Result"):

            save_planning_object(
                "Fact_Deletion",
                {
                    "type": "fact_deletion",
                    "data": result_df.to_dict("records")
                }
            )

# =====================================================
# CROSS MODEL
# =====================================================

elif planning_action == "Cross Model":

    st.subheader("Cross Model Merge")

    second_model = st.selectbox(
        "Target Model",
        [
            x for x in models.keys()
            if x != model_name
        ]
    )

    if second_model:

        cross_df = pd.DataFrame(
            models[second_model]["data"]
        )

        common_cols = list(
            set(df.columns)
            &
            set(cross_df.columns)
        )

        if len(common_cols) > 0:

            join_column = st.selectbox(
                "Join Column",
                common_cols
            )

            if st.button("Merge Models"):

                merged_df = pd.merge(
                    df,
                    cross_df,
                    on=join_column,
                    how="left"
                )

                st.success(
                    "Cross Model Completed"
                )

                st.dataframe(
                    merged_df,
                    use_container_width=True
                )

                if st.button("Save Cross Model"):

                    save_planning_object(
                        "Cross_Model",
                        {
                            "type": "cross_model",
                            "data": merged_df.to_dict("records")
                        }
                    )

        else:

            st.error(
                "No common columns found"
            )

# =====================================================
# VERSION COPY
# =====================================================

elif planning_action == "Version Copy":

    st.subheader("Version Planning")

    source_version = st.text_input(
        "Source Version",
        "Actual"
    )

    target_version = st.text_input(
        "Target Version",
        "Budget"
    )

    increase = st.number_input(
        "Increase %",
        value=10.0
    )

    version_measure = st.selectbox(
        "Measure",
        measures
    )

    if st.button("Run Version Copy"):

        version_df = df.copy()

        version_df["Version"] = target_version

        version_df[version_measure] = (
            version_df[version_measure]
            * (1 + increase/100)
        ).round(2)

        st.dataframe(
            version_df,
            use_container_width=True
        )

        if st.button("Save Version"):

            save_planning_object(
                target_version,
                {
                    "type": "version_copy",
                    "data": version_df.to_dict("records")
                }
            )

# =====================================================
# EDITABLE PLANNING TABLE
# =====================================================

elif planning_action == "Editable Planning Table":

    st.subheader("Planning Grid")

    editable_df = st.data_editor(
        df,
        use_container_width=True,
        num_rows="dynamic"
    )

    if st.button("Save Edited Data"):

        save_planning_object(
            "Editable_Planning",
            {
                "type": "editable_table",
                "data": editable_df.to_dict("records")
            }
        )

        st.success(
            "Planning Data Saved"
        )
