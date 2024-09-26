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

@st.cache_data
def fetch_image(img_url):
    img = requests.get(img_url).content
    return img

def display_image(img_url):
    img = fetch_image(img_url)
    if img is not None:
        st.image(img)
        return img
    else:
        st.error("Failed to display image.")
        return None

def main():
    ## チャット機能
    st.title('お試しチャットアプリ')

    if 'messages' not in st.session_state:
        st.session_state.messages = []

    ## チャット履歴表示
    for message in st.session_state.messages:
        if message['role'] == 'ai' and message['content']['type'] == 'image':
            with st.chat_message(message["role"]):
                if 'data' in message['content']:
                    # キャッシュデータがある場合、これを使って表示
                    st.image(message['content']['data'])
                else:
                    # URLがある場合、URLから画像を表示
                    st.image(message['content']['url'])
        else:
            with st.chat_message(message["role"]):
                st.write(message["content"]['data'])


    ## 各会話
    input_prompt = st.chat_input('Say someting')

    if input_prompt:
        with st.chat_message('user'):
            st.write(input_prompt)
            st.session_state.messages.append({'role': 'user', 
                                              'content': {
                                                            'type': 'text',
                                                            'url': '',
                                                            'data': input_prompt,
                                                        }})

        with st.chat_message('ai'):
            response = task_allocator(input_prompt)
            print(response)

            if validators.url(response):#このresponseは画像URL
                img_data = display_image(response)
                st.session_state.messages.append({'role': 'ai', 
                                                  'content': {
                                                            'type': 'image',
                                                            'url': response,
                                                            'data': img_data  # キャッシュされた画像データ
                                                        }})
            else:
                st.write(response)
                st.session_state.messages.append({'role': 'ai', 
                                                  'content': {
                                                            'type': 'text',
                                                            'url': '',
                                                            'data': response,
                                                        } })
        
if __name__ == '__main__':
    main()