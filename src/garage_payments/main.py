from banks.sber.read_payments import payments
from garages.garages import garages
from utils.utils import next_payment_datetime
from datetime import datetime, timedelta

import pandas as pd

if __name__ == "__main__":
    current_datetime = datetime.now()
    joined_table = garages.merge(payments, how="left", on="amount")

    # Creation payment_datetime column
    joined_table["payment_datetime"] = next_payment_datetime(
        joined_table, current_datetime, offset=1
    )

    # Creation delta columns
    joined_table["previous_payment_datetime"] = next_payment_datetime(
        joined_table, current_datetime, offset=0
    )

    joined_table["delta"] = joined_table["payment_datetime"] - joined_table[
        "last_payment_datetime"
    ].dt.tz_localize(None)

    # Creation status column
    joined_table.loc[
        (
            joined_table["delta"]
            > (
                joined_table["payment_datetime"]
                - next_payment_datetime(joined_table, current_datetime, offset=0)
                + timedelta(days=3)
            )
        )
        | (joined_table["last_payment_datetime"].isna()),
        "payment_status",
    ] = "Просрочен"

    joined_table.loc[
        joined_table["delta"]
        < (
            joined_table["payment_datetime"]
            - joined_table["previous_payment_datetime"]
        ),
        "payment_status",
    ] = "Срок не подошел"

    joined_table.loc[
        (
            joined_table["payment_datetime"].dt.date
            == joined_table["last_payment_datetime"].dt.date
        )
        | (
            next_payment_datetime(joined_table, current_datetime, offset=0).dt.date
            == joined_table["last_payment_datetime"].dt.date
        ),
        "payment_status",
    ] = "Получен"

    pd.set_option("display.max_columns", None)

    print(joined_table)
