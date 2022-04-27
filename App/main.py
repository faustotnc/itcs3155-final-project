import streamlit as st
import altair as alt
import pandas as pd
from helpers import add_space
from pages import home, resources, choropleth, scatter_plot, age_group

# How to combine charts in Altair:
# Use the "+" operator to layer charts on top of each other
# Use the "&" operator to place charts next to each other vertically
# Use the "|" operator to place charts next to each other horizontally

st.set_page_config(page_title="UniStats", layout="wide")


@st.cache
# This function is cashed so that the data is not
# reloaded every time the app's state changes.
def load_data():
    data = pd.read_csv("./Datasets/Bachelor_Degree_Majors.csv")

    # Convert these columns to integers
    selection = [
        "Bachelors Degree Holders",
        "Science and Engineering",
        "Science and Engineering Related Fields",
        "Business",
        "Education",
        "Arts, Humanities and Others"
    ]

    data[selection] = data[selection].transform(
        [lambda v: int(v.replace(",", ""))])

    # Remove "Total" rows
    data = data[data.Sex != "Total"]

    # Append State Ids to the Data
    ids = pd.read_csv("./Datasets/StateIds.csv")
    data["StateId"] = [ids[ids.state == s].id.iloc[0] for s in data.State]

    return data


DATA = load_data()
PROGRAMS = ["Science and Engineering", "Science and Engineering Related Fields",
            "Business", "Education", "Arts, Humanities and Others"]


@st.cache
# This function is cashed so that the data is not
# re-aggregated every time the app's state changes.
def group_data_by_sex():
    return DATA.groupby(["State", "StateId", "Sex"]).sum().reset_index()


DATA_BY_SEX = group_data_by_sex()


with st.sidebar:
    st.title("UniStats")
    st.write("Empowering Equality in Higher Education.")

    add_space(32)

    # Create a page dropdown
    page = st.selectbox("Choose your page", [
                        "Home", "U.S. Map", "Age Groups", "Scatter Plot", "Resources"])

    add_space(32)
    st.write("Our dashboard displays various visualizations that will help you find specific states and college programs that will foster a more "
             "supportive learning environment. Once you find a state that you would like to move to, there is a link in our resources page that "
             "will direct you to specific universities that are located in each state. ")


if page == "Home":
    # Show the Header Section
    home.display_page()
elif page == "U.S. Map":
    # The Choropleth Map
    choropleth.display_page(PROGRAMS, DATA_BY_SEX)
elif page == "Age Groups":
    age_group.display_page(DATA, PROGRAMS)
elif page == "Scatter Plot":
    scatter_plot.display_page(DATA)
elif page == "Resources":
    # Show the footer section
    resources.display_page()
