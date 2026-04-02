from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate
from langchain.messages import SystemMessage,HumanMessage,AIMessage
# import streamlit as st
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

model = OllamaLLM(model="mistral")

prompt = PromptTemplate(
    template="genrate 5 interesting facts about {topic}",
    input_variables=['topic']
)


parser = StrOutputParser()

chain = prompt | model | parser

result = chain.invoke({'topic':'football'})


print(result)

chain.get_graph().print_ascii()
