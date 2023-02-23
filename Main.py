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
total_cost = filtered_df.groupby(['cost']).sum()

col1, col2, col3, col4 = st.columns([0.1, 1, 1, 0.1])
with col2:
    st.dataframe(filtered_df)
with col3:
    st.write(
        f"""
        <br><br>
        <div class="base-wrapper" style="background-color: green; opacity: 0.1; border-radius: 2.5rem;
        border-top: 2.5px solid #224B90; border-bottom: 2.5px solid #224B90;
        border-left: 2.5px solid #224B90; border-right: 2.5px solid #224B90;
        background-repeat: no-repeat;
        opacity: 0.8; background-size: 80px;">
            <div class="hero-wrapper">
                <div class="hero-container" style="width: 300px; height: 150px;">
                    <div class="hero-container-content">
                        <span class="subpages-container-product darkblue-span" style="text-align: right; font-size: 18px; margin-left: -2.5em; margin-top: 2.5em; line-height: 30px; text-transform: capitalize; color: white;">Turnover cost</span>
                        <span class="subpages-container-product darkblue-span" style="text-align: right; font-size: 48px; margin-left: -0.5em; margin-top: 0.25em; color: white;">{total_cost}</span>
                    </div>
                </div>
            </div><br>
        </div>
        """,
        unsafe_allow_html=True,
        )


cols1, cols2, cols3, cols4 = st.columns([0.1, 1, 1, 0.1])
with cols2:
    kmf = KaplanMeierFitter()
    fig, ax = plt.subplots(figsize=(10, 5), dpi=500)

    ## Employees with coaching

    cohort1 = filtered_df[filtered_df['type'] == "voluntary"]
    voluntary_x_median = cohort1['years_tenure'].median()


    kmf.fit(durations=cohort1["years_tenure"],
            event_observed=cohort1["event"],
            label='Voluntary turnover')

    kmf.plot_survival_function(ax=ax, ci_show=False)

    ## Employees without coaching

    cohort2 = filtered_df[filtered_df['type'] != "voluntary"]
    involuntary_x_median = cohort2['years_tenure'].median()

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
