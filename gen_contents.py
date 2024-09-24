import os
from dotenv import load_dotenv

from langchain.tools import Tool
from langchain.agents import initialize_agent, Tool
from openai import OpenAI

load_dotenv()
open_api_key = os.environ['OPENAI_API_KEY']
client  = OpenAI()

def generate_image(input_prompt):
    response = client.images.generate(
        model='dall-e-3',
        prompt=input_prompt,
        size='1024x1024',
        quality='standard',
        n=1,
    )
    return response.data[0].url

