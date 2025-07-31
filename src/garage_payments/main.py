from banks.sber.read_payments import payments
from garages.garages import garages
from utils.utils import next_payment_datetime
from datetime import datetime

import pandas as pd

if __name__ == "__main__":
    # current_datetime = datetime.strptime("11.03.2025", "%d.%m.%Y")
    current_datetime = datetime.now()
    joined_table = garages.merge(payments, how="left", on="amount")
    joined_table["payment_datetime"] = next_payment_datetime(joined_table, current_datetime)

    print(joined_table)
