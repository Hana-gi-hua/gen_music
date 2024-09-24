from langchain.agents import AgentExecutor
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from gen_contents import *

llm = ChatGoogleGenerativeAI(model="gemini-pro")

def get_intent_classification(input_prompt):
    template = """
    {sentense_before_classification}
    上記の文章から画像生成または音楽生成の意図を汲み取る場合は以下の選択肢から選んでください:
    1. 画像生成
    2. 音楽生成
    3. 会話を続ける
    回答は "画像生成", "音楽生成", または "会話" のいずれかにしてください。
    """

    prompt = PromptTemplate(template=template, 
                            input_variables=['sentense_before_classification'])
    prompt_text = prompt.format(sentense_before_classification=input_prompt)
    response = llm.invoke(prompt_text)
    return response.content.strip()


def task_allocator(input_prompt):
    intent = get_intent_classification(input_prompt)

    if intent == '画像生成':
        return generate_image(input_prompt)
    elif intent == '音楽生成':
        return "music"
    elif intent == '会話':
        return llm.invoke(input_prompt).content
    
