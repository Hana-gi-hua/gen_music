import os
from dotenv import load_dotenv
import streamlit as st
# import google.generativeai as genai
from task_agent import *
from PIL import Image
import io
import requests
import validators

# .envファイルの読み込み
load_dotenv()

def main():
    ## チャット機能
    st.title('お試しチャットアプリ')

    if 'messages' not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    input_prompt = st.chat_input('Say someting')

    if input_prompt:
        with st.chat_message('user'):
            st.write(input_prompt)
            st.session_state.messages.append({'role': 'user', 'content': input_prompt})

        with st.chat_message('ai'):
            response = task_allocator(input_prompt)
            if validators.url(response):
                # image = Image.open(io.BytesIO(response))
                image = requests.get(response).content
                st.image(image)
            else:
                st.write(task_allocator(input_prompt))
            
            st.session_state.messages.append({'role': 'ai', 'content': task_allocator(input_prompt)})
        
if __name__ == '__main__':
    main()