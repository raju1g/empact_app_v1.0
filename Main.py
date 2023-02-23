#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on:
@author: raju1g
"""

import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
from lifelines import KaplanMeierFitter
import matplotlib.pyplot as plt
import seaborn as sns
import utils
import plotly.express as px
import plotly.graph_objects as go

from pandas.api.types import (
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype,
)

st.set_page_config(page_title="EmpAct Cooperative App",
                   initial_sidebar_state="collapsed",
                   layout="wide",
                   page_icon="🔮")

utils.local_css("style_trial.css")
st.write(
f"""
<div class="base-wrapper" style="background-color:#FA8072;">
    <div class="hero-wrapper">
        <div class="hero-container" style="width:100%; height:100px">
            <div class="hero-container-content">
                <span class="subpages-subcontainer-product white-span" style="margin-left: -0.5em;">Talent management audit</span>
            </div>
        </div>
    </div>
</div>
""",
unsafe_allow_html=True,
)

st.write(
f"""
<br><br><br>
""", unsafe_allow_html=True,
)

#st.title("Talent Management App")
#st.write(
#    """
#    """
#)


def filter_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds a UI on top of a dataframe to let viewers filter columns

    Args:
        df (pd.DataFrame): Original dataframe

    Returns:
        pd.DataFrame: Filtered dataframe
    """
    modify = st.checkbox("Add filters")

    if not modify:
        return df

    df = df.copy()

    # Try to convert datetimes into a standard format (datetime, no timezone)
    for col in df.columns:
        if is_object_dtype(df[col]):
            try:
                df[col] = pd.to_datetime(df[col])
            except Exception:
                pass

        if is_datetime64_any_dtype(df[col]):
            df[col] = df[col].dt.tz_localize(None)
    
    
    modification_container = st.container()

    with modification_container:
        to_filter_columns = st.multiselect("Filter dataframe on", df.columns)
        for column in to_filter_columns:
            left, right = st.columns((1, 20))
            # Treat columns with < 10 unique values as categorical
            if is_categorical_dtype(df[column]) or df[column].nunique() < 10:
                user_cat_input = right.multiselect(
                    f"Values for {column}",
                    df[column].unique(),
                    default=list(df[column].unique()),
                )
                df = df[df[column].isin(user_cat_input)]
            elif is_numeric_dtype(df[column]):
                _min = float(df[column].min())
                _max = float(df[column].max())
                step = (_max - _min) / 100
                user_num_input = right.slider(
                    f"Values for {column}",
                    min_value=_min,
                    max_value=_max,
                    value=(_min, _max),
                    step=step,
                )
                df = df[df[column].between(*user_num_input)]
            elif is_datetime64_any_dtype(df[column]):
                user_date_input = right.date_input(
                    f"Values for {column}",
                    value=(
                        df[column].min(),
                        df[column].max(),
                    ),
                )
                if len(user_date_input) == 2:
                    user_date_input = tuple(map(pd.to_datetime, user_date_input))
                    start_date, end_date = user_date_input
                    df = df.loc[df[column].between(start_date, end_date)]
            else:
                user_text_input = right.text_input(
                    f"Substring or regex in {column}",
                )
                if user_text_input:
                    df = df[df[column].astype(str).str.contains(user_text_input)]

    return df
#data_url = "https://raw.githubusercontent.com/raju1g/empact_app_v1.0/blob/main/"

df = pd.read_csv("datasets/penguins.csv")
filtered_df = filter_dataframe(df)
cohort1 = filtered_df[filtered_df['type'] == "voluntary"]
voluntary_x_median = cohort1['years_tenure'].median()
total_cost_voluntary = cohort1['cost'].aggregate('sum')
cohort2 = filtered_df[filtered_df['type'] != "voluntary"]
involuntary_x_median = cohort2['years_tenure'].median()
total_cost_involuntary = cohort2['cost'].aggregate('sum')

col1, col2, col3, col4, col5 = st.columns([0.1, 1, 0.5, 0.5, 0.1])
with col2:
    st.dataframe(filtered_df)
with col3:
    st.write(
        f"""
        <div class="base-wrapper" style="background-color: lightblue; opacity: 0.1; border-radius: 0.5rem;
        border-top: 2.5px solid #224B90; border-bottom: 2.5px solid #224B90;
        border-left: 2.5px solid #224B90; border-right: 2.5px solid #224B90;
        background-repeat: no-repeat;
        opacity: 0.8; background-size: 80px;">
            <div class="hero-wrapper">
                <div class="hero-container" style="width:100%; height:100px">
                    <div class="hero-container-content">
                        <span class="subpages-subcontainer-product white-span" style="margin-left: 0em; text-transform: capitalize; color: #224B90; font-size: 18px;">50% turnover after {voluntary_x_median} years</span>
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
        )
    
    st.write(
        f"""
        <br>
        <div class="base-wrapper" style="background-color: orange; opacity: 0.1; border-radius: 0.5rem;
        border-top: 2.5px solid #224B90; border-bottom: 2.5px solid #224B90;
        border-left: 2.5px solid #224B90; border-right: 2.5px solid #224B90;
        background-repeat: no-repeat;
        opacity: 0.8; background-size: 80px;">
            <div class="hero-wrapper">
                <div class="hero-container" style="width:100%; height:100px">
                    <div class="hero-container-content">
                        <span class="subpages-subcontainer-product white-span" style="margin-left: 0em; text-transform: capitalize; color: #224B90; font-size: 18px;">50% turnover after {involuntary_x_median} years</span>
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
        )
with col4:
    st.write(
        f"""
        <div class="base-wrapper" style="background-color: lightblue; opacity: 0.1; border-radius: 0.5rem;
        border-top: 2.5px solid #224B90; border-bottom: 2.5px solid #224B90;
        border-left: 2.5px solid #224B90; border-right: 2.5px solid #224B90;
        background-repeat: no-repeat;
        opacity: 0.8; background-size: 80px;">
            <div class="hero-wrapper">
                <div class="hero-container" style="width:100%; height:100px">
                    <div class="hero-container-content">
                        <span class="subpages-subcontainer-product white-span" style="margin-left: 0em; text-transform: capitalize; color: #224B90; font-size: 32px;">Cost € {total_cost_voluntary}</span>
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
        )
    
    st.write(
        f"""
        <br>
        <div class="base-wrapper" style="background-color: orange; opacity: 0.1; border-radius: 0.5rem;
        border-top: 2.5px solid #224B90; border-bottom: 2.5px solid #224B90;
        border-left: 2.5px solid #224B90; border-right: 2.5px solid #224B90;
        background-repeat: no-repeat;
        opacity: 0.8; background-size: 80px;">
            <div class="hero-wrapper">
                <div class="hero-container" style="width:100%; height:100px">
                    <div class="hero-container-content">
                        <span class="subpages-subcontainer-product white-span" style="margin-left: 0em; text-transform: capitalize; color: #224B90; font-size: 32px;">Cost € {total_cost_involuntary}</span>
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
        )

cols1, cols2, cols3, cols4 = st.columns([0.1, 1, 1, 0.1])
with cols2:
    st.write(
    f"""
    <br><br>
    """, unsafe_allow_html=True,
    )
    kmf = KaplanMeierFitter()
    fig, ax = plt.subplots(figsize=(10, 5), dpi=500)

    ## Employees with coaching

    kmf.fit(durations=cohort1["years_tenure"],
            event_observed=cohort1["event"],
            label='Voluntary turnover')

    kmf.plot_survival_function(ax=ax, ci_show=False)

    ## Employees without coaching

    kmf.fit(durations=cohort2["years_tenure"],
            event_observed=cohort2["event"],
            label='Involuntary turnover')

    ## Adding a few details to the plot

    kmf.plot_survival_function(ax=ax, ci_show=False)

    ax.set_ylabel("Employee survival rate")
    ax.set_xlabel("Timeline - years")

    plt.text(8.5, 0.8, '-- 50% voluntary turnover', size=9, color='lightblue')
    #plt.text(8, 0.66, 'after {0:.2f}.format(voluntary_x_median) years', size=10, color='lightblue')
    plt.text(8.5, 0.76, '-- 50% involuntary turnover', size=9, color='orange')
    #plt.text(8, 0.46, 'after {0:.2f}.format(involuntary_x_median) years', size=10, color='orange')
    plt.axvline(x=voluntary_x_median, color='lightblue', linestyle='--')
    plt.axvline(x=involuntary_x_median, color='orange', linestyle='--')

    plt.legend(fontsize=9)

    for item in ([ax.title, ax.xaxis.label, ax.yaxis.label] +
                 ax.get_xticklabels() + ax.get_yticklabels()):
        item.set_fontsize(10)
    fig

with cols3:
    config = {
            'scrollZoom': False,
            'displayModeBar': False,
            'editable': False,
            'showLink': False,
            'displaylogo': False,
        }
    figure_1 = px.histogram(filtered_df, x="reason")
    
    figure_1.update_layout(showlegend=False)
    figure_1.update_xaxes(tickfont_size=10, showgrid=False)
    figure_1.update_yaxes(showticklabels=False, showgrid=False)
    st.plotly_chart(figure_1, use_container_width=True, config=config)

st.write(
    f"""
    <br><br>
    """, unsafe_allow_html=True,
    )
st.title("Observations")
st.markdown(
"""
- Involuntary reasons account for more than 50% of total turnovers in women
- 60% of this involuntary turnover in women is performance related costing the company (i.e., 40% of the total turnover cost) and 30% due to conflict with company personnel
- Women without benefits get turned over (voluntarily as well as involuntarily) after 2 years (much lower than the sample average)
"""
)
st.title("Recommendations")
st.markdown(
"""
In order to significantly reduce the turnover cost to the company, we recommend the following points:
- To reduce the high turnover due to conflict with colleagues and managers, the onboarding and integration process needs to be thoroughly reviewed. 
- Better coaching and training programs need to be implemented to reduce performance related turnover in both men and women. 
"""
)
