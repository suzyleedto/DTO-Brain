 # Importing required packages
import streamlit as st
import openai
import uuid
import time
import pandas as pd
import io
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI()

# Your chosen model
#MODEL = "gpt-3.5-turbo-16k" # Legacy
MODEL = "gpt-4-turbo-preview" # Latest model
#MODEL = "gpt-4-1106-preview"

# Initialize session state variables
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "run" not in st.session_state:
    st.session_state.run = {"status": None}

if "messages" not in st.session_state:
    st.session_state.messages = []

if "retry_error" not in st.session_state:
    st.session_state.retry_error = 0
    
    
st.set_page_config(page_title="Problem Statement here")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Target Audience:")
    txt_who = st.text_area(label = "Whose problem are you trying to solve?",placeholder="Grocery shoppers")
   

with col2:
   st.subheader("Problem")
   txt_what = st.text_area(label = "Write a short description of the problem", placeholder="Find the best deals in online groceries")
   
st.button("Generate Problem Statement")