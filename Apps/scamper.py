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
    
    
st.set_page_config(page_title="Brainwriting Assistant (SCAMPER)")

with st.container():

    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("Target Audience:")
        txt_who = st.text_area(label = "Whose problem are you trying to solve?",placeholder="Grocery shoppers")

    with col2:
        st.subheader("Problem")
        txt_what = st.text_area(label = "Write a short description of the problem", placeholder="Find the best deals in online groceries")
    
    with col3:
        st.subheader("Product")
        txt_where = st.text_area(label = "What product/service do you currently have or are planning to build?", placeholder="E-commerce Grocery Website")
    



if st.button("Generate Ideas using SCAMPER"):
    tabS, tabC, tabA = st.tabs(["Substitute", "Combine", "Adapt"])
    # Initialize OpenAI assistant
    with tabS:
        with tabC:
            status_c = st.status("Queued", expanded=False)
        with st.status("Starting work...", expanded=False) as status_box:
            if "assistant" not in st.session_state:
                openai.api_key = st.secrets["OPENAI_API_KEY"]
                st.session_state.assistant = openai.beta.assistants.retrieve(st.secrets["OPENAI_ASSISTANT_SCAMPER_S"])

                st.session_state.thread = client.beta.threads.create(
                    metadata={'session_id': st.session_state.session_id}
                )    
            prompt = "Generate Ideas for this: \""""+txt_who +"\""" and Problem: \""""+ txt_what + " and Product: \""""+ txt_where+ "\""""
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
                time.sleep(5)
                status_box.update(label=f"{st.session_state.run.status}...", state="running")
                st.session_state.run = openai.beta.threads.runs.retrieve(
                thread_id=st.session_state.thread.id,
                run_id=st.session_state.run.id
            )
            print(st.session_state.run.status)
            status_box.update(label="Complete", state="complete", expanded=True)
            thread_messages = client.beta.threads.messages.list(st.session_state.thread.id)
            message_text = thread_messages.data[0].content[0].text.value
            st.markdown("### S-Substitute\n")
            st.markdown("#### _The substitute technique tends to provide alternative solutions for decision-makers to choose different solutions in order to reach the final action._\n")
            st.markdown(message_text)
            st.markdown("\n===========================\n")
            #st.markdown(message_text)
          
    with tabC:
            status_c.update(label ="Starting work...", expanded=False, state = "running")
            if "assistant" not in st.session_state:
                openai.api_key = st.secrets["OPENAI_API_KEY"]
                st.session_state.assistant = openai.beta.assistants.retrieve(st.secrets["OPENAI_ASSISTANT_SCAMPER_C"])

                st.session_state.thread = client.beta.threads.create(
                    metadata={'session_id': st.session_state.session_id}
                )    
            prompt = "Generate Ideas for this: \""""+txt_who +"\""" and Problem: \""""+ txt_what + " and Product: \""""+ txt_where+ "\""""
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
                time.sleep(5)
                status_box.update(label=f"{st.session_state.run.status}...", state="running")
                st.session_state.run = openai.beta.threads.runs.retrieve(
                thread_id=st.session_state.thread.id,
                run_id=st.session_state.run.id
            )
            print(st.session_state.run.status)
            status_box.update(label="Complete", state="complete", expanded=True)
            thread_messages = client.beta.threads.messages.list(st.session_state.thread.id)
            message_text = thread_messages.data[0].content[0].text.value
            st.markdown("### C-Combine\n")
            st.markdown("#### _The combined technique tends to analyze the possibility of merging two or more ideas, stages of the process or product in one single more efficient output._\n")
            st.markdown(message_text)
            st.markdown("\n===========================\n")
            #st.markdown(message_text)
        
        