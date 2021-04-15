import pandas
import json

df = pandas.read_csv(
    'data/eco2mix_min.csv',
    sep=';',
    usecols=['Date', 'Taux de CO2 (g/kWh)'],
    dtype={'Taux de CO2 (g/kWh)': 'float16'}
)

# drop all rows with NaN values
df.dropna(subset=['Taux de CO2 (g/kWh)'], inplace=True)

# convert string to date time format
df['Date'] = pandas.to_datetime(df['Date'], format='%Y-%m-%d')

# group by year-month and add sum, mean, max and min columns
# s2 = df.groupby([df['Date'].dt.year, df['Date'].dt.month])['Taux de CO2 (g/kWh)'].agg(['sum', 'mean', 'max', 'min'])

# group by year
# s3 = df.groupby([df['Date'].dt.year])['Taux de CO2 (g/kWh)'].agg(['sum', 'mean', 'max', 'min'])

# Group by year-month and add sum, mean, max and min columns and convert to json
emissions = json.loads(
    df.groupby([
        df['Date'].dt.year,
        df['Date'].dt.month
    ])['Taux de CO2 (g/kWh)'].agg(['sum', 'mean', 'max', 'min']).to_json(orient='index')
)

# group by year and convert to JSON
yearly_emissions = json.loads(
    df.groupby([
        df['Date'].dt.year
    ])['Taux de CO2 (g/kWh)'].agg(['sum', 'mean', 'max', 'min']).to_json(orient='index')
)
