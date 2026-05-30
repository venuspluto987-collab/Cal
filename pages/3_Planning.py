import streamlit as st
import pandas as pd

from utils.storage import (
get_models,
load_model,
save_planning,
get_planning
)

st.set_page_config(
page_title="Planning",
layout="wide"
)

st.title("📈 SAC Planning")

# =====================================================

# LOAD MODELS

# =====================================================

model_names = get_models()

if not model_names:
st.warning("No Models Available")
st.stop()

selected_model = st.selectbox(
"Select Source Model",
model_names
)

try:
model = load_model(selected_model)
except Exception as e:
st.error(f"Error Loading Model: {e}")
st.stop()

df = model["data"]

if not isinstance(df, pd.DataFrame):
df = pd.DataFrame(df)

dimensions = model.get("dimensions", [])
measures = model.get("measures", [])

# =====================================================

# PLANNING MENU

# =====================================================

planning_action = st.selectbox(
"Planning Function",
[
"Copy Action",
"Allocation",
"Embedded Data Action",
"Cross Model",
"Version Management",
"Planning Grid",
"Planning Repository"
]
)

# =====================================================

# COPY ACTION

# =====================================================

if planning_action == "Copy Action":

```
st.subheader("Copy Measure")

source_measure = st.selectbox(
    "Source Measure",
    measures
)

target_measure = st.text_input(
    "Target Measure",
    f"{source_measure}_COPY"
)

adjustment_pct = st.number_input(
    "Adjustment %",
    value=0.0
)

if st.button("Execute Copy"):

    result = df.copy()

    result[target_measure] = (
        result[source_measure]
        * (1 + adjustment_pct / 100)
    ).round(2)

    st.dataframe(
        result,
        use_container_width=True
    )

    save_planning(
        target_measure,
        {
            "type": "Copy Action",
            "data": result.to_dict("records")
        }
    )

    st.success("Copy Action Saved")
```

# =====================================================

# ALLOCATION

# =====================================================

elif planning_action == "Allocation":

```
st.subheader("Allocation Data Action")

driver = st.selectbox(
    "Driver Measure",
    measures
)

allocation_amount = st.number_input(
    "Allocation Amount",
    value=100000.0
)

target_measure = st.text_input(
    "Target Measure",
    "Allocated_Value"
)

if st.button("Run Allocation"):

    result = df.copy()

    total_driver = result[driver].sum()

    if total_driver == 0:
        st.error("Driver total cannot be zero")
    else:

        result[target_measure] = (
            result[driver]
            / total_driver
        ) * allocation_amount

        result[target_measure] = (
            result[target_measure]
            .round(2)
        )

        st.dataframe(
            result,
            use_container_width=True
        )

        save_planning(
            target_measure,
            {
                "type": "Allocation",
                "data": result.to_dict("records")
            }
        )

        st.success("Allocation Saved")
```

# =====================================================

# EMBEDDED DATA ACTION

# =====================================================

elif planning_action == "Embedded Data Action":

```
st.subheader("Embedded Formula")

measure1 = st.selectbox(
    "Measure 1",
    measures,
    key="m1"
)

operator = st.selectbox(
    "Operator",
    ["+", "-", "*", "/"]
)

measure2 = st.selectbox(
    "Measure 2",
    measures,
    key="m2"
)

target_measure = st.text_input(
    "Result Measure",
    "Calculated_Measure"
)

if st.button("Run Data Action"):

    result = df.copy()

    if operator == "+":
        result[target_measure] = (
            result[measure1]
            + result[measure2]
        )

    elif operator == "-":
        result[target_measure] = (
            result[measure1]
            - result[measure2]
        )

    elif operator == "*":
        result[target_measure] = (
            result[measure1]
            * result[measure2]
        )

    elif operator == "/":
        result[target_measure] = (
            result[measure1]
            / result[measure2]
        )

    st.dataframe(
        result,
        use_container_width=True
    )

    save_planning(
        target_measure,
        {
            "type": "Embedded Data Action",
            "data": result.to_dict("records")
        }
    )

    st.success("Data Action Saved")
```

# =====================================================

# CROSS MODEL

# =====================================================

elif planning_action == "Cross Model":

```
st.subheader("Cross Model")

target_models = [
    x for x in model_names
    if x != selected_model
]

if not target_models:

    st.warning(
        "At least two models are required."
    )

else:

    target_model = st.selectbox(
        "Target Model",
        target_models
    )

    second_model = load_model(
        target_model
    )

    second_df = second_model["data"]

    if not isinstance(
        second_df,
        pd.DataFrame
    ):
        second_df = pd.DataFrame(
            second_df
        )

    common_cols = list(
        set(df.columns)
        &
        set(second_df.columns)
    )

    if common_cols:

        join_col = st.selectbox(
            "Join Column",
            common_cols
        )

        if st.button(
            "Run Cross Model"
        ):

            merged = pd.merge(
                df,
                second_df,
                on=join_col,
                how="left"
            )

            st.dataframe(
                merged,
                use_container_width=True
            )

            save_planning(
                "Cross_Model",
                {
                    "type": "Cross Model",
                    "data": merged.to_dict("records")
                }
            )

            st.success(
                "Cross Model Saved"
            )

    else:
        st.error(
            "No common columns found."
        )
```

# =====================================================

# VERSION MANAGEMENT

# =====================================================

elif planning_action == "Version Management":

```
st.subheader("Version Copy")

source_version = st.text_input(
    "Source Version",
    "Actual"
)

target_version = st.text_input(
    "Target Version",
    "Budget"
)

version_measure = st.selectbox(
    "Measure",
    measures
)

increase_pct = st.number_input(
    "Increase %",
    value=5.0
)

if st.button("Create Version"):

    version_df = df.copy()

    version_df["Version"] = (
        target_version
    )

    version_df[version_measure] = (
        version_df[version_measure]
        * (
            1
            + increase_pct / 100
        )
    ).round(2)

    st.dataframe(
        version_df,
        use_container_width=True
    )

    save_planning(
        target_version,
        {
            "type": "Version",
            "data": version_df.to_dict("records")
        }
    )

    st.success(
        "Version Saved"
    )
```

# =====================================================

# PLANNING GRID

# =====================================================

elif planning_action == "Planning Grid":

```
st.subheader(
    "Editable Planning Grid"
)

edited_df = st.data_editor(
    df,
    use_container_width=True,
    num_rows="dynamic"
)

if st.button(
    "Save Planning Grid"
):

    save_planning(
        "Planning_Grid",
        {
            "type": "Planning Grid",
            "data": edited_df.to_dict(
                "records"
            )
        }
    )

    st.success(
        "Planning Grid Saved"
    )
```

# =====================================================

# PLANNING REPOSITORY

# =====================================================

elif planning_action == "Planning Repository":

```
st.subheader(
    "Saved Planning Objects"
)

planning_objects = (
    get_planning()
)

if planning_objects:

    st.dataframe(
        pd.DataFrame(
            {
                "Planning Objects":
                planning_objects
            }
        ),
        use_container_width=True
    )

else:
    st.info(
        "No Planning Objects Found"
    )
```
