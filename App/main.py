import streamlit as st
import altair as alt
from vega_datasets import data
import pandas as pd

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

    _, c1, _ = st.columns([0.5, 3, 0.5])
    c1.title("UniStats Dashboard")
    c1.write("Empowering Equality in Higher Education.")


def show_choropleth_map():
    """
    The function for the Choropleth Map section.
    """

    # The title for this section
    _, c1, _ = st.columns([0.5, 3, 0.5])
    c1.subheader("Enrollment by State, Sex, and College Program")
    add_space(24)

    # The columns for the chart and radio buttons
    _, c1, c2, _ = st.columns([0.5, 2, 1, 0.5])

    # The radio buttons and data filtering
    add_space(48, col=c2)
    sex = c2.radio("Select Sex", ('Female', 'Male'))
    program = c2.radio("Select College Program", PROGRAMS)
    filtered_data = DATA_BY_SEX[DATA_BY_SEX.Sex == sex]

    # Create the Choropleth Map Chart
    states_map = alt.topo_feature(data.us_10m.url, 'states')
    chart = alt.Chart(states_map).mark_geoshape().encode(
        color=alt.Color(f"{program}:Q", legend=alt.Legend(title="")),
        tooltip=["State:N", alt.Tooltip(f"{program}:Q", title="Enrollment")],
    ).transform_lookup(
        lookup="id",
        from_=alt.LookupData(filtered_data, 'StateId', ["State", *PROGRAMS])
    ).project(
        type="albersUsa"
    ).properties(
        height=500
    )

    # Add the Choropleth Map chart to the view
    c1.altair_chart(chart, use_container_width=True)

def show_barchart():
    """
    The function for the barchart section.
    """
    source = DATA

    # The title for this section
    _, c1, _ = st.columns([0.5, 3, 0.5])
    c1.subheader("Enrollment of Sex by State and College Program")
    c1.write(
        "This stacked bar chart displays the number of males and females enrolled in Bachelors Degree programs "
        "for each state in America. Hovering over a section of a bar displays the specific number of females or males "
        "that are enrolled in a program for that particular state.")

    # Create the Barchart
    chart = alt.Chart(source).mark_bar().encode(
        x='State',
        y='sum(Bachelors Degree Holders)',
        color='Sex',
        # charts can also have tooltips when users hover
        tooltip=["State", 'sum(Bachelors Degree Holders)']
    ).interactive().properties(
        height=500
    )

    # Add the Choropleth Map chart to the view
    c1.altair_chart(chart, use_container_width=True)


def show_stacked_barchart():
    """
        The function for the Stacked Barchart section.
    """

    # The title for this section
    _, _, c2, _ = st.columns([0.5, 2, 2, 0.1])
    c2.subheader("Total Enrollment by State & Sex")
    add_space(24)

    source = DATA

    bachelor_chart = alt.Chart(source).mark_bar().encode(
        x='sum(Bachelors Degree Holders)',
        y='Sex',
        color='State',
        # charts can also have tooltips when users hover
        tooltip=["State", alt.Tooltip(
            'sum(Bachelors Degree Holders)', title="Degree Holders")],
        order=alt.Order(
            # Sort the segments of the bars by this field
            'State',
            sort='ascending'
        ),
    ).interactive().properties(
        height=200, width=1200)

    _, c1, c2, _ = st.columns([0.5, 1, 2, 0.1])
    c1.write("This stacked barchart displays the varying distribution of Bachelors Degree holders from several different states. "
             "There are two bars which divide the total number of degree holders by their sex. "
             "Here we see that the state of California has the largest number of female degree holders, "
             "by hovering over the chart we can see that there are over 9.7 million females that received "
             "their degrees in Cali where as only 9.1 million males did the same.")
    c2.altair_chart(bachelor_chart, use_container_width=True)
    add_space(32)

    # The title for the rest of the bar charts
    _, c1, _ = st.columns([0.5, 3, 0.5])
    c1.subheader("Enrollment by State, Sex, & Age (Specific Programs)")
    program = c1.selectbox('Select a Degree Program', PROGRAMS)
    add_space(25)

    selected_chart = alt.Chart(source).mark_bar().encode(
        column='Sex',
        x=f'sum({program})',
        y='Age Group',
        color='State',
        # charts can also have tooltips when users hover
        tooltip=["State", alt.Tooltip(
            f'sum({program})', title="Enrolled Students")],
        order=alt.Order(
            # Sort the segments of the bars by this field
            'State',
            sort='ascending'
        ),
    ).interactive().properties(
        height=200, width=1200)

    # Add the stacked barcharts to the view
    _, c1, c2, _ = st.columns([0.2, 1, 1, 0.5])
    c1.altair_chart(selected_chart, use_container_width=True)
    add_space(32, col=c2)


def show_scatter_plot():
    # The title for this section
    _, c1, _ = st.columns([0.5, 4, 0.5])
    c1.subheader(
        "Enrollment by Age, State, Sex, and College Program with Scatter Plot")
    add_space(24)

    # The columns for the chart and radio buttons
    _, c1, c2, _ = st.columns([0.5, 2, 1, 0.5])

    source = DATA
    science_engineering_chart = alt.Chart(source).mark_circle(size=60).encode(
        x='Science and Engineering',
        y='Age Group',
        color='Sex',
        tooltip=['State', 'Age Group', 'Sex']
    ).interactive()
    science_engineering_related_fields_chart = alt.Chart(source).mark_circle(size=60).encode(
        x='Science and Engineering Related Fields',
        y='Age Group',
        color='Sex',
        tooltip=['State', 'Age Group', 'Sex']
    ).interactive()
    business_chart = alt.Chart(source).mark_circle(size=60).encode(
        x='Business',
        y='Age Group',
        color='Sex',
        tooltip=['State', 'Age Group', 'Sex']
    ).interactive()
    education_chart = alt.Chart(source).mark_circle(size=60).encode(
        x='Education',
        y='Age Group',
        color='Sex',
        tooltip=['State', 'Age Group', 'Sex']
    ).interactive()
    art_humanities_others_chart = alt.Chart(source).mark_circle(size=60).encode(
        x='Arts, Humanities and Others',
        y='Age Group',
        color='Sex',
        tooltip=['State', 'Age Group', 'Sex']
    ).interactive()

    _, c1, c2, _ = st.columns([0.5, 2, 1, 0.5])
    c1.altair_chart(science_engineering_chart, use_container_width=True)
    c2.write(
        "These scatter plots display the varying distribution of enrollment from different age groups and sexes "
        "across several different states. "
        "Each scatter plot depicts information from a different program.")
    c1.altair_chart(science_engineering_related_fields_chart,
                    use_container_width=True)
    add_space(32, col=c2)
    c1.altair_chart(business_chart, use_container_width=True)
    add_space(32, col=c2)
    c1.altair_chart(education_chart, use_container_width=True)
    add_space(32, col=c2)
    c1.altair_chart(art_humanities_others_chart, use_container_width=True)
    add_space(32, col=c2)

def show_footer_section():
    _, c1, _ = st.columns([0.5, 3, 0.5])
    c1.write("---")
    c1.subheader("UniStats Dashboard")
    c1.write("Empowering Equality in Higher Education.")
    add_space(24, col=c1)
    c1.write("The data used in this project is publicly available at this URL: https://www.kaggle.com/datasets/tjkyner/bachelor-degree-majors-by-age-sex-and-state")
    c1.write("Visit https://university.graduateshotline.com/ubystate.html to access the contact information of universities in the U.S. by state.")


# Show the Header Section
show_header()

# Add Empty Space
add_space(64)

# The Choropleth Map
show_choropleth_map()

# The Barchart()
show_barchart()

# The Stacked Barchart
show_stacked_barchart()

# The Normalized Stacked Area Chart()
show_scatter_plot()

# Add Empty Space
add_space(64)

# Show the footer section
show_footer_section()
