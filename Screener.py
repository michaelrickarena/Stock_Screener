import yahoo_fin.stock_info as si
import pandas as pd
from yahoo_fin.stock_info import *
import csv
import time

#collects all tickers from the s&p 500 and the nasdaq
snp_tickers = si.tickers_sp500()

nasdaq_tickers = si.tickers_nasdaq()


df = pd.read_csv('C:/Users/Michael Arena/Desktop/stocks_info.csv')

matrix2 = df[df.columns[0]].as_matrix()
list2 = matrix2.tolist()



#combines both lists and removes duplicates
all_stocks = snp_tickers + list(set(nasdaq_tickers) - set(snp_tickers))

unused_stocks = list(set(all_stocks) - set(list2))



# test = get_quote_table(all_stocks[find]) # check json data in `get_quote_table
time.sleep(10)

n = 0 #initilize n
#loop through stock tickers

#save headers down
headers = {'Ticker': 'random', 'Stock Price': 'stock_price', 'Market Capitilization': 'value_int', 'Target Price': 'target_price', 'Earnings Report Date': 'earnings_date', '52 Week Range': 'year_range', 'Beta': 'Beta'}
keys = headers.keys()
with open('stocks_List.csv', 'w', newline='')  as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()

ticker_issues = []
for stock in unused_stocks:
	n += 1
	time.sleep(0.2)

	print(f"\npulling {stock} with index {n}")

	try:
		mkt_cap_str = get_quote_table(stock)['Market Cap']
		target_price = get_quote_table(stock)['1y Target Est']
		earnings_date =  get_quote_table(stock)['Earnings Date']
		stock_price = get_quote_table(stock)['Previous Close']
		year_range = get_quote_table(stock)['52 Week Range']
		Beta = get_quote_table(stock)['Beta (5Y Monthly)']
		value_int = float(mkt_cap_str[:-1])
	except Exception as e:
		print(f'\n{type(e)} Error at index {n}')

	try:
		if mkt_cap_str.endswith('T'):
			value_int = int(value_int*1000000000000)
		elif mkt_cap_str.endswith('B'):
			value_int = int(value_int*1000000000)
		elif mkt_cap_str.endswith('M'):
			value_int = int(value_int*1000000)
		elif mkt_cap_str == 'nan':
			value_int = int(0) 
	except Exception as m:
		value_int = 0
		print(f"\n{type(m)} Error with market Capitilization of {stock}")

	
	try:
		stock_info = {'Ticker': stock, 'Stock Price': stock_price, 'Market Capitilization': value_int, 'Target Price': target_price, 'Earnings Report Date': earnings_date, '52 Week Range': year_range, 'Beta': Beta}	
	except Exception as l:
			ticker_issues.append(stock)
			print(type(l))


	with open('stocks_info.csv', 'a', newline='')  as output_file:
		dict_writer = csv.DictWriter(output_file, keys)
		dict_writer.writerow(stock_info)

print(f'Errors occured with incorrect dictionary values of companies {ticker_issues}')
