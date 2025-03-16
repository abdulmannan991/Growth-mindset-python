import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="File Converter", layout="wide")
st.title("📂 File Converter")
st.write("Upload CSV or Excel files and convert them easily.")

# Upload multiple files
files = st.file_uploader("Upload CSV or Excel files", type=["csv", "xlsx"], accept_multiple_files=True)

if files:
    for file in files:
        ext = file.name.split(".")[-1]
        df = pd.read_csv(file) if ext == "csv" else pd.read_excel(file)

        st.subheader(f"📄 Preview of {file.name}")
        st.dataframe(df.head())

        # Remove Duplicates
        if st.checkbox(f"🗑 Remove Duplicates - {file.name}"):
            df = df.drop_duplicates()
            st.success("✅ Duplicates removed successfully! ")
            st.dataframe(df.head())

        # Fill Missing Values
        if st.checkbox(f"🛠 Fill Missing Values - {file.name}"):
            df.fillna(df.select_dtypes(include=["number"]).mean(), inplace=True)
            st.success("✅ Missing values filled with mean.")
            st.dataframe(df.head())

        # Select Columns
        selected_columns = st.multiselect(f"🔍 Select Columns to Display - {file.name}", df.columns, default=df.columns)
        df = df[selected_columns]
        st.dataframe(df.head())

        # Show Chart
        if st.checkbox(f"📊 Show Chart - {file.name}") and not df.select_dtypes(include="number").empty:
            st.bar_chart(df.select_dtypes(include="number").iloc[:, :2])

        # File Format Selection
        format_choice = st.radio(f"🔄 Convert {file.name} to:", ["CSV", "Excel"], key=file.name)

        # Download Button
        if st.button(f"📥 Download {file.name} as {format_choice}"):
            with st.spinner("Processing... ⏳"):
                output = BytesIO()

                if format_choice == "CSV":
                    df.to_csv(output, index=False)
                    mime_type = "text/csv"
                    new_name = file.name.replace(ext, "csv")

                else:  # Excel
                    df.to_excel(output, index=False, engine='openpyxl')
                    mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    new_name = file.name.replace(ext, "xlsx")

                output.seek(0)
                st.download_button("⬇️ Download File", file_name=new_name, data=output, mime=mime_type)

        st.success("✅ Processing Complete!")

