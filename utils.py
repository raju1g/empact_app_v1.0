#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 11 12:30:14 2021
@author: raju1g
"""

import streamlit as st
from datetime import datetime
from datetime import timedelta
from typing import List, Dict
import session
from typing import List
import re
import numpy as np
import math
import pandas as pd
import random
import os
import time
import base64
from io import BytesIO
from pathlib import Path
#from ua_parser import user_agent_parser



def local_css(file_name):
    """
        This function will add css file to streamlit app.
        Write html-code to streamlit app.

        Parameters
        ----------
        file_name : string
            Path to file.

        Returns
        -------
        None.
    """
    with open(file_name) as file:
        st.markdown(
            f'<style type="text/css">{file.read()}</style>',
            unsafe_allow_html=True
        )


def image_to_bytes(img_path, html=1):
    """
        This function makes PNG image to bytes, which we can show on HTML page

        Parameters
        ----------
        img_path : String
            Path to the image file which you want to show.

        Returns
        -------
        image_html : String
            HTML code which includes the image in base64 format.
        """

    img_bytes = Path(img_path).read_bytes()
    encoded = base64.b64encode(img_bytes).decode()
    if html == 1:
        image_html = "<img src='data:image/png;base64,{}' style='display: block; text-align: center; width: 2em; margin: 5em auto;' />".format(
            encoded)
    else:
        image_html = f"data:image/png;base64,{encoded}"

    return image_html


def reload_window():
    """ Reloads the user's entire browser window """
    st.write(
        f"""
        <iframe src="resources/window_reload.html?load_user_data=true" height="0" width="0" style="border: none; float: right;"></iframe>""",
        unsafe_allow_html=True,
    )
    time.sleep(1)


# JAVASCRIPT / CSS HACK METHODS

def load_image(path):
    return base64.b64encode(Path(str(os.getcwd()) + "/" + path).read_bytes()).decode()


def hide_iframes():
    st.write(
        f"""<iframe src="resources/hide-iframes.html" height = 0 width = 0></iframe>""",
        unsafe_allow_html=True,
    )


def gen_pdf_report():
    st.write(
        """
    <iframe src="resources/ctrlp.html" height="100" width="350" style="border:none; float: right;"></iframe>
    """,
        unsafe_allow_html=True,
    )


def make_clickable(text, link):
    # target _blank to open new window
    # extract clickable text to display for your link
    return f'<a target="_blank" href="{link}">{text}</a>'


def gen_whatsapp_button(info) -> None:
    """Generate WPP button

    Args:
        info: config["contact"]
    """
    url = "https://api.whatsapp.com/send?text={}&phone=${}".format(info["msg"], info["phone"])
    st.write(
        """ 
         <a href="%s" class="float" target="_blank" id="messenger">
                <i class="material-icons">?</i>
                <p class="float-header">Doubts?</p></a>
        """
        % url,
        unsafe_allow_html=True,
    )


def gen_teams_button(info) -> None:
    """Generate Teams button

    Args:
        info: config["contact"]
    """
    url = "https://teams.microsoft.com/_#/conversations/?ctx=chat".format(info["msg"], info["phone"])
    st.write(
        """ 
         <a href="%s" class="float" target="_blank" id="messenger">
                <i class="material-icons">?</i>
                <p class="float-header">Doubts?</p></a>
        """
        % url,
        unsafe_allow_html=True,
    )


def manage_user_existence(session_state):
    """
        Decides if the user is new or not and if it is new generates a random id
        Will not try to do it twice because we can have the case of the user refusing to hold our cookies
        therefore we will consider him the anonymous user and give up trying to give him our cookie.
    """
    hash_id = gen_hash_code(size=32)
    update_user_public_info()
    time.sleep(0.1)
    give_cookies("user_unique_id", hash_id, 99999, True)


def gen_hash_code(size=16):
    return "".join(
        random.choice("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuv")
        for i in range(size)
    )


def parse_headers(request):
    """ Takes a raw streamlit request header and converts it to a nicer dictionary """
    data = dict(request.headers.items())
    ip = request.remote_ip
    if "Cookie" in data.keys():
        data["Cookie"] = dict([i.split("=", 1) for i in data["Cookie"].split("; ")])
        data["cookies_initialized"] = True
    else:
        data["Cookie"] = dict()
        data["cookies_initialized"] = False
    if "user_public_data" in data["Cookie"].keys():
        data["Cookie"]["user_public_data"] = dict(
            [i.split("|:", 1) for i in data["Cookie"]["user_public_data"].split("|%")]
        )
    data["Remote_ip"] = ip
    data.update(parse_user_agent(data["User-Agent"]))
    return data


def parse_user_agent(ua_string):
    #in_data = Parse(ua_string)
    out_data = dict()
    data_reference = [
        ["os_name", ["os", "family"]],
        ["os_version", ["os", "major"]],
        ["device_manufacturer", ["device", "brand"]],
        ["device_model", ["device", "model"]],
        ["platform", ["user_agent", "family"]],
        ["app_version", ["user_agent", "major"]],
    ]
    for key_in, keys_out in data_reference:
        try:
            out_data["ua_" + key_in] = [keys_out[0]][keys_out[1]]
        except:
            out_data["ua_" + key_in] = None
    return out_data


def give_cookies(cookie_name, cookie_info, cookie_days=99999, rerun=False):
    """ Gives the user a browser cookie """
    # Cookie days is how long in days will the cookie last
    st.write(
        f"""<iframe src="resources/cookiegen.html?cookie_name={cookie_name}&cookie_value={cookie_info}&cookies_days={cookie_days}" height="0" width="0" style="border: 1px solid black; float: right;"></iframe>""",
        unsafe_allow_html=True,
    )
    if rerun:
        time.sleep(1)
        reload_window()
        # session.rerun()


def update_user_public_info():
    """ updates the user's public data for us like his ip address and geographical location """
    st.write(
        f"""
        <iframe src="resources/cookiegen.html?load_user_data=true" height="0" width="0" style="border: none; float: right;"></iframe>""",
        unsafe_allow_html=True,
    )


def reload_window():
    """ Reloads the user's entire browser window """
    st.write(
        f"""
        <iframe src="resources/window_reload.html?load_user_data=true" height="0" width="0" style="border: none; float: right;"></iframe>""",
        unsafe_allow_html=True,
    )
    time.sleep(1)



