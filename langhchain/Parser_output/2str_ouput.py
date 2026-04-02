from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm = OllamaLLM(model="mistral")

report_prompt = PromptTemplate(
    template="Write a detailed report on {topic}",
    input_variables=["topic"]
)

summary_prompt = PromptTemplate(
    template="Summarize the following text in 5 lines:\n{text}",
    input_variables=["text"]
)

parser = StrOutputParser()
chain = report_prompt | llm |parser | summary_prompt | llm |parser
result = chain.invoke({'topic':'black hole'})
print(result)
