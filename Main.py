import streamlit as st
import pandas as pd
import numpy as np
import random
from lifelines import KaplanMeierFitter

## Data Visualization:
import matplotlib.pyplot as plt
import seaborn as sns

#%matplotlib inline

from plotly.offline import iplot, init_notebook_mode
import plotly.express as px

## Correlation
from scipy.stats.stats import pearsonr

## Let's install lifelines
#!pip install lifelines --upgrade --quiet

## Let's import lifelines
import lifelines

# The code below is for the title and logo for this page.
st.set_page_config(page_title="EmpAct Cooperative App (beta)", page_icon="📊")

st.title("Talent management audit (2022-23) - XYZ Oy")

st.subheader("Preface")

@st.experimental_memo
def load_data():

    # Load data
    df = pd.read_csv("datasets/turnover.csv", engine="python", encoding="ISO-8859-1")
    df[["cost"]] = np.random.randint(10000, size=(1129, 1)).astype(float)
    df = df.drop(["traffic"], axis=1)
    df = df.drop(["head_gender"], axis=1)
    df = df.drop(["greywage"], axis=1)
    df = df.drop(["way"], axis=1)
    df = df.drop(["profession"], axis=1)
    df = df.drop(["extraversion"], axis=1)
    df = df.drop(["independ"], axis=1)
    df = df.drop(["selfcontrol"], axis=1)
    df = df.drop(["anxiety"], axis=1)
    df = df.drop(["coach"], axis=1)
    df = df.drop(["industry"], axis=1)
    df = df.rename({'novator': 'engagement'}, axis=1)
    df['benefits'] = pd.Series(random.choices(['yes', 'no'], weights=[1, 1], k=len(df)))
    df['type'] = pd.Series(random.choices(['voluntary', 'involuntary'], weights=[1, 1], k=len(df)))
    df['reason'] = pd.Series(random.choices(
        ['Better salary and benefits', 'Lack of career growth opportunities', 'Poor management and work culture',
         'Unhappy with job responsibilities', 'Violation of company policies and procedures',
         'Poor performance and attendance', 'Conflict with colleagues and manager',
         'Misconduct and inappropriate behavior'], weights=[1, 1, 1, 1, 1, 1, 1, 1], k=len(df)))
    df["years_tenure"] = df["stag"] / 12
    df = df.drop(["stag"], axis=1)
    df['years_tenure'] = df["years_tenure"].round(1)
    return df


df = load_data()

with st.expander("Show the `Employee turnover` dataframe"):
    st.write(df)

df_new_slider_01 = df[["type", "reason", "gender", "benefits"]]
new_slider_01 = [col for col in df_new_slider_01]

st.write("")

cole, col1, cole, col2, cole = st.columns([0.1, 1, 0.05, 1, 0.1])

with col1:

    MetricSlider01 = st.selectbox("Pick your 1st metric", new_slider_01)

    #MetricSlider02 = st.selectbox("Pick your 2nd metric", new_slider_02, index=1)

    st.write("")

with col2:

    if MetricSlider01 == "type":
        # col_one_list = transaction_df_new["brand"].tolist()
        col_one_list = df_new_slider_01["type"].drop_duplicates().tolist()
        multiselect = st.multiselect(
            "Select the value(s)", col_one_list, ["voluntary", "involuntary"]
        )
        df = df[df["type"].isin(multiselect)]

    elif MetricSlider01 == "reasons":
        col_one_list = (
            df_new_slider_01["reasons"].drop_duplicates().tolist()
        )
        multiselect = st.multiselect(
            "Select the value(s)", col_one_list, ['Better salary and benefits','Lack of career growth opportunities', 'Poor management and work culture', 'Unhappy with job responsibilities', 'Violation of company policies and procedures', 'Poor performance and attendance', 'Conflict with colleagues and manager', 'Misconduct and inappropriate behavior']
        )
        df = df[
            df["reasons"].isin(multiselect)
        ]

try:
    kmf = KaplanMeierFitter()
    fig, ax = plt.subplots(figsize=(10, 5), dpi=500)

    ## Employees with coaching

    cohort1 = df[df["type"] == "voluntary"]

    kmf.fit(durations=cohort1["years_tenure"],
            event_observed=cohort1["event"],
            label='Voluntary turnover')

    kmf.plot_survival_function(ax=ax, ci_show=False)

    ## Employees without coaching

    cohort2 = df[df["type"] != "voluntary"]

    kmf.fit(durations=cohort2["years_tenure"],
            event_observed=cohort2["event"],
            label='Involuntary turnover')

    ## Adding a few details to the plot

    kmf.plot_survival_function(ax=ax, ci_show=False)

    ax.set_ylabel("Employee survival rate")
    ax.set_xlabel("Timeline - years")

    plt.text(5.15, 0.7, '50% voluntary turnover', size=10, color='lightblue')
    plt.text(5.15, 0.66, 'after 5 years', size=10, color='lightblue')
    plt.text(-0.5, 0.3, '50% involuntary turnover', size=10, color='orange')
    plt.text(-0.5, 0.26, 'after 3.5 years', size=10, color='orange')
    plt.axvline(x=4.9, color='lightblue', linestyle='--')
    plt.axvline(x=3.5, color='orange', linestyle='--')

    plt.legend(fontsize=9)

    for item in ([ax.title, ax.xaxis.label, ax.yaxis.label] +
                 ax.get_xticklabels() + ax.get_yticklabels()):
        item.set_fontsize(10)

except IndexError:
    st.warning("This is throwing an exception, bear with us!")
