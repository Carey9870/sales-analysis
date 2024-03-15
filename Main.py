# to run app - open cmd - streamlit run Main.py
# import libraries

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
import altair as alt
import streamlit as st
from streamlit_extras.dataframe_explorer import dataframe_explorer

# config the page width
st.set_page_config(page_title="Home", page_icon="", layout="wide")

# load data set
df = pd.read_csv('data.csv')

#st.dataframe(df, use_container_width=True)

# sidebar
st.sidebar.image('./logo1.png')

# sidebar date picker
with st.sidebar:
    st.title('Select Date Range')
    start_date = st.date_input(label='Start Date')

with st.sidebar:
    end_date = st.date_input(label='End Date')

st.error('You have chosen analytics from: ' + str(start_date) + ' to ' + str(end_date))

# filter data range
df2 = df[
            (df['OrderDate'] >= str(start_date)) &
            (df['OrderDate'] <= str(end_date))
        ]

with st.expander('Filter Excel Data'):
    filtered_df = dataframe_explorer(df2, case=False)
    st.dataframe(filtered_df)

a1, a2 = st.columns(2)

with a1:
    st.subheader('Product and Qualities', divider='rainbow')
    source = pd.DataFrame({
        'Quantity ($)': df2['Quantity'],
        'Product': df2['Product']
    })
    bar_chart = alt.Chart(source).mark_bar().encode(
        x = "sum(Quantity ($)):Q",
        y = alt.Y("Product:N", sort="-x")
    )
    st.altair_chart(bar_chart, use_container_width=True)

# Metrics
with a2:
    st.subheader('Data Metrics', divider='rainbow')
    from streamlit_extras.metric_cards import style_metric_cards
    col1, col2 = st.columns(2)
    col1.metric(label='All number of Items', value=df2.Product.count(), delta='All Items in Dataset')
    col2.metric(label='Sum of Product Price USD', value=f"{df2.TotalPrice.sum():,.0f}", delta = df2.TotalPrice.median())
    
    col11, col22, col33 = st.columns(3)
    col11.metric(label='Maximum Price', value=f"{df2.TotalPrice.max():,.0f}", delta = "High Price")
    col22.metric(label='Minimum Price', value=f"{df2.TotalPrice.min():,.0f}", delta = "Low Price")
    col33.metric(label='Price Range', value=f"{df2.TotalPrice.max() - df2.TotalPrice.min():,.0f}", delta = "Range")
    
    # style the metric
    #style_metrics_cards(background_color='#3c4d66', border_left_color='#e6200e', border_color='#00060a')
    
b1, b2 = st.columns(2)
# dot plot
with b1:
    st.subheader('Products & Total Price', divider='rainbow')
    source = df2
    chart = alt.Chart(source).mark_circle().encode(
        x = 'Product',
        y = 'TotalPrice',
        color='Category'
    ).interactive()
    
    st.altair_chart(chart, theme='streamlit', use_container_width=True)

with b2:
    st.subheader('Product and UnitPrice', divider='rainbow')
    source = pd.DataFrame({
        'Product ': df2['Product'],
        'UnitPrice': df2['UnitPrice'],
        'Date': df2['OrderDate']
    })
    bar_chart = alt.Chart(source).mark_bar().encode(
        x = "month(Date):O",
        y = "sum(UnitPrice ($)):Q",
        color="Product:N"
    )
    st.altair_chart(bar_chart, use_container_width=True)

c1, c2 = st.columns(2)
# dot plot
with c1:
    st.subheader('Products & UnitPrice', divider='rainbow')
    feature_x = st.selectbox('select X, qualitative data', df2.select_dtypes('object').columns)
    feature_y = st.selectbox('select Y, quantitative data', df2.select_dtypes('number').columns)
    
    fig, ax = plt.subplots()
    sns.scatterplot(data=df2, x=feature_x, y=feature_y, hue=df2.Product, ax=ax)
    st.pyplot(fig)

with c2:
    st.subheader('Features by Frequency', divider='rainbow')
    feature = st.selectbox('select only, qualitative data', df2.select_dtypes('object').columns)
    fig, ax = plt.subplots()
    ax.hist(df2[feature], bins=20)
    
    ax.set_title(f'Histogram of {feature}')
    ax.set_xlabel(feature)
    ax.set_ylabel('Frequency')
    st.pyplot(fig)

