
import streamlit as st
import pandas as pd
from io import BytesIO
import openpyxl

st.set_page_config(page_title="file converter" ,layout="wide" )
st.title("File converter")
st.write("upload CSV or Excel files")

files = st.file_uploader("Upload CSV or Excel files", type=["csv","xlsx"], accept_multiple_files=True)

if files:
    for file in files:
        ext = file.name.split(".")[-1]
        df = pd.read_csv(file) if ext == "csv" else pd.read_excel(file)

        st.subheader(f"Preview of {file.name}")
        st.dataframe(df.head())

        if st.checkbox(f"Remove duplicates - {file.name}"):
            df = df.drop_duplicates()
            st.success("Duplicates removed successfully😊 ")
            st.dataframe(df.head())

        if st.checkbox(f"fill missing values - {file.name}"):
            df = df.fillna(df.select_dtypes(include=["number"]).mean(),inplace=True)
            st.success("Missing values filled with mean")
            st.datafram(df.head())

        selected_colums = st.multiselect(f"select colums to display - {file.name}",df.columns,default=df.columns)
        df = df[selected_colums]
        st.dataframe(df.head())

        if st.checkbox(f"Show chart - {file.name}")and not df.select_dtypes(include="number").empty:
            st.bar_chart(df.select_dtypes(include="number").iloc[:, :2])

        format_choise = st.radio(f"Convert {file.name} to: ", ["csv","Excel"],key=file.name)

        
        if st.button(f"Download {file.name} as {format_choise}"):
            output = BytesIO()
    
            if format_choise == "csv":
                df.to_csv(output, index=False)
                mine = "text/csv"
                new_name = file.name.replace(ext, "csv")

            else:
                df.to_excel(output, index=False, engine='openpyxl')
                mine = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                new_name = file.name.replace(ext, "xlsx")
            
            output.seek(0)
            st.download_button("download file",file_name=new_name, data=output, mime=mine)
    
        st.success("Processing Complete!")
