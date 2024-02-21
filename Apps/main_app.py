from pathlib import Path

import streamlit as st

from st_pages import Page, add_page_title, show_pages

"## Declaring the pages in your app:"

show_pages(
        [
            Page("Apps/main_app.py", "Home", "🏠"),
            # Can use :<icon-name>: or the actual icon
            Page("Apps/prob_statement.py", "Problem Statement", "✏️"),
            # The pages appear in the order you pass them
        ]
    )

add_page_title("Welcome to your DTO Toolbox")  # Optional method to add title and icon to current page
