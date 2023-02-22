#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on:  
@author: raju1g
"""
from dataclasses import dataclass
from typing import ClassVar
#pip install snowflake
from snowflake.snowpark.session import Session

# main.py
# Initialize connection.
def init_connection() -> Session:
    return Session.builder.configs(st.secrets["snowpark"]).create()

if __name__ == "__main__":
    # Initialize the filters
    session = init_connection()

@dataclass
class OurFilter:
    """This dataclass represents the filter that can be optionally enabled.

    It is created to parametrize the creation of filters from Streamlit and to keep the state."""
    # Class variables
    table_name: ClassVar[str]
    session: ClassVar[Session]

    # The name to display in UI
    human_name: str
    # Column in the table which will be used for filtering
    table_column: str
    # ID of the streamlit widget
    widget_id: str
    # The type of streamlit widget to generate
    widget_type: callable
    # Field to track if the filter is active. Can be used for filtering the list of filters
    is_enabled: bool = False
    # max value
    _max_value: int = 0
    # dataframe method that will be used for filtering the data
    _df_method: str = ""

def __post_init__(self):
    if self.widget_type not in (st.select_slider, st.checkbox):
        raise NotImplemented

    if self.widget_type is st.select_slider:
        self._df_method = "between"
        self._max_value = (
            self.session.table(MY_TABLE)
            .select(max(col(self.table_column)))
            .collect()[0][0]
        )
    elif self.widget_type is st.checkbox:
        self._df_method = "__eq__"


def create_widget(self):
    if self.widget_type is st.select_slider:
        base_label = "Select the range of"
    elif self.widget_type is st.checkbox:
        base_label = "Is"
    else:
        base_label = "Choose"
    widget_kwargs = dict(label=f"{base_label} {self.widget_id}", key=self.widget_id)
    if self.widget_type is st.select_slider:
        widget_kwargs.update(
            dict(
                options=list(range(self.max_value + 1)),
                value=(0, self.max_value),
            )
        )
    # Invocation of the streamlit method to place the widget on the page
    # e.g. st.checkbox(**widget_kwargs)
    self.widget_type(**widget_kwargs)


def __call__(self, _table: Table):
    """This method turns this class into a functor allowing to filter the dataframe.

    This allows to call it like so:

    f = OurFilter(...)
    new_table = last_table[f(last_table)]"""
    return methodcaller(self.df_method, **(self._get_filter_value()))(
        _table[self.table_column.upper()]
    )

def _get_filter_value(self):
    """Custom unpack function that retrieves the value of the filter
    from session state in a format compatible with self._df_method"""
    _val = st.session_state.get(self.widget_id)
    if self.widget_type is st.checkbox:
        # For .eq
        return dict(other=_val)
    elif self.widget_type is st.select_slider:
        # For .between
        return dict(lower_bound=_val[0], upper_bound=_val[1])
    else:
        raise NotImplemented


from typing import Iterable

import streamlit as st
from lib.filterwidget import OurFilter
from toolz import pluck


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

df = load_data()
MY_TABLE = df

def _get_active_filters() -> filter:
    return filter(lambda _: _.is_enabled, st.session_state.filters)

def _is_any_filter_enabled() -> bool:
    return any(pluck("is_enabled", st.session_state.filters))

def _get_human_filter_names(_iter: Iterable) -> Iterable:
    return pluck("human_name", _iter)

def draw_sidebar():
    """Should include dynamically generated filters"""

    with st.sidebar:
        selected_filters = st.multiselect(
            "Select which filters to enable",
            list(_get_human_filter_names(st.session_state.filters)),
            [],
        )
        for _f in st.session_state.filters:
            if _f.human_name in selected_filters:
                _f.enable()

        if _is_any_filter_enabled():
            with st.form(key="input_form"):

                for _f in _get_active_filters():
                    _f.create_widget()
                st.session_state.clicked = st.form_submit_button(label="Submit")
        else:
            st.write("Please enable a filter")

if __name__ == "__main__":
    # Initialize the filters
    session = init_connection()
    OurFilter.session = session
    OurFilter.table_name = MY_TABLE

    st.session_state.filters = (
        OurFilter(
            human_name="Gender",
            table_column="gender",
            widget_id="gender",
            widget_type=st.multiselect,
        ),
        OurFilter(
            human_name="Tenure",
            table_column="years_tenure",
            widget_id="tenure_slider",
            widget_type=st.select_slider,
        )
    )

    draw_sidebar()


def draw_main_ui(_session: Session):
    """Contains the logic and the presentation of the main section of the UI"""
    if _is_any_filter_enabled():  # Do not run any logic if no filters are actually enabled

        customers: Table = _session.table(MY_TABLE)
        table_sequence = [customers]

        _f: MyFilter
        for _f in _get_active_filters():
            # This block generates the sequence of dataframes as continually applying AND filtering set by the sidebar
            # The dataframes are to be used in the Sankey chart.

            # First, get the last dataframe in the list
            last_table = table_sequence[-1]
            # Apply the current filter to it
            new_table = last_table[
                # At this point the filter will be applied to the dataframe using the __call__ method
                _f(last_table)
            ]
            # And save it in the sequence
            table_sequence += [new_table]

        st.header("Dataframe preview")

        st.write(table_sequence[-1].sample(n=5).to_pandas().head())
    else:
        st.write("Please enable a filter in the sidebar to show transformations")
