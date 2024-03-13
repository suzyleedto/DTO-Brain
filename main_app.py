from pathlib import Path

import streamlit as st

from st_pages import Page, add_page_title, show_pages


show_pages(
        [
            Page("main_app.py","DTO Toolbox Home","🏠"),
            # Can use :<icon-name>: or the actual icon
            Page("pages/prob_statement.py", "Problem Statement Generator","✏️"),
            # The pages appear in the order you pass them
            Page("pages/scamper.py", "Brainstorming Buddy using SCAMPER","💡"),
            # The pages appear in the order you pass them
            Page("pages/proto_persona.py","Proto-Persona Creator","🧑‍🤝‍🧑"),
            # The pages appear in the order you pass them
            
        ]
    )


st.page_link("main_app.py", label="Home", icon="🏠")
st.page_link("pages/prob_statement.py", label="Problem Statement Generator", icon="✏️")
st.page_link("pages/scamper.py", label = "Brainstorming Buddy using SCAMPER", icon="💡")
st.page_link("pages/proto_persona.py", label = "Proto-Persona Creator", icon  = "🧑‍🤝‍🧑")
