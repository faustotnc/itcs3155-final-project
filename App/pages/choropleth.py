import streamlit as st
from helpers import add_space
import altair as alt
from vega_datasets import data


def display_page(programs, data_by_sex):
    """
    The function for the Choropleth Map section.
    """

    # The title for this section
    _, c1, _ = st.columns([0.5, 3, 0.5])
    c1.subheader("Enrollment by State, Sex, and College Program")
    c1.write("This map can be filtered by sex and college program. Once you have selected your desired fields, the map will display the concentration of "
             "male/female enrollment in each state. The lighter the color, the less students enrolled. If the state is a darker blue, "
             "it means there are many students enrolled. Hovering over the state will show you exactly how many male/female students are enrolled in that state "
             "for your chosen program.")
    add_space(24)

    # The columns for the chart and radio buttons
    _, c1, c2, _ = st.columns([0.5, 2, 1, 0.5])

    # The radio buttons and data filtering
    add_space(48, col=c2)
    sex = c2.radio("Select Sex", ('Female', 'Male'))
    program = c2.radio("Select College Program", programs)
    filtered_data = data_by_sex[data_by_sex.Sex == sex]

    # Create the Choropleth Map Chart
    states_map = alt.topo_feature(data.us_10m.url, 'states')
    chart = alt.Chart(states_map).mark_geoshape().encode(
        color=alt.Color(f"{program}:Q", legend=alt.Legend(title="")),
        tooltip=["State:N", alt.Tooltip(f"{program}:Q", title="Enrollment")],
    ).transform_lookup(
        lookup="id",
        from_=alt.LookupData(filtered_data, 'StateId', ["State", *programs])
    ).project(
        type="albersUsa"
    ).properties(
        height=500
    )

    # Add the Choropleth Map chart to the view
    c1.altair_chart(chart, use_container_width=True)
