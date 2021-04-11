from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dataframes import yearly_prod_groups, yearly_cons_groups, year_list, regional_cons, regional_prod
from eco2mix import yearly_emissions, emissions

app = FastAPI()

# Allow CORS
origins = [
    "*",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/production/{year}")
def get_yearly_prod_data(year: int):
    return yearly_prod_groups[year_list.index(year)]


@app.get("/api/consumption/{year}")
def get_yearly_cons_data(year: int):
    return yearly_cons_groups[year_list.index(year)]


@app.get("/api/consumption/historical/{region_id}")
def get_hist_cons_data(region_id: int):
    return regional_cons[region_id]


@app.get("/api/production/historical/{region_id}")
def get_hist_prod_data(region_id: int):
    return regional_prod[region_id]


@app.get("/api/emission")
def get_hist_emission():
    return emissions


@app.get("/api/emission/{year}")
def get_yearly_emission(year: str):
    return yearly_emissions[year]
