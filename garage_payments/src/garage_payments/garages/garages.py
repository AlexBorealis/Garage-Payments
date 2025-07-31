import os

import pandas as pd
from dotenv import load_dotenv

load_dotenv()

# Reading data
garages = pd.read_excel(
    os.path.join(os.getenv("HOME_DIR"), "data/arenda.xlsx"), parse_dates=False
)

# Rename columns
garages.columns = ["storage_num", "amount", "initial_datetime"]

# Transforms column
garages["amount"] = garages["amount"].astype(float)
garages["initial_datetime"] = pd.to_datetime(
    garages["initial_datetime"],
    format="%d.%m.%Y %H:%M",
)
