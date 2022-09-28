import streamlit as st
import pandas as pd
import numpy as np
from pandas_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report #This can display pandas profile object in streamlit
import sys
import os

st.set_page_config(page_title="Data profiler",layout="wide")

#validation on type of file uploaded:

def validate_file(file):
    filename = file.name
    name,ext = os.path.splitext(filename)
    if ext in ('.csv','.xlsx'):
        return ext
    else:
        return False

def get_file_size(file):
    size_bytes = sys.getsizeof(file)
    size_mb = size_bytes/(1024**2)
    return np.round(size_mb,1)





#Step 1 : Creating a sidebar

with st.sidebar:
    uploaded_file = st.file_uploader("Upload .csv,.xlsx files not exceeding 10 MB")
    if uploaded_file is not None:
        ext = validate_file(uploaded_file)
        size_mb = get_file_size(uploaded_file)
        if ext is not False and size_mb<=10:
            st.write('Modes of operation')
            minimal_choice = st.checkbox("Do you want minimal report?")

            display_mode = st.radio("Display mode",options=('Primary','Dark','Orange'))

            if display_mode=='Primary':
                dark=False
                orange=False
            elif display_mode=='Dark':
                dark=True
                orange=False
            else:
                dark=False
                orange=True
            
if uploaded_file is not None:
    if size_mb<=10:
        if ext:
            if ext == '.csv':
                df = pd.read_csv(uploaded_file)
            elif ext == '.xlsx':
                xl_file = pd.ExcelFile(uploaded_file)
                sheet_tuple = tuple(xl_file.sheet_names)
                sheet_name = st.sidebar.selectbox('Select the sheet',sheet_tuple)
                df = pd.read_excel(uploaded_file,sheet_name=sheet_name)
            with st.spinner('Generating the report'):
                pr = ProfileReport(df,minimal=minimal_choice,dark_mode=dark,orange_mode=orange)
            st_profile_report(pr)  
        else:
            st.error("Please upload either .csv or .xlsx only")  
    else:
        st.error("Maximum size of the file should be 10MB but received {}MB".format(size_mb))

else:
    st.title("Data Profiler")
    st.info("Upload your file on the left sidebar to generate data report")

        





























