import pandas as pd
import math

class DividendPayment():

    def __init__(self, source, amount, date, account_currency):
        self.source = source
        self.amount = amount
        self.date = date
        self.account_currency = account_currency

    def __str__(self):
        return "{} payed {} {} on {}".format(self.source, self.amount, self.account_currency, self.date)

class DeGiroDataHandler():

    def __init__(self, csv_file, account_currency):
        self.df = pd.read_csv(csv_file)
        self.account_currency = account_currency

    def prepare_data(self):
        for index, row in self.df.iterrows():
            if "Dividend" in row["Description"]:
                if row["Date"] == self.df.loc[index + 1]["Date"]:
                    print(row["Date"])

    def get_dividends(self):
        dividend_payments = []
        for index, row in self.df.iterrows():
            if row["Description"] == "Dividend":
                if self.df.loc[index + 1]["Description"] == "Dividend Tax":
                    amount = row[8] + self.df.loc[index + 1][8]
                else:
                    amount = row[8]

                found_match = False
                for i in range(1, index):
                    if self.df.loc[index - i]["Description"] == "FX Debit":
                        if abs(self.df.loc[index - i][8] + amount) < 0.02:
                            amount = self.df.loc[index - i - 1][8]
                            found_match = True

                if found_match == True:
                    dividend_payments.append(DividendPayment(row["Product"], amount, row["Date"], self.account_currency))
                else:
                    print("Wasn't able to find payment for {}".format(row["Product"]))

        for payment in dividend_payments:
            print(payment)