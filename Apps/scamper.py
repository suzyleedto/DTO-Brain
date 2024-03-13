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
    
    
st.set_page_config(page_title="Brainstorming Buddy (SCAMPER)")

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
    tabS, tabC, tabA, tabM, tabP, tabE, tabR = st.tabs(["Substitute", "Combine", "Adapt","Modify","Put to another context","Eliminate","Reverse"])
    # Initialize OpenAI assistant
    with tabS:
        with tabC:
            status_c = st.status("Queued", expanded=False)
        with tabA:
            status_a = st.status("Queued", expanded=False)
        with tabM:
            status_m = st.status("Queued", expanded=False)
        with tabP:
            status_p = st.status("Queued", expanded=False)
        with tabE:
            status_e = st.status("Queued", expanded=False)
        with tabR:
            status_r = st.status("Queued", expanded=False)          
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
           #st.markdown(thread_messages+"\n")
            st.markdown("### S-Substitute\n")
            st.markdown("#### _The substitute technique tends to provide alternative solutions for decision-makers to choose different solutions in order to reach the final action._\n")
            st.markdown(message_text)
            st.markdown("\n===========================\n")
            #st.markdown(message_text)
          
    with tabC:
        status_c.update(label ="Starting work...", expanded=False, state = "running")
        
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
            assistant_id=st.session_state.assistant.id,            )

                
        while st.session_state.run.status != 'completed':
            time.sleep(5)
            status_c.update(label=f"{st.session_state.run.status}...", state="running")
            st.session_state.run = openai.beta.threads.runs.retrieve(
                thread_id=st.session_state.thread.id,
                run_id=st.session_state.run.id
            )
        print(st.session_state.run.status)
        status_c.update(label="Complete", state="complete", expanded=True)
        thread_messages = client.beta.threads.messages.list(st.session_state.thread.id)
        message_text = thread_messages.data[0].content[0].text.value
        st.markdown("### C-Combine\n")
        st.markdown("#### _The combined technique tends to analyze the possibility of merging two or more ideas, stages of the process or product in one single more efficient output._\n")
        st.markdown(message_text)
        st.markdown("\n===========================\n")
            #st.markdown(message_text)
    with tabA:
            status_a.update(label ="Starting work...", expanded=False, state = "running")
         
            openai.api_key = st.secrets["OPENAI_API_KEY"]
            st.session_state.assistant_A = openai.beta.assistants.retrieve(st.secrets["OPENAI_ASSISTANT_SCAMPER_A"])
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
                assistant_id=st.session_state.assistant.id,            )

                    
            while st.session_state.run.status != 'completed':
                time.sleep(5)
                status_a.update(label=f"{st.session_state.run.status}...", state="running")
                st.session_state.run = openai.beta.threads.runs.retrieve(
                    thread_id=st.session_state.thread.id,
                    run_id=st.session_state.run.id
                )
            print(st.session_state.run.status)
            status_a.update(label="Complete", state="complete", expanded=True)
            thread_messages = client.beta.threads.messages.list(st.session_state.thread.id)
            message_text = thread_messages.data[0].content[0].text.value
            st.markdown("### A-Adapt\n")
            st.markdown("#### _Adapt refers to a brainstorming discussion that aims to adjust or tweak product or service for a better output._\n")
            st.markdown(message_text)
            st.markdown("\n===========================\n")
                #st.markdown(message_text)       
    with tabM:
            status_m.update(label ="Starting work...", expanded=False, state = "running")
           
            openai.api_key = st.secrets["OPENAI_API_KEY"]
            st.session_state.assistant_M = openai.beta.assistants.retrieve(st.secrets["OPENAI_ASSISTANT_SCAMPER_M"])
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
                assistant_id=st.session_state.assistant.id,            )

                    
            while st.session_state.run.status != 'completed':
                time.sleep(5)
                status_m.update(label=f"{st.session_state.run.status}...", state="running")
                st.session_state.run = openai.beta.threads.runs.retrieve(
                    thread_id=st.session_state.thread.id,
                    run_id=st.session_state.run.id
                )
            print(st.session_state.run.status)
            status_m.update(label="Complete", state="complete", expanded=True)
            thread_messages = client.beta.threads.messages.list(st.session_state.thread.id)
            message_text = thread_messages.data[0].content[0].text.value
            st.markdown("### M-Modify\n")
            st.markdown("#### _The modify technique refers to changing the process in a way that unleashes more innovative capabilities or solves problems._\n")
            st.markdown(message_text)
            st.markdown("\n===========================\n")
                #st.markdown(message_text)                  
    with tabP:
            status_p.update(label ="Starting work...", expanded=False, state = "running")
            
            openai.api_key = st.secrets["OPENAI_API_KEY"]
            st.session_state.assistant_P = openai.beta.assistants.retrieve(st.secrets["OPENAI_ASSISTANT_SCAMPER_P"])
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
                assistant_id=st.session_state.assistant_P.id,            )

                    
            while st.session_state.run.status != 'completed':
                time.sleep(5)
                status_p.update(label=f"{st.session_state.run.status}...", state="running")
                st.session_state.run = openai.beta.threads.runs.retrieve(
                    thread_id=st.session_state.thread.id,
                    run_id=st.session_state.run.id
                )
            print(st.session_state.run.status)
            status_p.update(label="Complete", state="complete", expanded=True)
            thread_messages = client.beta.threads.messages.list(st.session_state.thread.id)
            message_text = thread_messages.data[0].content[0].text.value
            st.markdown("### P-Put to another context\n")
            st.markdown("#### _This technique concerns how to put the current product or process in another purpose or how to use the existing product to solve problems._\n")
            st.markdown(message_text)
            st.markdown("\n===========================\n")
                #st.markdown(message_text)  
    with tabE:
            status_e.update(label ="Starting work...", expanded=False, state = "running")
        
            openai.api_key = st.secrets["OPENAI_API_KEY"]
            st.session_state.assistant_E = openai.beta.assistants.retrieve(st.secrets["OPENAI_ASSISTANT_SCAMPER_E"])
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
                assistant_id=st.session_state.assistant.id,            )

                    
            while st.session_state.run.status != 'completed':
                time.sleep(5)
                status_e.update(label=f"{st.session_state.run.status}...", state="running")
                st.session_state.run = openai.beta.threads.runs.retrieve(
                    thread_id=st.session_state.thread.id,
                    run_id=st.session_state.run.id
                )
            print(st.session_state.run.status)
            status_e.update(label="Complete", state="complete", expanded=True)
            thread_messages = client.beta.threads.messages.list(st.session_state.thread.id)
            message_text = thread_messages.data[0].content[0].text.value
            st.markdown("### E-Eliminate\n")
            st.markdown("#### _This technique aims to identify the parts of the process that can be eliminated to improve the process product or service._\n")
            st.markdown(message_text)
            st.markdown("\n===========================\n")
                #st.markdown(message_text)  
    with tabR:
            status_r.update(label ="Starting work...", expanded=False, state = "running")
          
            openai.api_key = st.secrets["OPENAI_API_KEY"]
            st.session_state.assistant_R = openai.beta.assistants.retrieve(st.secrets["OPENAI_ASSISTANT_SCAMPER_R"])
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
                assistant_id=st.session_state.assistant.id,            )

                    
            while st.session_state.run.status != 'completed':
                time.sleep(5)
                status_r.update(label=f"{st.session_state.run.status}...", state="running")
                st.session_state.run = openai.beta.threads.runs.retrieve(
                    thread_id=st.session_state.thread.id,
                    run_id=st.session_state.run.id
                )
            print(st.session_state.run.status)
            status_r.update(label="Complete", state="complete", expanded=True)
            thread_messages = client.beta.threads.messages.list(st.session_state.thread.id)
            message_text = thread_messages.data[0].content[0].text.value
            st.markdown("### R-Reverse\n")
            st.markdown("#### _The reverse or rearrange technique aims to explore the innovative potential when changing the order of the process in the production line._\n")
            st.markdown(message_text)
            st.markdown("\n===========================\n")
                #st.markdown(message_text)  