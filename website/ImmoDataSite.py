import streamlit as st
import pandas as pd
import glob
import pydeck as pdk
import numpy as np
import plotly.express as px

#TODO
#count groupby szerint(hány darab hirdetés van 1-1 fajtából), szórás, filter táblára/mapre, szépítés, plusz adatok behúzása (zöld terület, bűnözési adatok), dinamikus plot amin a kerületek
#közötti összehasonlítás megtekinthető?
#dinamikus számítások (pl felh. kiválaszthatja h medián helyett countot akar látni)
#opcionális: ne rerunolja a kódot minden filter változtatásnál

st.title("Rental situation in Vienna")
path = "F:/ImmoData/transformed"
csv_files = glob.glob(path + "/*.csv")
df_list = (pd.read_csv(file) for file in csv_files)
data = pd.concat(df_list, ignore_index=True)

def round_numbers(df):
    tmp = df.select_dtypes(include=[np.number])
    df.loc[:, tmp.columns] = np.round(tmp,3) 

def agg_df_drop_unused_cols(df,group_by_cols, drop_cols, agg_type):
    grouped_data = df.groupby(group_by_cols, as_index=False).agg(agg_type)
    grouped_data.drop(drop_cols,inplace=True,axis=1)
    return grouped_data


map_df = agg_df_drop_unused_cols(data,['District'],['ID','Time'],np.nanmedian)

table_df = data.groupby(['District','Property_type'], as_index=False).agg(Nr_of_occurences=('ID','count'),Avg_apt_size = ('Apt_size','median'),Avg_nr_of_rooms=('Nr_of_rooms','median'),
                                                                          Avg_nr_of_bathrooms = ('Nr_of_bathrooms','median'),Avg_cold_price=('Cold_price','median'),
                                                                          Avg_cold_price_per_sqm=('Cold_price_per_sqm','median'),Avg_deposit=('Deposit','median'))


st.pydeck_chart(pdk.Deck(
    map_style=None,
    initial_view_state=pdk.ViewState(
        latitude= 48.22680787756701,
        longitude= 16.37895427875075,
        zoom=10
    ),
    layers=pdk.Layer(
    "ScatterplotLayer",
    map_df,
    pickable=True,
    opacity=0.8,
    stroked=True,
    filled=True,
    radius_scale=25,
    radius_min_pixels=1,
    radius_max_pixels=100,
    line_width_min_pixels=1,
    get_position='[longitude,latitude]',
    get_radius='Cold_price_per_sqm',
    get_fill_color=[255, 140, 0],
    get_line_color=[0, 0, 0],),
    tooltip={"text": "{District}\nCold price per squaremeter: {Cold_price_per_sqm}\nNumber of rooms: {Nr_of_rooms}"}
    )
)
default_columns = table_df[['District', 'Property_type']]

chooseable = range(2,len(table_df.columns))
options = table_df.columns[chooseable]

selected_options = st.multiselect(label='Choose filters for table:',options=options)
selected_columns = table_df[selected_options]
filtered_table_df = default_columns.join(selected_columns)

st.dataframe(filtered_table_df, use_container_width=True, hide_index=True)
print(table_df)