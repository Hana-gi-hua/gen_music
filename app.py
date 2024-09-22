import os
from dotenv import load_dotenv
import streamlit as st
# import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain import PromptTemplate

# .envファイルの読み込み
load_dotenv()

## モデルの設定
# GOOGLE_API_KEY=os.getenv('GOOGLE_API_KEY')
# genai.configure(api_key=GOOGLE_API_KEY)

llm = ChatGoogleGenerativeAI(model="gemini-pro")

def get_response(input_prompt):
    # response = model.generate_content(prompt)
    template = """
    次の文章では画像と音楽のどちらを生成したいのかについて考えてください。
    {sentense_before_classification}
    """

    prompt = PromptTemplate(template=template, 
                            input_variables=['sentense_before_classification'])
    prompt_text = prompt.format(sentense_before_classification=input_prompt)
    response = llm.invoke(prompt_text)

    return response.content




## チャット機能
st.title('お試しチャットアプリ')

if 'messages' not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

input_prompt = st.chat_input('Say someting')

if input_prompt:
    st.chat_message('user').write(input_prompt)
    st.chat_message('ai').write(get_response(input_prompt))

    st.session_state.messages.append({'role': 'user', 'content': input_prompt})
    st.session_state.messages.append({'role': 'ai', 'content': get_response(input_prompt)})
    
