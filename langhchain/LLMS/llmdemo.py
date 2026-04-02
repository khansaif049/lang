from langchain_openai import OpenAI
# from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

llm = OpenAI(model='gpt-4o-mini')

result = llm.invoke("what is capital of maharastra")

print(result,"getting_result")
