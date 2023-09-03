import json
import os
import pandas as pd
import requests as r

EMAIL = "varunrao1995@gmail.com"
KEY = os.getenv("AQS_KEY")

STATE = "06"  # California
COUNTIES = ["075", "085", "081"]  # SF, Santa Clara, San Mateo
SITES = ["0005", "0006", "1001"]  # San Francisco, San Jose - Knox Avenue, Redwood City


begin_date = "20220101"
end_date = "20221231"
url_sample_data_site = f"https://aqs.epa.gov/data/api/sampleData/bySite?email={EMAIL}&key={KEY}&param=88101&bdate={begin_date}&edate={end_date}&state={STATE}"

for county, site in zip(COUNTIES, SITES):
    print(f"Processing {county} and {site}")
    resp = r.get(url_sample_data_site + f"&county={county}&site={site}")
    with open(f"data/pm2.5_{county}_{site}_2022.json", "w") as out_file:
        json.dump(resp.json(), out_file)

df = pd.DataFrame()
for county, site in zip(COUNTIES, SITES):
    with open(f"data/pm2.5_{county}_{site}_2022.json") as infile:
        df = pd.concat([df, pd.DataFrame(json.load(infile)["Data"])])


COLS_TO_INCLUDE = [
    "county",
    "date_local",
    "time_local",
    "sample_measurement",
    "units_of_measure",
    "detection_limit",
    "uncertainty",
    "method",
]
df[COLS_TO_INCLUDE].to_csv("data/all_samples.csv")

# def process_data():