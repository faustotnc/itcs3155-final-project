from turtle import title
import streamlit as st
from helpers import add_space
import altair as alt
from vega_datasets import data


def display_page(programs, data_by_sex):
    """
    The function for the Choropleth Map section.
    """

    # The title for this section
    _, c1, _ = st.columns([1, 3, 1])
    c1.subheader("Enrollment by State, Sex, and College Program")
    c1.write("This map can be filtered by sex and college program. Once you have selected your desired fields, the map will display the concentration of "
             "male/female enrollment in each state. The lighter the color, the less students enrolled. If the state is a darker blue, "
             "it means there are many students enrolled. Hovering over the state will show you exactly how many male/female students are enrolled in that state "
             "for your chosen program.")
    add_space(24, col=c1)
    program = c1.selectbox("Select College Program", programs)

    add_space(48)

    # The columns for the chart and radio buttons
    c1, c2 = st.columns([1, 1])

    states_map = alt.topo_feature(data.us_10m.url, 'states')

    map_female = alt.Chart(states_map, title="Female Enrollment").mark_geoshape().encode(
        color=alt.Color(f"{program}:Q", legend=alt.Legend(title="")),
        tooltip=["State:N", alt.Tooltip(
            f"{program}:Q", title="Enrollment", format=",")],
    ).transform_lookup(
        lookup="id",
        from_=alt.LookupData(data_by_sex[data_by_sex.Sex == "Female"], 'StateId', [
                             "State", *programs])
    ).project(
        type="albersUsa"
    ).properties(
        height=500
    )

    map_male = alt.Chart(states_map, title="Male Enrollment").mark_geoshape().encode(
        color=alt.Color(f"{program}:Q", legend=alt.Legend(title="")),
        tooltip=["State:N", alt.Tooltip(
            f"{program}:Q", title="Enrollment", format=",")],
    ).transform_lookup(
        lookup="id",
        from_=alt.LookupData(data_by_sex[data_by_sex.Sex == "Male"], 'StateId', [
                             "State", *programs])
    ).project(
        type="albersUsa"
    ).properties(
        height=500
    )

    # Add the Choropleth Map chart to the view
    c1.altair_chart(map_female, use_container_width=True)
    c2.altair_chart(map_male, use_container_width=True)
