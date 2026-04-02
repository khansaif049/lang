from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import Literal
from langchain_core.runnables import RunnableParallel,RunnableBranch,RunnableLambda


model1 = OllamaLLM(model="mistral")

class FeedBack(BaseModel):
    sentiment: Literal['positive', 'negative', 'neutral'] = Field(
        description='Give the sentiment of the feedback'
    )
parser2 = PydanticOutputParser(pydantic_object=FeedBack)

prompt1 = PromptTemplate(
    template="""
Classify the sentiment of the following feedback.
Only respond in the specified format.

Feedback:
{feedback}

{format_instruction}
""",
    input_variables=['feedback'],
    partial_variables={
        'format_instruction': parser2.get_format_instructions()
    }
)

classifier_chain = prompt1 | model1 | parser2

prompt2 = PromptTemplate(
    template="Write a appropriate response to this postive feedback \n {feedback}",
    input_variables=['feedback']
)

prompt3 = PromptTemplate(
    template="Write a appropriate response to this nefative feedback \n {feedback}",
    input_variables=['feedback']
)

branch_chain = RunnableBranch(
    (lambda x: x.sentiment == 'positive', prompt2 | model1),
    (lambda x: x.sentiment == 'negative', prompt3 | model1),
    (lambda x: x.sentiment == 'neutral', prompt2 | model1),
    RunnableLambda(lambda x: "could not find sentiment")
)

# result = classifier_chain.invoke(
#     {"feedback": "This is leading phone"}
# )
final_chain = classifier_chain | branch_chain

result = final_chain.invoke(
    {'feedback': 'This is the worst phone'}
)

final_chain.get_graph().print_ascii()
print(result)
# print(final_chain.pr)