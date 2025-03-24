import streamlit as st
from langchain.schema import Document
# for vectorising
from langchain.embeddings import SentenceTransformerEmbeddings
from google import genai
from google.genai import types
from dotenv import load_dotenv
import os

import PIL.Image

gemini_api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(
        api_key=gemini_api_key,
    )

model = "gemini-2.0-flash"

# Picture upload and analysis

uploaded_picture = st.file_uploader("Choose picture to discuss on", type=["jpg", "jpeg", "png"], accept_multiple_files=False)
if uploaded_picture is not None:
    st.image(uploaded_picture, caption="Jūsų įkelta nuotrauka diskusijai")

image = PIL.Image.open('/path/to/image.png')

# Chat processing

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("What is up?"):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Query the vector store
    prompt_content = query_vectorstore(st.session_state.vectorstore, prompt, k=5)
    if prompt_content:
        combined_content = " ".join([doc.page_content for doc in prompt_content])
    else:
        combined_content = "No relevant content found."

    # Add the combined content to the messages
    st.session_state.messages.append({"role": "system", "content": f"Search in the following content: {combined_content}"})

    full_response = client.chat.completions.create(
    messages=[
        {
            #  instruction/prompt engineering example - 1
            "role": "system",
            "content": "Always respond in Lithuanian language, even if asked in any other language"
        },
        {
            #  instruction/prompt engineering example - 2
            "role": "system",
            "content": "Pretend as you are a famous traveler. Be polite, helpful, informal. Answer with no more than 3 short sentences. Always add travel tips"
        },
        {
            #  instruction/prompt engineering example - 3
            "role": "assistant",
            "content": "Rephrase user question in the beginning of the answer and ask a related question on answer content at the end of the answer"
        },
        {
            "role": "user",
            "content": prompt,
        },
        {
            "role": "system",
            "content": f"Search in the following content: {combined_content}"
        }
    ],
    model="gpt-4o",
    max_tokens=4096,
)

    response = full_response.choices[0].message.content
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})