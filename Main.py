#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on:  
@author: raju1g
"""
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on:
@author: raju1g
"""

import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
from pandas.api.types import (
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype,
)

st.title("Auto Filter Dataframes in Streamlit")
st.write(
    """This app accomodates the blog [here](<https://blog.streamlit.io/auto-generate-a-dataframe-filtering-ui-in-streamlit-with-filter_dataframe/>)
    and walks you through one example of how the Streamlit
    Data Science Team builds add-on functions to Streamlit.
    """
)


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


def load_data():

    # Load data
    df1 = pd.read_csv("datasets/turnover.csv", engine="python", encoding="ISO-8859-1")
    df1[["cost"]] = np.random.randint(10000, size=(1129, 1)).astype(float)
    df1[["year"]] = np.random.randint([2021, 2022], size=(1129, 1)).astype(int)
    df1 = df1.drop(["traffic"], axis=1)
    df1 = df1.drop(["head_gender"], axis=1)
    df1 = df.drop(["greywage"], axis=1)
    df1 = df1.drop(["way"], axis=1)
    df1 = df1.drop(["profession"], axis=1)
    df1 = df1.drop(["extraversion"], axis=1)
    df1 = df1.drop(["independ"], axis=1)
    df1 = df1.drop(["selfcontrol"], axis=1)
    df1 = df1.drop(["anxiety"], axis=1)
    df1 = df1.drop(["coach"], axis=1)
    df1 = df1.drop(["industry"], axis=1)
    df1 = df1.rename({'novator': 'engagement'}, axis=1)
    df1['benefits'] = pd.Series(random.choices(['yes', 'no'], weights=[1, 1], k=len(df)))
    df1['type'] = pd.Series(random.choices(['voluntary', 'involuntary'], weights=[1, 1], k=len(df)))
    df1['reason'] = pd.Series(random.choices(
        ['Better salary and benefits', 'Lack of career growth opportunities', 'Poor management and work culture',
         'Unhappy with job responsibilities', 'Violation of company policies and procedures',
         'Poor performance and attendance', 'Conflict with colleagues and manager',
         'Misconduct and inappropriate behavior'], weights=[1, 1, 1, 1, 1, 1, 1, 1], k=len(df)))
    df1["years_tenure"] = df1["stag"] / 12
    df1 = df1.drop(["stag"], axis=1)
    df1['years_tenure'] = df1["years_tenure"].round(1)
    return df1

st.dataframe(filter_dataframe(df1))
