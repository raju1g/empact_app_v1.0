import streamlit as st
import pandas as pd
import numpy as np
import itertools
from itertools import product
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

st.set_page_config(page_title="EmpAct Cooperative App",
                   initial_sidebar_state="collapsed",
                   page_icon="🔮")


tabs = ["Main", "About"]
page = st.sidebar.radio("Tabs", tabs)


@st.cache(persist=False,
          allow_output_mutation=True,
          suppress_st_warning=True,
          show_spinner=True)


@st.experimental_memo
def load_data():

    # Load data
    df = pd.read_csv("datasets/turnover.csv", engine="python", encoding="ISO-8859-1")
    df[["cost"]] = np.random.randint(10000, size=(1129, 1)).astype(float)
    df[["year"]] = np.random.randint([2021, 2022], size=(1129, 1)).astype(int)
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


if tabs == 'Main':
    def create_scatter(feature1, feature2):
        fig = plt.figure(title="%s vs %s Relation" % (feature1.capitalize(), feature2.capitalize()))

        scat = plt.scatter(x=df[feature1],
                           y=df[feature2],
                           color=df["age"],
                           )

        plt.xlabel(feature1.capitalize())
        plt.ylabel(feature2.capitalize())

        plt.show()


