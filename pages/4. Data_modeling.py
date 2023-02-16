import streamlit as st
import pandas as pd
import numpy as np
import datetime as dt
import seaborn as sns

import matplotlib.pyplot as plt
import plotly.express as px
import matplotlib as mpl
import plotly.graph_objs as go
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.metrics import classification_report

# The code below is for the title and logo for this page.
st.set_page_config(page_title="EmpAct Cooperative App (beta)", page_icon="📊")


st.title("Analyzing employee turnover using linear regression")

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

with st.expander("What is linear regression?"):

    st.write("")

    st.markdown(
        """

A linear regression equation describes the relationship between the independent variables (IVs) and the dependent variable (DV). It can also predict new values of the DV for the IV values you specify.
In regression analysis, the procedure estimates the best values for the constant and coefficients. Typically, regression models switch the order of terms in the equation compared to algebra by displaying the constant first and then the coefficients. It also uses different notation, as shown below for simple regression.

Y = β0 + β1X1
Using this notation, β0 is the constant, while β1 is the coefficient for X. Multiple regression just adds more βkXk terms to the equation up to K independent variables (Xs).


"""
    )

    st.write("")

    st.markdown(
        """

The underlying code models the data to answer the question:

 *If an employee receives a high engagement score then is that employee more likely to continue in the same organisation?"*

The data is visualised using [Plotly](https://plotly.com/python/).

    """
    )

    st.write("")


@st.experimental_memo
def load_data():

    # Load data
    df = pd.read_excel("datasets/regression.xlsx")

    return df


df = load_data()
feature_cols = ["Tenure (in years)", "score"]
X = df[feature_cols]
x1 = df["Tenure (in years)"]
y1 = df["score"]
y = df["continuation"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=16)

with st.expander("Show the `regression` dataframe"):
    st.write(df)

try:
    fig = px.scatter(df, x=x1, y=y1, trendline="ols")
    fig


except IndexError:
    st.warning("This is throwing an exception, bear with us!")