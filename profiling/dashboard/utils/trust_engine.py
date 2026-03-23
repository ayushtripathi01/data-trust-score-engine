import pandas as pd
from pandas import errors

def calculate_trust(df, sales_col, id_col, date_col):

    # -----------------------------
    # COMPLETENESS
    # -----------------------------
    missing_cells = df[[sales_col, id_col, date_col]].isnull().sum().sum()
    total_cells = len(df) * 3

    completeness = ((total_cells - missing_cells) / total_cells) * 100

    # -----------------------------
    # DATA TYPE FIX
    # -----------------------------
    df[sales_col] = pd.to_numeric(df[sales_col], errors='coerce')
    df[date_col] = pd.to_datetime(df[date_col], errors='coerce')

    # -----------------------------
    # ACCURACY
    # -----------------------------
    errors = 0

    # Safe numeric check
    errors += ((df[sales_col] < 0).fillna(False)).sum()

    # Missing ID
    errors += df[id_col].isnull().sum()

    # Safe date check
    valid_dates = df[date_col].notnull()
    errors += ((df.loc[valid_dates, date_col] > pd.Timestamp.today())).sum()

    accuracy = (1 - (errors / len(df))) * 100

    # -----------------------------
    # FINAL TRUST SCORE
    # -----------------------------
    trust = (completeness * 0.5) + (accuracy * 0.5)

    return round(completeness, 2), round(accuracy, 2), round(trust, 2)