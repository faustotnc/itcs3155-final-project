import streamlit as st
import altair as alt
from vega_datasets import data

st.set_page_config(page_title="UniStats", layout="wide")


def add_space(size, col=None):
    """
    Adds vertical space between two sections.
    """

    (col if col else st).markdown(
        body=f"<div style='margin-top: {size}px'></div>",
        unsafe_allow_html=True
    )


def show_header():
    """
    The function for the header section.
    """

    _, c1, _ = st.columns([0.75, 2.5, 0.75])
    c1.title("UniStats Dashboard")
    c1.write("Empowering Equality in Higher Education.")


def show_choropleth_map():
    """
    The function for the Choropleth Map section.
    """

    _, c1, c2, _ = st.columns([0.75, 2, 0.5, 0.75])
    c1.subheader("College Program Enrollment by State and Gender")
    add_space(24)

    # Create the Choropleth Map Chart
    counties = alt.topo_feature(data.us_10m.url, 'states')
    source = data.population_engineers_hurricanes.url
    chart = alt.Chart(counties).mark_geoshape().encode(
        color='population:Q'
    ).transform_lookup(
        lookup='id',
        from_=alt.LookupData(source, 'id', ['population'])
    ).project(
        type='albersUsa'
    ).properties(
        width=500,
        height=500
    )

    # Add the Choropleth Map chart to the view
    _, c1, c2, _ = st.columns([0.75, 2, 0.5, 0.75])
    c1.altair_chart(chart, use_container_width=True)
    add_space(32, col=c2)
    c2.write("Select Gender")


def show_stacked_barchart():
    _, c3, c4, _ = st.columns([0.75, 2, 0.5, 0.75])
    c3.subheader("Enrollment by State and Gender")
    add_space(24)

    source = data.barley()
    chart = alt.Chart(source).mark_bar().encode(
        x='sum(yield)',
        y='variety',
        color='site',
        order=alt.Order(
            # Sort the segments of the bars by this field
            'site',
            sort='ascending'
        )
    )

    # Add the stacked barchart to the view
    _, c3, c4, _ = st.columns([0.75, 2, 0.5, 0.75])
    c3.altair_chart(chart, use_container_width=True)
    add_space(32, col=c4)
    c4.write("Description")


# Show the Header Section
show_header()

# Add Empty Space
add_space(64)

# The Choropleth Map
show_choropleth_map()

# The Stacked Barchart
show_stacked_barchart()
