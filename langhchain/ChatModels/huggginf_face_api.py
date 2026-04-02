from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from dotenv import load_dotenv
import os

load_dotenv()

print("TOKEN:", os.getenv("HUGGINGFACEHUB_API_TOKEN"))  # None nahi hona chahiye

llm = HuggingFaceEndpoint(
    repo_id="HuggingFaceH4/zephyr-7b-beta",
)

chat = ChatHuggingFace(llm=llm)

res = chat.invoke("What is the capital of India?")
print(res)
