import streamlit as st
import pandas as pd
import numpy as np
import itertools
from dataclasses import dataclass
from typing import List
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


@dataclass(frozen=True)
class Variant:
    gender: str
    type: str
    reason: str
    benefits: str


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

# Initialization
if "type_use_input" not in st.session_state:
    st.session_state.type_use_input = df["type"].unique()

if "reg_use_input" not in st.session_state:
    st.session_state.reg_use_input = df["reason"].unique()

if "gen_use_input" not in st.session_state:
    st.session_state.gen_use_input = df["gender"].unique()

if "ben_use_input" not in st.session_state:
    st.session_state.ben_use_input = df["benefits"].unique()

row00_0, row00_1, row00_2 = st.columns([0.5, 0.25, 1])
with row00_0:
    container = st.container()
    all = st.checkbox("All", value=True)
    if all:
        type = container.multiselect(
            "Type:",
            st.session_state.type_use_input,
            default=st.session_state.type_use_input,
        )
        gender = container.multiselect(
            "Gender:",
            st.session_state.gen_use_input,
            default=st.session_state.gen_use_input,
        )
        reason = container.multiselect(
            "Reason:",
            st.session_state.reg_use_input,
            default=st.session_state.reg_use_input,
        )
        benefits = container.multiselect(
            "Benefits:",
            st.session_state.ben_use_input,
            default=st.session_state.ben_use_input,
        )
    else:
        type = container.multiselect(
            "Type:",
            st.session_state.type_use_input,
        )
        gender = container.multiselect(
            "Gender:",
            st.session_state.gen_use_input,
        )
        reason = container.multiselect(
            "Reason:",
            st.session_state.reg_use_input,
        )
        benefits = container.multiselect(
            "Benefits:",
            st.session_state.ben_use_input,
        )

sel = [gender, type, reason, benefits]
variants = list(itertools.product(*sel))
variants: List[Variant] = [
    Variant(gender=i[0], reason=i[1], type=i[2], benefits=i[3])
    for i in variants
]
totals = {}

for df in df.items():
    filtered_dfs = []

for variant in variants:
    filtered_df = df[
        (df["gender"] == variant.gender)
        & (df["reason"] == variant.reason)
        & (df["type"] == variant.type)
        & (df["benefits"] == variant.benefits)
        ]

    if not filtered_df.empty:
        filtered_dfs.append(filtered_df)

try:
    kmf = KaplanMeierFitter()
    fig, ax = plt.subplots(figsize=(10, 5), dpi=500)

    ## Employees with coaching

    cohort1 = filtered_dfs[filtered_dfs["type"] == "voluntary"]

    kmf.fit(durations=cohort1["years_tenure"],
            event_observed=cohort1["event"],
            label='Voluntary turnover')

    kmf.plot_survival_function(ax=ax, ci_show=False)

    ## Employees without coaching

    cohort2 = filtered_dfs[filtered_dfs["type"] != "voluntary"]

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
    fig
except IndexError:
    st.warning("This is throwing an exception, bear with us!")
