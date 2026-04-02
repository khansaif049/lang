from langchain.messages import SystemMessage,HumanMessage,AIMessage
from langchain_ollama import OllamaLLM

llm = OllamaLLM(model="mistral")

messages = [
    SystemMessage(content = "You are a helpful Assistant"),
    HumanMessage(content="Tell me About Langchain")
]
res = llm.invoke(messages)

messages.append(AIMessage(content=res))

print(messages)