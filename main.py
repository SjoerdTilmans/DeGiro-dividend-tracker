import libs

data_handler = libs.DeGiroDataHandler(csv_file="Data/Account.csv", account_currency="GDP")
data_handler.prepare_data()
data_handler.get_dividends()