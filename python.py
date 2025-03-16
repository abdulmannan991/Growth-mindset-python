import streamlit as st
import pandas as pd
from io import BytesIO

# Page Configuration
st.set_page_config(page_title="📂 File Converter", layout="wide", page_icon="🔄")

# Sidebar for file upload
st.sidebar.title("🔼 Upload Files")
files = st.sidebar.file_uploader("Upload CSV or Excel files", type=["csv", "xlsx"], accept_multiple_files=True)

# Main Title
st.title("📂 File Converter")
st.write("Easily convert CSV or Excel files with a **clean UI experience**! 🚀")

# Initialize session state for data storage
if "dataframes" not in st.session_state:
    st.session_state.dataframes = {}

# Process Uploaded Files
if files:
    for file in files:
        ext = file.name.split(".")[-1]
        
        # Load data only if it's not already in session state
        if file.name not in st.session_state.dataframes:
            df = pd.read_csv(file) if ext == "csv" else pd.read_excel(file)
            st.session_state.dataframes[file.name] = df  # Store in session state

        df = st.session_state.dataframes[file.name]  # Retrieve from session state

        with st.expander(f"📄 Preview - {file.name}", expanded=True):
            st.dataframe(df.head(10))

        col1, col2 = st.columns(2)

        with col1:
            if st.checkbox(f"🗑 Remove Duplicates - {file.name}", key=f"remove_{file.name}"):
                df = df.drop_duplicates()
                st.session_state.dataframes[file.name] = df  # Update session state
                st.success("✅ Duplicates removed successfully!")
                st.dataframe(df.head(5))

        with col2:
            if st.checkbox(f"🛠 Fill Missing Values - {file.name}", key=f"fill_{file.name}"):
                df.fillna(df.select_dtypes(include=["number"]).mean(), inplace=True)
                st.session_state.dataframes[file.name] = df  # Update session state
                st.success("✅ Missing values filled with mean.")
                st.dataframe(df.head(5))

        # Column Selection
        selected_columns = st.multiselect(f"🔍 Select Columns to Display - {file.name}", df.columns, default=df.columns)
        df = df[selected_columns]
        st.session_state.dataframes[file.name] = df  # Update session state
        st.dataframe(df.head(5))

        # Show Chart Option
        if st.checkbox(f"📊 Show Chart - {file.name}") and not df.select_dtypes(include="number").empty:
            st.bar_chart(df.select_dtypes(include="number").iloc[:, :2])

        # Format Choice
        st.divider()
        format_choice = st.radio(f"🔄 Convert {file.name} to:", ["CSV", "Excel"], key=file.name, horizontal=True)

        # Download Button
        col1, col2 = st.columns([3, 1])
        with col1:
            if st.button(f"📥 Download {file.name} as {format_choice}", use_container_width=True):
                with st.spinner("⚡ Processing... Please wait!"):
                    output = BytesIO()

                    if format_choice == "CSV":
                        df.to_csv(output, index=False)
                        mime_type = "text/csv"
                        new_name = file.name.replace(ext, "csv")

                    else:  # Excel
                        df.to_excel(output, index=False, engine='openpyxl')
                        mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        new_name = file.name.replace(ext, "xlsx")
# .
                    output.seek(0)
                    st.download_button("⬇️ Download File", file_name=new_name, data=output, mime=mime_type, use_container_width=True)
                    st.success("🎉 File is ready for download!")
