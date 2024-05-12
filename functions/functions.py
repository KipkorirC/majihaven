import pandas as pd
def load_and_process_data(excel_file):
    RAIN_DATA = pd.read_excel(excel_file, engine="openpyxl")
    RAIN_DATA = RAIN_DATA[1:]
    RAIN_DATA.rename(columns={'Precipitation (CHIRPS)': 'Date'}, inplace=True)
    RAIN_DATA.rename(columns={'Unnamed: 1': 'Rain in mm'}, inplace=True)
    return RAIN_DATA

