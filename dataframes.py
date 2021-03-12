import pandas
import json

"""
Convoluted mess to clean, group and transform datasets.To be refactored.
"""

# Creation of a Pandas Dataframe from CSV file
cons_df, prod_df = pandas.read_csv('data/consumption2.csv', sep=';'), pandas.read_csv('data/energy.csv', sep=';')

# Replace non-ascii characters in column 'Region'
prod_df['Région'] = prod_df['Région'].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')
cons_df['Région'] = cons_df['Région'].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')

# Replace non-ascii characters in column titles
prod_df.rename(
    columns={
        'Année': 'annee',
        'Code INSEE région': 'codeInsee',
        'Région': 'region',
        'Production nucléaire (GWh)': 'Nucleaire',
        'Production thermique (GWh)': 'Thermique',
        'Production hydraulique (GWh)': 'Hydraulique',
        'Production éolienne (GWh)': 'Eolienne',
        'Production solaire (GWh)': 'Solaire',
        'Production bioénergies (GWh)': 'Bioenergies',
        'Géo-shape région': 'geoShape',
        'Géo-point région': 'geoPoint'
    }, inplace=True)
cons_df.rename(
    columns={
        'Année': 'annee',
        'Code INSEE région': 'codeInsee',
        'Consommation nette corrigée (GWh)': 'consoNette',
        'Région': 'region',
        'Géo-shape région': 'geoShape',
        'Géo-point région': 'geoPoint',
    }, inplace=True)

prod_df.drop(['geoShape', 'geoPoint'], axis=1, inplace=True)
cons_df.drop(['geoShape', 'geoPoint'], axis=1, inplace=True)
prod_df.set_index('region', inplace=True)
cons_df.set_index('region', inplace=True)

prod_year, cons_year = prod_df.groupby(['annee']), cons_df.groupby(['annee'])
years = {
    0: 2008, 1: 2009, 2: 2010,
    3: 2011, 4: 2012, 5: 2013,
    6: 2014, 7: 2015, 8: 2016,
    9: 2017, 10: 2018, 11: 2019,
}
year_list = list(years.values())

# Divide the dataframes into individual yearly_groups
yearly_prod_groups = [
    json.loads(prod_year.get_group(years[year]).to_json(orient='index', force_ascii=False))
    for year in years
]

yearly_cons_groups = [
    json.loads(cons_year.get_group(years[year]).to_json(orient='index', force_ascii=False))
    for year in years
]

cons_df_region = cons_df.groupby(['region', 'annee']).sum().reset_index()
cons_df_region.drop(['codeInsee'], axis=1, inplace=True)
regional_cons = cons_df_region.pivot(index='annee', columns='region').apply(
    lambda x: json.loads(x.to_json(orient='index'))
)

prod_df_regions = prod_df.groupby(['region', 'annee']).sum().reset_index()
prod_df_regions.drop(['codeInsee'], axis=1, inplace=True)
prod_df_regions['prodTotal'] = prod_df_regions.apply(
    lambda row: row.Nucleaire + row.Thermique + row.Hydraulique + row.Eolienne + row.Solaire + row.Bioenergies,
    axis=1
)
prod_df_regions.drop([
    'Nucleaire',
    'Thermique',
    'Hydraulique',
    'Eolienne',
    'Solaire',
    'Bioenergies',
], axis=1, inplace=True)
regional_prod = prod_df_regions.pivot(index='annee', columns='region').apply(
    lambda x: json.loads(x.to_json(orient='index'))
)

