from banks.sber.read_payments import payments
from garages.garages import garages
from utils.utils import next_payment_datetime
from datetime import datetime

if __name__ == "__main__":
    #current_datetime = datetime.strptime("01.03.2025", "%d.%m.%Y")
    current_datetime = datetime.now()
    joined_table = garages.merge(payments, how="left", on="amount")
    # joined_table["status"] = joined_table.apply(next_payment_datetime, current_datetime=current_datetime, axis=1)

    print(joined_table)