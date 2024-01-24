import streamlit as st
import pandas as pd
import glob
import pydeck as pdk
import numpy as np

st.title("Rental situation in Vienna")
path = "F:/ImmoData/transformed"
csv_files = glob.glob(path + "/*.csv")
df_list = (pd.read_csv(file) for file in csv_files)
data = pd.concat(df_list, ignore_index=True)

grouped_data = data.groupby(['District']).agg(np.nanmean)

print(grouped_data)
st.dataframe(grouped_data, use_container_width=True)
#st.map(grouped_data)
st.pydeck_chart(pdk.Deck(
    map_style=None,
    initial_view_state=pdk.ViewState(
        latitude= 48.22680787756701,
        longitude= 16.37895427875075,
        zoom=10
    ),
    layers=pdk.Layer(
    "ScatterplotLayer",
    grouped_data,
    pickable=True,
    opacity=0.8,
    stroked=True,
    filled=True,
    radius_scale=6,
    radius_min_pixels=1,
    radius_max_pixels=100,
    line_width_min_pixels=1,
    get_position='[longitude,latitude]',
    get_radius='Cold_price',
    get_fill_color=[255, 140, 0],
    get_line_color=[0, 0, 0],)
    )
)
