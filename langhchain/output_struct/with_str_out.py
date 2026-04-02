from langchain_ollama import ChatOllama
from typing import TypedDict

chat = ChatOllama(
    model="mistral",
    temperature=0
)



class Review(TypedDict):
    summary:str
    sentiment:str

structed_model = chat.with_structured_output(Review)

res = structed_model.invoke("The hardware is great, but the software feels bloated. There are too many pre-installed apps that I can't remove. Also, the UI looks outdated compared to other brands. Hoping for a software update to fix this.")

print(res)