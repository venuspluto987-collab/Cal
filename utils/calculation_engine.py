import pandas as pd
import numpy as np


def apply_calculation(
    df,
    calc_type,
    measure,
    new_column
):

    try:

        if calc_type == "Running Total":

            df[new_column] = (
                df[measure]
                .cumsum()
            )

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

        elif calc_type == "Min":

            df[new_column] = (
                df[measure].min()
            )

        elif calc_type == "Max":

            df[new_column] = (
                df[measure].max()
            )

        elif calc_type == "Average":

            df[new_column] = (
                df[measure].mean()
            )

        elif calc_type == "Variance":

            df[new_column] = (
                df[measure]
                .var()
            )

        elif calc_type == "Standard Deviation":

            df[new_column] = (
                df[measure]
                .std()
            )

        return df

    except Exception:
        return df


def custom_formula(
    df,
    formula,
    new_column
):

    try:

        df[new_column] = df.eval(
            formula
        )

    except Exception:
        pass

    return df
