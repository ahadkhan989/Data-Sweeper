import streamlit as st
import pandas as pd
import os
from io import BytesIO


# Setup our App
st.set_page_config(page_title = "Data Sweeper", layout = "wide")
st.title("📁 Data Sweeper")
st.write("Transform Data, See Results: CSV & Excel Conversion with Cleaning & Visualization")

uploaded_files = st.file_uploader("Upload your files (CSV or Excel):", type = ["csv", "xlsx"], accept_multiple_files = True)

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()


        if file_ext == ".csv":
            df = pd.read_csv(file)  #df --> data frame and pd--> short form of pandas
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"unsupported file type: {file_ext}")
            continue
        

        #Display information about the file type
        st.write(f"**File Name:** {file.name}")
        st.write(f"**File Size:** {file.size/1024}")

        # Show 5 rows of our data frame "df"
        st.write("🔍 Preview the Head of the Dataframe")
        st.dataframe(df.head())

        # OPtions for Data Cleaning
        st.subheader("🧹 Data Cleaning Options")
        if st.checkbox(f"Clean Data for {file.name}"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"Remove Duplicates from {file.name}"):
                    df.drop_duplicates(inplace = True)
                    st.write("Duplicates removed!")

            with col2:
                if st.button(f"Fill missing values for {file.name}"):
                    numeric_cols = df.select_datatypes(include = ['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write("Missing values have been filled!")
        

        # Choose Specific Columns to keep or convert
        st.subheader("Select Columns to Convert")
        columns = st.multiselect(f"Choose Columns for {file.name}", df.columns, default = df.columns)
        df = df[columns]


        # Create some visualizations
        st.subheader("📊 Data Visualizations")
        if st.checkbox(f"Show Visualizations for {file.name}"):
            st.bar_chart(df.select_datatypes(include = 'number').iloc[:,:2])  #iloc --> i_location

        
        # Convert the file --> CSV to Excel
        st.subheader("🔰 Options")
        conversion_type = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key = file.name)
        if st.button(f"Convert {file.name}"):
            buffer = BytesIO()
            if conversion_type == "CSV":
                df.to_CSV(buffer, index = False)
                file_name = file.name.replace(file_ext, ".csv")
                mim_type = "text/csv"    #mim_type --> memory type

            elif conversion_type == "Excel":
                df.to_excel(buffer, index = False)
                file_name = file.name.replace(file_ext, ".xlsx")
                mim_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" #mim_type --> memory type
            buffer.seek(0)


            # Download Button
            st.download_button(
                label = f"🔽 Download {file.name} as {conversion_type}",
                data = buffer,
                filename = file_name,
                mim = mim_type
            )
        st.success("🎇 All files processed!")