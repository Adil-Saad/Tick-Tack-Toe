import streamlit as st
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

# Load the tips dataset
tips = sns.load_dataset('tips')

# Set the title of the dashboard
st.title("Tips Dataset Analysis Dashboard")

# Display the dataset
if st.checkbox('Show raw data'):
    st.subheader('Raw Data')
    st.write(tips)

# Create a sidebar for user input
st.sidebar.header("Filters")

# Gender filter
gender_filter = st.sidebar.multiselect(
    'Select Gender',
    options=tips['sex'].unique(),
    default=tips['sex'].unique()
)

# Day filter
day_filter = st.sidebar.multiselect(
    'Select Day',
    options=tips['day'].unique(),
    default=tips['day'].unique()
)

# Time filter
time_filter = st.sidebar.multiselect(
    'Select Time',
    options=tips['time'].unique(),
    default=tips['time'].unique()
)

# Apply filters
filtered_tips = tips[(tips['sex'].isin(gender_filter)) &
                     (tips['day'].isin(day_filter)) &
                     (tips['time'].isin(time_filter))]

# Display summary statistics
st.subheader('Summary Statistics')
st.write(filtered_tips.describe())

# Create a bar plot for total bill by day
st.subheader('Total Bill by Day')
plt.figure(figsize=(10, 5))
sns.barplot(x='day', y='total_bill', data=filtered_tips, estimator=sum)
plt.title('Total Bill by Day')
plt.ylabel('Total Bill ($)')
st.pyplot(plt)

# Create a scatter plot for total bill vs tip
st.subheader('Total Bill vs Tip')
plt.figure(figsize=(10, 5))
sns.scatterplot(x='total_bill', y='tip', data=filtered_tips, hue='sex', style='time')
plt.title('Total Bill vs Tip')
plt.xlabel('Total Bill ($)')
plt.ylabel('Tip ($)')
st.pyplot(plt)

# Create a box plot for tips by day
st.subheader('Box Plot of Tips by Day')
plt.figure(figsize=(10, 5))
sns.boxplot(x='day', y='tip', data=filtered_tips)
plt.title('Box Plot of Tips by Day')
plt.xlabel('Day')
plt.ylabel('Tip ($)')
st.pyplot(plt)
