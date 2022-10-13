import pandas as pd
import requests
from io import BytesIO


def load_data(dataset_directory, date_column = 'Date'):
    data = pd.read_csv(dataset_directory)
    titlecase = lambda x: str(x).title()
    data.rename(titlecase, axis='columns', inplace=True)
    if date_column in list(data.columns):
        data[date_column] = pd.to_datetime(data[date_column])
    return data

def convert_to_csv(df):
    return df.to_csv()

def read_image_url(url):
    response = requests.get(url)
    return BytesIO(response.content)