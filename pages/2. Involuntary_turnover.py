import streamlit as st
import pandas as pd
import numpy as np
import datetime as dt

import matplotlib.pyplot as plt
import matplotlib as mpl
import plotly.graph_objs as go

# The code below is for the title and logo for this page.
st.set_page_config(page_title="EmpAct Cooperative App (beta)", page_icon="📊")


st.title("`Involuntary turnover`")

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

    `Involuntary turnover` of an employee in an organisation occurs when that employee leaves that organisation due to the termination of his/her/their contract. 
    
    The following reasons for involuntary turnover were considered in the analysis:
    
    - `Violation of company policies and procedures`
    - `Poor performance and attendance`
    - `Conflict with colleagues and manager`
    - `Misconduct and inappropriate behavior`
    - `Theft and fraud`

"""
    )

    st.write("")

    st.markdown(
        """

    The underlying code groups employees according to tenure and plots against the no. of turnover employees. Employees that stayed in the organisation for more than 3 years were less likely to involuntarily leave the organisation as compared to those that served for less than 3 years.

    The data is visualised using [Plotly](https://plotly.com/python/).

    """
    )

    st.write("")


@st.experimental_memo
def load_data():

    # Load data
    df = pd.read_excel("datasets/involuntary_turnover.xlsx")

    return df


df = load_data()
with st.expander("Show the `involuntary turnover` dataframe"):
    st.write(df)

df_new_slider_01 = df[["Reason for termination", "Tenure (in years)"]]
new_slider_01 = [col for col in df_new_slider_01]


st.write("")

cole, col1, cole, col2, cole = st.columns([0.1, 1, 0.05, 1, 0.1])

with col1:

    MetricSlider01 = st.selectbox("Pick your 1st metric", new_slider_01)

    st.write("")

with col2:

    if MetricSlider01 == "Reason for termination":
        # col_one_list = transaction_df_new["brand"].tolist()
        col_one_list = df_new_slider_01["Reason for termination"].drop_duplicates().tolist()
        multiselect = st.multiselect(
            "Select the value(s)", col_one_list, ["Violation of company policies and procedures", "Poor performance and attendance", "Conflict with colleagues and manager", "Misconduct and inappropriate behavior", "Theft and fraud"]
        )
        df = df[df["Reason for termination"].isin(multiselect)]

    elif MetricSlider01 == "Tenure (in years)":
        col_one_list = (
            df_new_slider_01["Tenure (in years)"].drop_duplicates().tolist()
        )
        multiselect = st.multiselect(
            "Select the value(s)", col_one_list, [1, 2, 3, 5, 7]
        )
        df = df[
            df["Tenure (in years)"].isin(multiselect)
        ]

try:

    # Plotting the retention rate
    import plotly.graph_objects as go
    import plotly.express as px
    from bubbly.bubbly import bubbleplot

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df['Tenure (in years)'],
        y=df['no. of employees'],
        name='involuntary turnover',
        # mode='markers',
        marker_color='green',
        # marker_line_width=2, marker_size=30,
        text=df['no. of employees'],
        textposition='auto',
        legendgroup='1'))

    fig.update_layout(xaxis_tickangle=0, width=900, height=600, font_size=16,
                      font_family="Trebuchet MS",
                      xaxis_title="tenure (years)",
                      yaxis1_title="no. of employees",
                      # yaxis2_title="mins./match",
                      # yaxis3_title="(Poh.)",
                      # yaxis4_title="(Ita.)",
                      paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='white', showlegend=True)
    #fig.update_xaxes(tickfont_size=48, showgrid=False)
    #fig.update_yaxes(tickfont_size=48, showticklabels=True, showgrid=False)
    fig

except IndexError:
    st.warning("This is throwing an exception, bear with us!")
