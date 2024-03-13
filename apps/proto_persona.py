 # Importing required packages
import streamlit as st
import openai
import uuid
import time
import pandas as pd
import io
from openai import OpenAI

st.set_page_config(
    page_title="Proto Persona Creator",
    page_icon="🧑‍🤝‍🧑",
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
    
    

col1, col2, col3= st.columns(3)

with col1:
    st.subheader("Audience:")
    txt_who = st.text_area(label = "Describe your audience/customers",placeholder="Grocery shoppers")
   

with col2:
   st.subheader("Product")
   txt_what = st.text_area(label = "Write a short description of the product, service or business who caters to the proto-personas", placeholder="E-commerce Grocery App")

with col3:
   st.subheader("Assumptions and Constraints")
   txt_limits = st.text_area(label = "What do you already know? (ie do you have information on customer demographics, do you have constraints?)", placeholder="personas must have monthly income less than P100,000 and male")

     


if st.button("Generate Proto-personas"):
    with st.status("Starting work...", expanded=False) as status_box:    
        # Initialize OpenAI assistant

        if "assistant" not in st.session_state:
            openai.api_key = st.secrets["OPENAI_API_KEY"]
            st.session_state.assistant = openai.beta.assistants.retrieve(st.secrets["OPENAI_ASSISTANT_PROTO"])

            st.session_state.thread = client.beta.threads.create(
                metadata={'session_id': st.session_state.session_id}
            )    
        prompt = "Create proto personas for _Target Audience_: "+txt_who +" and _Product_: "+ txt_what +" with these _Assumptions_"+txt_limits
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
        