from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate
from langchain.messages import SystemMessage,HumanMessage,AIMessage
# import streamlit as st

# LLM
llm = OllamaLLM(model="mistral")

chat_history = [
    SystemMessage(content = "You are a AI helpful AI Assitant")
]
while True:
    user_input = input("enter the query:")

    if user_input == "exit":
        break
    chat_history.append(HumanMessage(content=user_input))
    res = llm.invoke(chat_history)
    chat_history.append(AIMessage(content=res))
    print("AI :",res)

print(chat_history)