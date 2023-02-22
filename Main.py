import streamlit as st
import pandas as pd
import numpy as np
import itertools
from itertools import product
from dataclasses import dataclass
from typing import List
import random
from lifelines import KaplanMeierFitter
import utils


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
  
utils.local_css("style_trial.css")   
st.write(
f"""
<div class="base-wrapper" style="background-color:#00A300;">
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

df = load_data()
with st.expander("Show the `employee turnover` dataframe"):
    st.dataframe(df, 100, 200)

st.write(
f"""
<br><br><br>
""", unsafe_allow_html=True,
)

gen_to = df['gender'].unique().tolist() 
reg_to = df['reason'].unique().tolist() 
typ_to = df['type'].unique().tolist() 
ben_to = df['benefits'].unique().tolist() 

# Create a table to have filters side by side :
col1, col2, col3, col4, col5, col6 = st.columns([0.5,1,1,1,1,0.5])
with col2:
    selected_gento = st.multiselect(
        'Gender:',
        gen_to
        )
with col3:
    selected_typto = st.multiselect(
        'Turnover type:',
        typ_to
        )
with col4:
    selected_reg_to = st.multiselect(
        'Turnover reason:',
        reg_to
        )
with col5:
    selected_ben_to = st.multiselect(
        'Benefits:',
        ben_to
        )
    
# try:
kmf = KaplanMeierFitter()
fig, ax = plt.subplots(figsize=(10, 5), dpi=500)

## Employees with coaching

cohort1 = df[df['type'] == "voluntary"]

kmf.fit(durations=cohort1["years_tenure"],
        event_observed=cohort1["event"],
        label='Voluntary turnover')

kmf.plot_survival_function(ax=ax, ci_show=False)

## Employees without coaching

cohort2 = df[df['type'] != "voluntary"]

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
# except IndexError:
#    st.warning("This is throwing an exception, bear with us!")






