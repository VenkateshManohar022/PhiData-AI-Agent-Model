from langchain_ollama import OllamaLLM
from langchain.prompts import PromptTemplate
from langchain.agents import tool
from langchain import hub
from dotenv import load_dotenv

load_dotenv()
import os


## Functions
@tool
def get_text_length(text:str) -> int:
    '''Return the length of the text by characters'''
    text=text.strip("'\n").strip('"') # stripping away non alphabetric characters just in case
    return len(text)


if __name__=='__main__':

    tools=[get_text_length]
    agent_prompt=hub.pull('hwchase16/react')
    
    

    llm = OllamaLLM(model="llama3")
    prompt_template = PromptTemplate(
        template="""
    Create a script for Marketing Agent, Which should be professional and E=Well readable when I sent this via Telegram API"""
    )

    chain = prompt_template | llm

    prompt = input("Enter the Marketing Scraped Details : ")
    print('The Length of the Text is : ',get_text_length.invoke(input={'text':prompt}))

    response = chain.invoke(input={"script": prompt})

    print("Marketing Script : ", response)


