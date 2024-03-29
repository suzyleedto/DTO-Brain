 # Importing required packages
import streamlit as st
import openai
import uuid
import time
import pandas as pd
import io
from openai import OpenAI

st.set_page_config(
    page_title="Problem Statement Generator",
    page_icon="✏️",
    layout="wide",
    initial_sidebar_state="expanded"
)


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
    
col1, col2 = st.columns(2)

with col1:
    st.subheader("Target Audience:")
    txt_who = st.text_area(label = "Whose problem are you trying to solve?",placeholder="Grocery shoppers")
   

with col2:
   st.subheader("Problem")
   txt_what = st.text_area(label = "Write a short description of the problem", placeholder="Find the best deals in online groceries")
   


if st.button("Generate Problem Statement"):
    
    with st.status("Starting work...", expanded=False) as status_box:
    # Initialize OpenAI assistant
        if "assistant" not in st.session_state:
            openai.api_key = st.secrets["OPENAI_API_KEY"]
            st.session_state.assistant = openai.beta.assistants.retrieve(st.secrets["OPENAI_ASSISTANT"])

            st.session_state.thread = client.beta.threads.create(
                metadata={'session_id': st.session_state.session_id}
            )    
        prompt = "Create How Might We Statements for Target Audience: "+txt_who +" and Problem: "+ txt_what
        message_data = {
            "thread_id": st.session_state.thread.id,
            "role": "user",
            "content": prompt
        }

        st.session_state.messages = client.beta.threads.messages.create(**message_data)
        
        st.session_state.run = client.beta.threads.runs.create(
            thread_id=st.session_state.thread.id,
            assistant_id=st.session_state.assistant.id,
        )

            
        while st.session_state.run.status != 'completed':
            status_box.update(label=f"{st.session_state.run.status}...", state="running")
            st.session_state.run = openai.beta.threads.runs.retrieve(
            thread_id=st.session_state.thread.id,
            run_id=st.session_state.run.id
        )
        print(st.session_state.run.status)
        
        thread_messages = client.beta.threads.messages.list(st.session_state.thread.id)
    
        status_box.update(label="Complete", state="complete", expanded=True)
        for thread_message in thread_messages:
    
            message_text = thread_message.content[0].text.value
            st.markdown(message_text)
            st.markdown("\n===========================\n")
            #st.markdown(message_text)
        
