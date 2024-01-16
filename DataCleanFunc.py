import pandas as pd
import numpy as np
import glob
import re

path = "F:/ImmoData/exports"
csv_files = glob.glob(path + "/*.csv")
df_list = (pd.read_csv(file, keep_default_na=False) for file in csv_files)
data = pd.concat(df_list, ignore_index=True)


latitude = {
    "01. Bezirk": "48.20863297021143",
    "02. Bezirk": "48.203617523797035",
    "03. Bezirk": "48.1948390094276",
    "04. Bezirk": "48.192010613819185",
    "05. Bezirk": "48.18523170899121",
    "06. Bezirk": "48.19562419407982",
    "07. Bezirk": "48.202452041827584",
    "08. Bezirk": "48.21105529696667",
    "09. Bezirk": "48.22330833991927",
    "10. Bezirk": "48.15840188647597",
    "11. Bezirk": "48.16855381854869",
    "12. Bezirk": "48.17102614824478",
    "13. Bezirk": "48.17883446638657",
    "14. Bezirk": "48.19688797409259",
    "15. Bezirk": "48.19602367792661",
    "16. Bezirk": "48.211728210909065",
    "17. Bezirk": "48.227498014498735",
    "18. Bezirk": "48.2329620210308",
    "19. Bezirk": "48.24618199986359",
    "20. Bezirk": "48.236276510701444",
    "21. Bezirk": "48.27350702061701",
    "22. Bezirk": "48.23047911886208",
    "23. Bezirk": "48.142783280562675"
}


longitude = {
    "01. Bezirk": "16.369827617914403",
    "02. Bezirk": "16.41758029966762",
    "03. Bezirk": "16.395490948238557",
    "04. Bezirk": "16.37062974063771",
    "05. Bezirk": "16.35528728268473",
    "06. Bezirk": "16.35204364408176",
    "07. Bezirk": "16.347684138305205",
    "08. Bezirk": "16.347708894126995",
    "09. Bezirk": "16.35824921927842",
    "10. Bezirk": "16.383473540704",
    "11. Bezirk": "16.436076248895482",
    "12. Bezirk": "16.31961598017012",
    "13. Bezirk": "16.27746453086234",
    "14. Bezirk": "16.291003624545844",
    "15. Bezirk": "16.327250552750186",
    "16. Bezirk": "16.30949941429204",
    "17. Bezirk": "16.31006462326045",
    "18. Bezirk": "16.32807548343598",
    "19. Bezirk": "16.342753712273154",
    "20. Bezirk": "16.377594032273304",
    "21. Bezirk": "16.407138640775035",
    "22. Bezirk": "16.46567122425539",
    "23. Bezirk": "16.29925805592741"
}



data[["Apt_size", "Apt_size_unit"]] = data["Apt_size"].str.split(" ", expand=True)
data[["Cold_price", "Cold_price_unit"]] = data["Cold_price"].str.split(" ", expand=True)
data[["Cold_price_per_sqm", "Cold_price_per_sqm_unit"]] = data[
    "Cold_price_per_sqm"
].str.split(" ", expand=True)
data[["Warm_price", "Warm_price_unit"]] = data["Warm_price"].str.split(" ", expand=True)
data["Street"].replace(",", "", regex=True, inplace=True)
data["Apt_size"].replace(",", ".", regex=True, inplace=True)
data["Cold_price"].replace(",", ".", regex=True, inplace=True)
data["Cold_price_per_sqm"].replace(",", ".", regex=True, inplace=True)
data.fillna('NA')

data['Latitude'] = ''
data['Longitude'] = ''





for i in range(data.shape[0]):
    temp = re.findall(r'(.*?),',data['Region_and_country'][i])[1]

    lat = latitude[temp]
    longi = longitude[temp]

    

    

data = data[
    [
        "ID",
        "Property_type",
        "Street",
        "Region_and_country",
        "Apt_size",
        "Apt_size_unit",
        "Floor",
        "Move_in",
        "Nr_of_rooms",
        "Nr_of_bathrooms",
        "Cold_price",
        "Cold_price_unit",
        "Cold_price_per_sqm",
        "Cold_price_per_sqm_unit",
        "Warm_price",
        "Warm_price_unit",
        "Labels",
        "Pets_allowed",
        "Year_built",
        "Heating",
        "Heating_price",
        "Parking",
        "Deposit",
        "Status",
        "Desc",
        "URL",
        "Time",
        "Latitude",
        "Longitude"
    ]
]


data.to_csv("F:/ImmoData/transformed/test.csv", encoding="utf-8-sig", index=False)
print(data)