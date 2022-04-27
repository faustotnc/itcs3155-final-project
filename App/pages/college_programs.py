import streamlit as st
from helpers import add_space
import altair as alt


def show_barchart(source):
    """
    The function for the barchart section.
    """

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
        tooltip=["State", alt.Tooltip(
            'sum(Bachelors Degree Holders)', title="Enrolled Students", format=",")]
    ).interactive().properties(
        height=500
    )

    # Add the barchart to the view
    c1.altair_chart(chart, use_container_width=True)


def show_stacked_barchart(source, program):
    """
        The function for the Stacked Barchart section.
    """

    # The title for the rest of the bar charts
    _, c1, _ = st.columns([0.5, 3, 0.5])
    c1.subheader("Enrollment by State, Sex, & Age (Specific Programs)")
    c1.write("This stacked bar chart can be filtered by your desired college program. It displays the number of students enrolled "
             "in each state for the program you select for both males and females. Each state is split up into four different age groups. ")
    program = c1.selectbox('Select a Degree Program', program)
    add_space(25)

    selected_chart = alt.Chart(source).mark_bar().encode(
        column='Sex',
        x=f'sum({program})',
        y='Age Group',
        color='State',
        # charts can also have tooltips when users hover
        tooltip=["State", alt.Tooltip(
            f'sum({program})', title="Enrolled Students", format=",")],
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


def display_page(source, program):
    show_barchart(source)
    show_stacked_barchart(source, program)
