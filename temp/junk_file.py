import pandas as pd


df = pd.read_csv(r'D:\Git\Home-project\data_collection\doge_5m_yearly_data.csv')

print(df.head(), df.tail(), sep='\n')

results = pd.DataFrame({'pair':['USDT','USDC'], 'P-value':[1.3,1.1]})
print(pd.DataFrame(results).sort_values('P-value'))
print(results.sort_values('P-value'))