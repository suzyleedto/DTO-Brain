from pathlib import Path

import streamlit as st

st.set_page_config(
    page_title="DTO Toolkit Home",
    page_icon="🛠️",
    layout="wide",
    initial_sidebar_state="expanded"
)

from st_pages import Page, add_page_title, show_pages

add_page_title()
show_pages(
        [
            Page("main_app.py","DTO Toolbox Home","🏠"),
            # Can use :<icon-name>: or the actual icon
            Page("apps/prob_statement.py", "Problem Statement Generator","✏️"),
            # The pages appear in the order you pass them
            Page("apps/scamper.py", "Brainstorming Buddy using SCAMPER","💡"),
            # The pages appear in the order you pass them
            Page("apps/proto_persona.py","Proto-Persona Creator","🧑‍🤝‍🧑"),
            # The pages appear in the order you pass them
            
        ]
    )


st.page_link("main_app.py", label="Home", icon="🏠")
st.page_link("apps/prob_statement.py", label="Problem Statement Generator", icon="✏️")
st.page_link("apps/scamper.py", label = "Brainstorming Buddy using SCAMPER", icon="💡")
st.page_link("apps/proto_persona.py", label = "Proto-Persona Creator", icon  = "🧑‍🤝‍🧑")
