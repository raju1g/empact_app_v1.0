import streamlit as st
import pandas as pd
import numpy as np
import datetime as dt

import matplotlib.pyplot as plt
import matplotlib as mpl
import plotly.graph_objs as go
import plotly.express as px

# The code below is for the title and logo for this page.
st.set_page_config(page_title="EmpAct Cooperative App (beta)", page_icon="📊")


st.title("`Employee engagement`")

st.write("")

st.markdown(
    """

"""
)
st.markdown(
    """

    This report is developed using [Streamlit](https://streamlit.io/) and is meant for demonstration purposes only.
    
"""
)

with st.expander("Definition"):

    st.write("")

    st.markdown(
        """

   `Employee engagement` is predominantly determined through the employee engagement score that is obtained through a feedback by the employees themselves. The score is a number in range 1-10 with 1 corresponding to least engaged and 10 corresponding to most engaged.
   

"""
    )

    st.write("")

    st.markdown(
        """

    The underlying code groups employees according to their engagement score and shows the distribution of each engagement score as a percentage of the total.

    The data is visualised using [Plotly](https://plotly.com/python/).

    """
    )

    st.write("")


@st.experimental_memo
def load_data():

    # Load data
    df = pd.read_excel("datasets/employee_engagement.xlsx")

    return df


df = load_data()
with st.expander("Show the `employee engagement` dataframe"):
    st.write(df)

try:
    fig = px.pie(df, values='Employee ID', names='Engagement score ')
    fig

except IndexError:
    st.warning("This is throwing an exception, bear with us!")