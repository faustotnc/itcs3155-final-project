import streamlit as st
from helpers import add_space


def display_page():
    """
    The function for the header section.
    """

    _, c1, _ = st.columns([1, 3, 1])
    c1.title("UniStats Dashboard")
    c1.write("Empowering Equality in Higher Education.")
    add_space(64)
    c1.write("With so many universities in the United States and so many programs within those universities, "
             "it can be difficult to find which programs have the most support for women.  "
             "It can also be difficult to know which programs need more promotion and advertisement "
             "for underrepresented groups. There are certain programs that desperately need more female "
             "representation. Having a well-presented, interactive summary of how university programs are spread "
             "across the United States can be beneficial when making decisions about which educational programs "
             "need the most support from universities and the government in terms of equality and diversity.")
    add_space(64)
    c1.write("Our dashboard displays various visualizations that will help you find specific states and college programs that will foster a more "
             "supportive learning environment. Once you find a state that you would like to move to, there is a link in our resources page that "
             "will direct you to specific universities that are located in each state. ")
