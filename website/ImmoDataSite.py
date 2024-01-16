import streamlit as st
import pandas as pd
import glob

st.title("Rental situation in Vienna")
path = "F:/ImmoData/exports"
csv_files = glob.glob(path + "/*.csv")
df_list = (pd.read_csv(file) for file in csv_files)
data = pd.concat(df_list, ignore_index=True)

st.dataframe(data, use_container_width=True)
st.map(data)
