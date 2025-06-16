import pandas as pd

def save_to_excel(df, filename, sheet_name, index=False):
    with pd.ExcelWriter(filename, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name=sheet_name, index=index)
