import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Planning",
    layout="wide"
)

st.title("📈 Planning")

# =====================================================
# IMPORT STORAGE FUNCTIONS
# =====================================================

try:
    from utils.storage import (
        load_models,
        save_planning_object
    )
except Exception as e:
    st.error(f"Import Error: {e}")
    st.stop()

# =====================================================
# LOAD MODELS
# =====================================================

try:
    models = load_models()
except Exception as e:
    st.error(f"Model Load Error: {e}")
    st.stop()

if not models:
    st.warning("No Models Available")
    st.stop()

# =====================================================
# MODEL SELECTION
# =====================================================

model_name = st.selectbox(
    "Select Model",
    list(models.keys())
)

model = models[model_name]

df = pd.DataFrame(model["data"])

measures = model.get("measures", [])
dimensions = model.get("dimensions", [])

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
        measures
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
        "Driver Measure",
        measures
    )

    allocation_amount = st.number_input(
        "Allocation Amount",
        value=100000.0
    )

    target_column = st.text_input(
        "Target Column",
        "Allocated_Value"
    )

    if st.button("Run Allocation"):

        result_df = df.copy()

        total_driver = result_df[driver_measure].sum()

        if total_driver == 0:
            st.error("Driver total cannot be zero")
        else:

            result_df[target_column] = (
                (
                    result_df[driver_measure]
                    / total_driver
                )
                * allocation_amount
            ).round(2)

            st.success("Allocation Complete")

            st.dataframe(
                result_df,
                use_container_width=True
            )

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
        measures
    )

    condition = st.selectbox(
        "Condition",
        ["<", ">", "="]
    )

    threshold = st.number_input(
        "Threshold",
        value=1000.0
    )

    if st.button("Run Deletion"):

        result_df = df.copy()

        if condition == "<":
            result_df = result_df[
                result_df[delete_measure] >= threshold
            ]

        elif condition == ">":
            result_df = result_df[
                result_df[delete_measure] <= threshold
            ]

        else:
            result_df = result_df[
                result_df[delete_measure] != threshold
            ]

        st.success(
            f"{len(df) - len(result_df)} rows removed"
        )

        st.dataframe(
            result_df,
            use_container_width=True
        )

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

    other_models = [
        x for x in models.keys()
        if x != model_name
    ]

    if not other_models:
        st.warning("No second model available")

    else:

        second_model = st.selectbox(
            "Target Model",
            other_models
        )

        cross_df = pd.DataFrame(
            models[second_model]["data"]
        )

        common_cols = list(
            set(df.columns)
            & set(cross_df.columns)
        )

        if common_cols:

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

    increase_pct = st.number_input(
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
            * (1 + increase_pct / 100)
        ).round(2)

        st.success("Version Created")

        st.dataframe(
            version_df,
            use_container_width=True
        )

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

    st.subheader("Editable Planning Grid")

    edited_df = st.data_editor(
        df,
        use_container_width=True,
        num_rows="dynamic"
    )

    if st.button("Save Edited Data"):

        save_planning_object(
            "Editable_Planning",
            {
                "type": "editable_table",
                "data": edited_df.to_dict("records")
            }
        )

        st.success(
            "Planning Data Saved Successfully"
        )
