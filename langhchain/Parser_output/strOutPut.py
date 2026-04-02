from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate

llm = OllamaLLM(model="mistral")

report_prompt = PromptTemplate(
    template="Write a detailed report on {topic}",
    input_variables=["topic"]
)

summary_prompt = PromptTemplate(
    template="Summarize the following text in 5 lines:\n{text}",
    input_variables=["text"]
)

report = llm.invoke(report_prompt.format(topic="black hole"))
summary = llm.invoke(summary_prompt.format(text=report))

# print("REPORT:\n", report)
print("\nSUMMARY:\n", summary)
