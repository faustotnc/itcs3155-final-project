import streamlit as st
from helpers import add_space
import altair as alt


def display_page(source):
    # The title for this section
    _, c1, _ = st.columns([0.5, 4, 0.5])
    c1.subheader(
        "Enrollment by Age, State, Sex, and College Program with Scatter Plot")
    add_space(24)

    # The columns for the chart and radio buttons
    _, c1, c2, _ = st.columns([0.5, 2, 1, 0.5])

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
        "These scatter plots display the varying distributions of enrollment from different age groups and sexes "
        "across several different states. "
        "Each scatter plot depicts information from a different college program. "
        "Hovering over each data point displays information about the state, age group, and sex.")
    c1.altair_chart(science_engineering_related_fields_chart,
                    use_container_width=True)
    add_space(32, col=c2)
    c1.altair_chart(business_chart, use_container_width=True)
    add_space(32, col=c2)
    c1.altair_chart(education_chart, use_container_width=True)
    add_space(32, col=c2)
    c1.altair_chart(art_humanities_others_chart, use_container_width=True)
    add_space(32, col=c2)
