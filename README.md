# Capital Gains and Losses Calculator
Given a list of transactions, calculates the total cost basis, proceeds, and short/long-term gains/losses using the FIFO (first in, first out) method.
## Instructions
### 1. Pre-setup
Install Python on your computer if it is not there already: https://wiki.python.org/moin/BeginnersGuide/Download

Download and extract this folder somewhere on your computer.

Combine all of your transactions into one CSV file. They all need to be in the same format, but do not need to be sorted by date. Put the CSV file in the same folder as the "tax_code.py" file.
### 2. Program setup
Open "tax_code.py" with a text editor and change the value to the right of `CSV_FILE = ` to the name of your CSV file.

If necessary, change the other values for the `CSV_` variables to match the format that your CSV is in. For example, the "UTC Timestamp" header might be called "Time" or something in your CSV. It does not matter what order the headers are in (e.g. timestamp can be first, last, or in the middle), but the headers need to match your entries, and they all need to be consistent.

By default, the program is configured to use SoFi's transaction format, which looks like this:

**UTC Timestamp,Transaction Type,Asset,Quantity,Price,Total**
### 3. Run the program
Run the "tax_code.py" script with the command-line interface (`python tax_code.py`) or however you prefer to run Python programs. The output will look like this:

```
Processing CSV

--- Asset: COIN1 ---
Summary:
Total amount bought: 300.0
Total amount sold: 300.0
Successfully processed all 1 sales
Summary of gains:
{'Total cost basis': 3000.0, 'Total proceeds': 7500.0, 'Total short-term gain/loss': 4500.0, 'Total long-term gain/loss': 0}

--- Asset: COIN2 ---
Summary:
Total amount bought: 300.0
Total amount sold: 200.0
Successfully processed all 2 sales
Summary of gains:
{'Total cost basis': 20000.0, 'Total proceeds': 5000.0, 'Total short-term gain/loss': -8000.0, 'Total long-term gain/loss': -7000.0}
```
### 4. Do your taxes without stress! ;)
## Disclaimer
Use this program at your own risk: I am not a tax professional and am not responsible for any inaccuracies in your tax return that may be caused by using this program. Please notify me if you find any mistakes with these calculations, but it is your responsibility to double check the math and ensure the correctness of your tax return.
