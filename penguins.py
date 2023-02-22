import pandas as pd
import pkg_resources
import numpy as np
import os
from os.path import dirname, exists, expanduser, isdir, join, splitext


def load_penguins(return_X_y=False,drop_na = False):
    """Load and return the penguins dataset (classification).
      The Palmer penguins dataset is a dataset for data exploration & visualization, and can be used as an
      alternative to the Iris dataset.
      =================   ==============
      Classes                          3
      Samples per class        [152,168,124]
      Samples total                  344
      Dimensionality                  8
      Features            real, integer, string, positive
      =================   ==============
      Read more in the :ref:`https://github.com/allisonhorst/palmerpenguins>`.
      Parameters
      ----------
      return_X_y : bool, default=False
          If True, returns a ``(data, target)`` tuple instead of a dataframe object.
          See below for more information about the `data` and `target` object.
      drop_na: bool, default=False
      If True drop rows from dataset that contain missing values. Only available when `return_X_y = True`
      Returns
      -------
      data : :class:`pandas.core.frame.DataFrame`
          data is a dataframe of shape (344  , 8) and has the following columns:
      =================   ==============
      species              a string denoting penguin species (Adélie, Chinstrap and Gentoo)
      island               a string denoting island in Palmer Archipelago, Antarctica (Biscoe, Dream or Torgersen)
      bill_length_mm       a number denoting bill length (millimeters)
      bill_depth_mm        a number denoting bill depth (millimeters)
      flipper_length_mm    an integer denoting flipper length (millimeters)
      body_mass_g          an integer denoting body mass (grams)
      sex                  a string denoting penguin sex (female, male)
      year                 an integer denoting the study year (2007, 2008, or 2009)
      =================   ==============
      (data, target) : tuple if ``return_X_y`` is True
          data : a dataframe of shape (344  , 4)  where each column corresponds to one of the four size measurements of penguins including bill_length_mm, bill_depth_mm, flipper_length_mm and body_mass_g.
          target: {ndarray, Series} of shape (344,)
              The classification target (i.e. penguin species).
      --------
      Let's say you are interested in the samples 10, 80, and 140, and want to
      know their class name.
      >>> from palmerpenguins.penguins import load_penguins
      >>> penguins = load_penguins()
      >>> list(penguins.iloc[[1, 160, 300],0])
      ['Adelie', 'Gentoo', 'Chinstrap']
      >>> dict(pd.value_counts(penguins.species))
      {'Adelie': 152, 'Gentoo': 124, 'Chinstrap': 68}
      """

    stream = pkg_resources.resource_stream(__name__, 'data/penguins.csv')
    penguins = pd.read_csv(stream)
    if return_X_y:
        if drop_na:
            penguins.dropna(inplace = True)
        data = penguins[['gender', 'reason',
                         'benefits']]
        target = penguins['type']


        return data, target

    return penguins
