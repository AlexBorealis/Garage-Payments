import os

import pandas as pd
from dotenv import load_dotenv

from src.garage_payments.utils.utils import to_float, tz, get_number_column

load_dotenv()

# Reading data
payments = pd.read_excel(os.path.join(os.getenv("HOME_DIR"), "data/print2.xlsx"))

# Determine indexes
date_idx = get_number_column(payments, r"^дата операции")
time_idx = get_number_column(payments, r"^время|^\d{2}\:\d{2}")
category_idx = get_number_column(payments, r"^категория")
amount_idx = get_number_column(payments, r"^сумма")

date_idx = date_idx if date_idx is not None else 0
time_idx = time_idx if time_idx is not None else date_idx + 1
category_idx = category_idx if category_idx is not None else time_idx + 1
amount_idx = amount_idx if amount_idx is not None else category_idx + 1

# Filtered data
payments = payments.iloc[:, [date_idx, time_idx, category_idx, amount_idx]]

# Rename columns
payments.columns = ["date", "time", "category", "amount"]

# Transform columns
payments.date = payments.date.apply(
    lambda x: x.split()[0]
    if isinstance(x, str) and len(x.split()) > 0 and x.split()[0].count(".") == 2
    else None
)

payments["last_payment_datetime"] = tz(
    payments.date + " " + payments.time, old="Europe/Moscow", new="Asia/Novosibirsk"
)

payments["amount"] = to_float(payments["amount"], [(",", "."), (" ", ""), ("+", "")])

payments = payments.loc[payments.amount.notna(), ["last_payment_datetime", "amount"]]
