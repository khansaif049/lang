# from langchain_community.llms import Ollama
from langchain_ollama import OllamaLLM

llm = OllamaLLM(model="mistral")

res = llm.invoke("Explain LangChain simply")
print(res)
