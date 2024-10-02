import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Title of the app
st.title("Data Analysis Streamlit App")

# Upload the data file
uploaded_file = st.file_uploader("Upload your CSV file", type="csv")

if uploaded_file is not None:

    st.text("Uploading file...")
    # Load the data
    data = pd.read_csv(uploaded_file)

    # Display the first few rows of the data
    st.write("### Data Preview:")
    st.dataframe(data.head())

    # # Perform basic analysis
    # st.write("### Summary Statistics:")
    # st.write(data.describe())

    # column names 
    st.write("Different columns")
    st.write(data.columns)
    
    # calendar names 
    st.write("Different Calendars")
    cals = data["Calendar Name"].unique()
    st.write(cals)

    st.write(type(cals))
    # option= st.selectbox(cals, options = array)
    # st.write("You selected this ", option)


    # # Example analysis: Count of a categorical variable
    # if 'category_column' in data.columns:  # Replace with your actual column name
    #     category_counts = data['category_column'].value_counts()
    #     st.write("### Category Counts:")
    #     st.bar_chart(category_counts)
