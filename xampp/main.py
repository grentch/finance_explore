import streamlit as st

# Custom imports 

from pages import Main_Page
from pages import Explore
from pages import Explore_Raw_Data
from pages import Load_Data
from pages import Edit_Data


st.set_page_config(page_title="page", layout="wide")


menu = st.sidebar.radio(
         'Select Menu:', ['Main','Explore Categories','Explore raw data','Load Data into Database','Edit Data'],index=0)


if menu == "Main":
    main = Main_Page.main_page()
    main.app()

if menu == "Explore Categories":
    explore = Explore.explore_page()
    explore.app()

if menu == "Explore raw data":
    exp = Explore_Raw_Data.explore_raw()
    exp.app()

if menu == "Load Data into Database":
    load = Load_Data.load_data()
    load.app()

if menu == "Edit Data":
    edit = Edit_Data.edit_data()
    edit.app()

    