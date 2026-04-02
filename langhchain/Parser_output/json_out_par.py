from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser,JsonOutputParser


llm = OllamaLLM(model="mistral")
parser = JsonOutputParser()

template = PromptTemplate(
    template="Give me the name, age and city of a fictional Person\n {format_instruction}",
    input_variables=["topic"],
    partial_variables={'format_instruction':parser.get_format_instructions()}
)

prompt = template.format()

# print(prompt)
res = llm.invoke(prompt)
final = parser.parse(res)
print(final,type(final))


