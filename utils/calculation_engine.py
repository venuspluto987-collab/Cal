import pandas as pd
import numpy as np


def create_calculation(
    df,
    calc_type,
    measure,
    new_column
):

    if calc_type == "Running Total":

        df[new_column] = df[measure].cumsum()

    elif calc_type == "Moving Average":

        df[new_column] = (
            df[measure]
            .rolling(3)
            .mean()
        )

    elif calc_type == "Growth %":

        df[new_column] = (
            df[measure]
            .pct_change()
            * 100
        )

    elif calc_type == "Rank":

        df[new_column] = (
            df[measure]
            .rank(
                ascending=False
            )
        )

    elif calc_type == "Contribution %":

        total = df[measure].sum()

        df[new_column] = (
            df[measure]
            / total
        ) * 100

    return df
