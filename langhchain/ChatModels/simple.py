from langchain_community.llms import GPT4All

llm = GPT4All(
    model="/home/saif/saif/learning/langh/langhchain/ChatModels/models/ggml-gpt4all-j-v1.3-groovy.bin"
)

print(llm.invoke("Explain LangChain simply"))
