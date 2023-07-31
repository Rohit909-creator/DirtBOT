import streamlit as st
import random
import time
import openai
import os
# print(st.__version__)
openai.api_key = os.getenv("OPEN_AI_API_KEY")
st.title("Dirt Chat")



# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


prompt = st.chat_input()
if prompt:
    with st.chat_message("user"):
        st.markdown(prompt)
    
    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {
        "role": "system",
        "content": "You are bot who talks dirty, try to seduce the person who talks to you. You should make the user feel like you are taking the person to bed and seducing them in a really naughty and dirty way. Tell them what you guys are doing to each other and what all positions you are doing them."
        },
        {
        "role": "user",
        "content": f"{prompt}"
        }
    ],
    temperature=0.7,
    max_tokens=256,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
    )


    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        assistant_response = response['choices'][0]['message']['content']
        # Simulate stream of response with milliseconds delay
        for chunk in assistant_response.split():
            full_response += chunk + " "
            time.sleep(0.05)
            # Add a blinking cursor to simulate typing
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})
