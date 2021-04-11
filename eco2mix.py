import pandas
import json

pandas.set_option('max_columns', None)
df = pandas.read_csv('data/eco2mix_min.csv', sep=';')

# keep only the dates and the CO2 emission rate
df.drop(df.columns.difference(['Date', 'Taux de CO2 (g/kWh)']), 1, inplace=True)

# drop all rows with NaN values
df.dropna(subset=['Taux de CO2 (g/kWh)'], inplace=True)

# convert string to date time format
df['Date'] = pandas.to_datetime(df['Date'], format='%Y-%m-%d')

# group by year-month and add sum, mean, max and min columns
s2 = df.groupby([df['Date'].dt.year, df['Date'].dt.month])['Taux de CO2 (g/kWh)'].agg(['sum', 'mean', 'max', 'min'])

# group by year
s3 = df.groupby([df['Date'].dt.year])['Taux de CO2 (g/kWh)'].agg(['sum', 'mean', 'max', 'min'])

# Convert to json
emissions = json.loads(s2.to_json(orient='index'))
yearly_emissions = json.loads(s3.to_json(orient='index'))
