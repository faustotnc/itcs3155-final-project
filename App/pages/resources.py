import streamlit as st
from helpers import add_space


def display_page():
    _, c1, _ = st.columns([0.5, 3, 0.5])
    c1.header("UniStats Dashboard")
    c1.write("Empowering Equality in Higher Education.")
    add_space(25, col=c1)
    c1.write("The data used in this project is publicly available at this URL:")
    c1.write(
        "https://www.kaggle.com/datasets/tjkyner/bachelor-degree-majors-by-age-sex-and-state")
    add_space(25, col=c1)
    c1.write("Visit https://university.graduateshotline.com/ubystate.html to access the contact "
             "information of universities in the U.S. by state.")
    c1.write("---")
    c1.subheader("Contact Us")
    c1.markdown("University of North Carolina at Charlotte")
    c1.markdown("**Address:** 9201 University City Blvd, Charlotte, NC 28223")
    c1.markdown("**Support:** support@unistats.com")
    c1.markdown("**Phone:** 984-242-7790")
