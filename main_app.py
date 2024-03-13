from pathlib import Path

import streamlit as st

from st_pages import Page, add_page_title, show_pages


show_pages(
        [
            Page(path="main_app.py", name = "DTO Toolbox Home"),
            # Can use :<icon-name>: or the actual icon
            Page(path="pages/prob_statement.py", name="Problem Statement Generator"),
            # The pages appear in the order you pass them
            Page(path="pages/scamper.py", name="Brainstorming Buddy using SCAMPER"),
            # The pages appear in the order you pass them
            Page(path = "pages/proto_persona.py", name = "Proto-Persona Creator")
            # The pages appear in the order you pass them
            
        ]
    )

add_page_title("Welcome to your DTO Toolbox")  # Optional method to add title and icon to current page
st.page_link("main_app.py", label="Home", icon="🏠")
st.page_link("pages/prob_statement.py", label="Problem Statement Generator", icon="✏️")
st.page_link("pages/scamper.py", label = "Brainstorming Buddy using SCAMPER", icon="💡")
st.page_link("pages/proto_persona.py", label = "Proto-Persona Creator", icon  = "🧑‍🤝‍🧑")
