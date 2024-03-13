from pathlib import Path

import streamlit as st

from st_pages import Page, add_page_title, show_pages


show_pages(
        [
            Page("Apps/main_app.py", "DTO Toolbox Home", "🛠️"),
            # Can use :<icon-name>: or the actual icon
            Page("Apps/prob_statement.py", "Problem Statement Generator", "✏️"),
            # The pages appear in the order you pass them
            Page("Apps/scamper.py", "Brainstorming Buddy using SCAMPER", "💡")
            # The pages appear in the order you pass them
        ]
    )

add_page_title("Welcome to your DTO Toolbox")  # Optional method to add title and icon to current page
st.page_link("Apps/main_app.py", label="Home", icon="🏠")
st.page_link("Apps/prob_statement.py", label="Problem Statement Generator", icon="✏️",disabled=True)
st.page_link("Apps/scamper.py", label = "Brainstorming Buddy using SCAMPER", icon="💡", disabled=True)
