import os
from dotenv import load_dotenv
import streamlit as st
import google.generativeai as genai


# .envファイルの読み込み
load_dotenv()

## モデルの設定
GOOGLE_API_KEY=os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-pro")


## チャット機能
st.title('お試しチャットアプリ')

if 'messages' not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input('Say someting')

if prompt:
    st.chat_message('user').write(prompt)
    response = model.generate_content(prompt)
    st.chat_message('ai').write(response.text)

    st.session_state.messages.append({'role': 'user', 'content': prompt})
    st.session_state.messages.append({'role': 'ai', 'content': response.text})
    
