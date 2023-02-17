import streamlit as st
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import datetime as dt

# The code below is for the title and logo for this page.
st.set_page_config(page_title="EmpAct Cooperative App (beta)", page_icon="📊")


st.title("`Voluntary turnover`")

st.write("")

st.markdown(
    """

    This report is developed using [Streamlit](https://streamlit.io/) and is meant for demonstration purposes only.

"""
)

with st.expander("Definition"):

    st.write("")

    st.markdown(
        """

    `Voluntary turnover` of an employee in an organisation occurs when that employee leaves that organisation without the termination of his/her/their contract. 
    
    The following reasons for voluntary turnover were considered in the analysis:
    
    - `Better salary and benefits`
    - `Lack of career growth opportunities`
    - `Relocating to another city`
    - `Poor management and work culture`
    - `Unhappy with job responsibilities`

    """
    )

    st.write("")

    st.markdown(
        """
    The underlying code groups employees according to tenure and plots against the cost of turnover. Employees that stayed in the organisation for more than 3 years were less likely to voluntarily leave the organisation as compared to those that served for less than 3 years.

    The data is visualised using [Plotly](https://plotly.com/python/).

    """
    )

    st.write("")


@st.experimental_memo
def load_data():

    # Load data
    df = pd.read_excel("datasets/voluntary_turnover.xlsx")

    return df


df = load_data()

with st.expander("Show the `Voluntary employee turnover` dataframe"):
    st.write(df)

df_new_slider_01 = df[["Reason for leaving", "Tenure (in years)"]]
new_slider_01 = [col for col in df_new_slider_01]


st.write("")

cole, col1, cole, col2, cole = st.columns([0.1, 1, 0.05, 1, 0.1])

with col1:

    MetricSlider01 = st.selectbox("Pick your 1st metric", new_slider_01)

    #MetricSlider02 = st.selectbox("Pick your 2nd metric", new_slider_02, index=1)

    st.write("")

with col2:

    if MetricSlider01 == "Reason for leaving":
        # col_one_list = transaction_df_new["brand"].tolist()
        col_one_list = df_new_slider_01["Reason for leaving"].drop_duplicates().tolist()
        multiselect = st.multiselect(
            "Select the value(s)", col_one_list, ["Better salary and benefits", "Lack of career growth opportunities", "Relocating to another city", "Poor management and work culture", "Unhappy with job responsibilities"]
        )
        df = df[df["Reason for leaving"].isin(multiselect)]

    elif MetricSlider01 == "Tenure (in years)":
        col_one_list = (
            df_new_slider_01["Tenure (in years)"].drop_duplicates().tolist()
        )
        multiselect = st.multiselect(
            "Select the value(s)", col_one_list, [1, 2, 3, 4, 5]
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
        y=df['Cost of turnover'],
        name='no. of employees',
        # mode='markers',
        marker_color='green',
        # marker_line_width=2, marker_size=30,
        text=df['no. of employees'],
        textposition='auto',
        legendgroup='1'))

    fig.update_layout(xaxis_tickangle=0, width=900, height=600, font_size=16,
                      font_family="Trebuchet MS",
                      xaxis_title="tenure (years)",
                      yaxis1_title="turnover cost (EUR)",
                      # yaxis2_title="mins./match",
                      # yaxis3_title="(Poh.)",
                      # yaxis4_title="(Ita.)",
                      paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='white', showlegend=True)
    #fig.update_xaxes(tickfont_size=48, showgrid=False)
    #fig.update_yaxes(tickfont_size=48, showticklabels=True, showgrid=False)
    fig

except IndexError:
    st.warning("This is throwing an exception, bear with us!")
