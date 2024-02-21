"""
Written by Nicolas Binford, February 2024

Use at your own risk! It is your responsibility to double check the math and
ensure the correctness of your tax return.
(If it makes you feel better, if the IRS comes after you because of this
program, that means they will probably come after me too)

"""

"""
Configure your CSV here
"""
CSV_FILE = "trades_mini.csv"
CSV_HEADER_ASSET_NAME = "Asset"
CSV_HEADER_TRANSACTION_TYPE = "Transaction Type"
CSV_HEADER_QUANTITY = "Quantity"
CSV_HEADER_PRICE = "Price"
CSV_HEADER_TRANSACTION_TIMESTAMP = "UTC Timestamp"
CSV_VALUE_BUY = "BUY"
CSV_VALUE_BONUS = "BONUS"
CSV_VALUE_SALE = "SELL"


from csv import DictReader
from datetime import datetime, timedelta
from operator import itemgetter


def get_gains_losses_for_asset(buy_list, sell_list):
    sell_index = 0
    buy_index = 0
    num_sells = len(sell_list)
    num_buys = len(buy_list)

    current_sell = sell_list[sell_index]
    current_buy = buy_list[buy_index]
    sell_chunk_amnt = float(current_sell[1])
    buy_chunk_amnt = float(current_buy[1])

    sell_remainder = 0
    buy_remainder = 0

    raw_gainz = []

    while sell_index < num_sells:
        current_sell_price = float(current_sell[2])
        current_buy_price = float(current_buy[2])
        price_diff = current_sell_price - current_buy_price
        time_diff = current_sell[3] - current_buy[3]

        # A dict with details about each sale
        sale_details_dict = {}
        cost_basis = sell_chunk_amnt * current_buy_price
        proceeds = sell_chunk_amnt * current_sell_price
        sale_details_dict["Cost basis"] = cost_basis
        sale_details_dict["Proceeds"] = proceeds
        sale_details_dict["Time difference"] = time_diff

        # Case 1: Current "buy chunk" spans > 1 "sale chunks"
        if sell_chunk_amnt < buy_chunk_amnt:
            gain_loss_amnt = sell_chunk_amnt * price_diff
            sale_details_dict["Sale amount"] = sell_chunk_amnt
            sale_details_dict["Gain/loss"] = gain_loss_amnt
            raw_gainz.append(sale_details_dict)

            buy_remainder = buy_chunk_amnt - sell_chunk_amnt
            sell_index += 1
            if sell_index == num_sells:
                print(f"Successfully processed all {num_sells} sales")
                break
            else:
                current_sell = sell_list[sell_index]
                sell_chunk_amnt = float(current_sell[1])
                buy_chunk_amnt = buy_remainder

        # Case 2: Current "sale chunk" and "buy chunk" are the same amount
        elif sell_chunk_amnt == buy_chunk_amnt:
            gain_loss_amnt = sell_chunk_amnt * price_diff
            sale_details_dict["Sale amount"] = sell_chunk_amnt
            sale_details_dict["Gain/loss"] = gain_loss_amnt
            raw_gainz.append(sale_details_dict)

            buy_remainder = buy_chunk_amnt - sell_chunk_amnt
            sell_index += 1
            buy_index += 1
            if sell_index == num_sells:
                print(f"Successfully processed all {num_sells} sales")
                break
            elif buy_index == num_buys:
                print(f"Error: more assets sold than bought - your CSV may be missing transactions")
                break
            else:
                current_sell = sell_list[sell_index]
                current_buy = buy_list[buy_index]
                sell_chunk_amnt = float(current_sell[1])
                buy_chunk_amnt = float(current_buy[1])

        # Case 3: Current "sale chunk" spans > 1 "buy chunks"
        else:
            # Math trick (?): use the buy chunk amount for the sale amount
            cost_basis = buy_chunk_amnt * current_buy_price
            proceeds = buy_chunk_amnt * current_sell_price
            gain_loss_amnt = buy_chunk_amnt * price_diff
            sale_details_dict["Cost basis"] = cost_basis
            sale_details_dict["Proceeds"] = proceeds
            sale_details_dict["Sale amount"] = buy_chunk_amnt
            sale_details_dict["Gain/loss"] = gain_loss_amnt
            raw_gainz.append(sale_details_dict)

            sell_remainder = sell_chunk_amnt - buy_chunk_amnt
            buy_index += 1
            if buy_index == num_buys:
                print(f"Error: more assets sold than bought - your CSV may be missing transactions")
                break
            else:
                current_buy = buy_list[buy_index]
                buy_chunk_amnt = float(current_buy[1])
                sell_chunk_amnt = sell_remainder

    gainz_summary = {}
    gainz_summary["Total cost basis"] = 0
    gainz_summary["Total proceeds"] = 0
    gainz_summary["Total short-term gain/loss"] = 0
    gainz_summary["Total long-term gain/loss"] = 0
    for gl in raw_gainz:
        gainz_summary["Total cost basis"] += gl["Cost basis"]
        gainz_summary["Total proceeds"] += gl["Proceeds"]
        if gl["Time difference"] > timedelta(days=365):
            gainz_summary["Total long-term gain/loss"] += gl["Gain/loss"]
        else:
            gainz_summary["Total short-term gain/loss"] += gl["Gain/loss"]

    print(f"Summary of gains:\n{gainz_summary}")


def main():
    # Read the CSV and put it in a list sorted by date
    print("Processing CSV")
    temp_list = []
    with open(CSV_FILE, "r") as f:
        rows = DictReader(f)
        for row in rows:
            ts = row[CSV_HEADER_TRANSACTION_TIMESTAMP]
            tst = datetime.fromisoformat(ts)
            row[CSV_HEADER_TRANSACTION_TIMESTAMP] = tst
            temp_list.append(row)
    sorted_by_date = sorted(temp_list, key=itemgetter(CSV_HEADER_TRANSACTION_TIMESTAMP))

    # Dict with each asset as the key, and the buys/sells as the value
    csv_transaction_dict = {}

    for row in sorted_by_date:
        asset = row[CSV_HEADER_ASSET_NAME]
        if asset not in csv_transaction_dict:
            csv_transaction_dict[asset] = {"buys": [], "sells": []}
        t_type = row[CSV_HEADER_TRANSACTION_TYPE]
        amount = row[CSV_HEADER_QUANTITY]
        price = row[CSV_HEADER_PRICE]
        t_time = row[CSV_HEADER_TRANSACTION_TIMESTAMP]
        if t_type == CSV_VALUE_BUY or t_type == CSV_VALUE_BONUS:
            tutu = ("BUY", amount, price, t_time)
            csv_transaction_dict[asset]["buys"].append(tutu)
        elif t_type == CSV_VALUE_SALE:
            tutu = ("SELL", amount, price, t_time)
            csv_transaction_dict[asset]["sells"].append(tutu)
        else:
            print(f"Invalid row found in CSV:\n{row}")

    for asset in csv_transaction_dict:
        print(f"\n--- Asset: {asset} ---")
        print("Summary:")
        
        buys = csv_transaction_dict[asset]["buys"]
        sells = csv_transaction_dict[asset]["sells"]

        buy_total = 0.0
        sell_total = 0.0

        # Calculate total amount bought and sold
        for b in buys:
            buy_total += float(b[1])
        for s in sells:
            sell_total += float(s[1])

        print(f"Total bought: {buy_total}")
        print(f"Total sold: {sell_total}")
        print("Gains and losses:")
        get_gains_losses_for_asset(buys, sells)


if __name__ == "__main__":
    main()
