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
    

def render_message(message):
    with st.chat_message(message["role"]):
        if message['role'] == 'ai':
            if message['content']['type'] == 'image':
                # キャッシュデータがある場合、これを使って表示
                st.image(message['content']['data'])
            else:
                # URLがある場合、URLから画像を表示
                st.write(message["content"]['data'])
        else:
            st.write(message["content"]['data'])

def main():
    ## チャット機能
    st.title('お試しチャットアプリ')

    if 'messages' not in st.session_state:
        st.session_state.messages = []

    ## チャット履歴表示
    for message in st.session_state.messages:
        render_message(message)


    ## 各会話
    input_prompt = st.chat_input('Say someting')

    if input_prompt:
        # ユーザーのメッセージをセッションステートに追加
        user_message = {
            'role': 'user',
            'content': {
                'type': 'text',
                'url': '',
                'data': input_prompt,
            }
        }
        st.session_state.messages.append(user_message)

        # ユーザーのメッセージを即座にレンダリング
        render_message(user_message)


        # AIの応答を取得
        response = task_allocator(input_prompt)
        print(response)

        if validators.url(response):  # 画像URLの場合
            img_data = fetch_image(response)  # 画像を取得
            ai_message = {
                'role': 'ai',
                'content': {
                    'type': 'image',
                    'url': response,
                    'data': img_data  # キャッシュされた画像データ
                }
            }
            st.session_state.messages.append(ai_message)
        else:  # テキストの場合
            ai_message = {
                'role': 'ai',
                'content': {
                    'type': 'text',
                    'url': '',
                    'data': response,
                }
            }
            st.session_state.messages.append(ai_message)

        # AIの応答を即座にレンダリング
        render_message(ai_message)


        
if __name__ == '__main__':
    main()