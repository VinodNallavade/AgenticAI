from langchain_text_splitters import CharacterTextSplitter,RecursiveCharacterTextSplitter
from langchain_community.document_loaders import  AzureBlobStorageContainerLoader
from azure.identity import DefaultAzureCredential,get_bearer_token_provider
from langchain_openai import AzureChatOpenAI
import os
from dotenv import load_dotenv

load_dotenv()
azureblobconn= os.getenv("AzureSTG_CONN")

token_provider= get_bearer_token_provider(DefaultAzureCredential(),"https://cognitiveservices.azure.com/.default")
model= AzureChatOpenAI(
    api_version="2024-12-01-preview",
    azure_endpoint="https://azopenai-langchain.openai.azure.com/",
    azure_ad_token_provider= token_provider,
    azure_deployment= "gpt-4o-mini",
    model= "gpt-4o-mini",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2
)


# Text Load
docs= AzureBlobStorageContainerLoader(conn_str= azureblobconn,container="ailearn")
datafromblob = docs.load()

# chunk data

sample_text = """
LangChain is a framework for developing applications powered by language models. 
It enables developers to chain together different components such as prompts, models, and memory.
This helps in building robust LLM-powered apps like chatbots, RAG systems, and more.
"""

char_splitter = CharacterTextSplitter(
    separator="\n",
    chunk_size=50,
    chunk_overlap=10
)

char_chunks = char_splitter.split_text(sample_text)
print("Character Splitter Output:")
for i, chunk in enumerate(char_chunks):
    print(f"\nChunk {i+1}:\n{chunk}")


print("******************************* RecursiveCharacterTextSplitter ***********************")
recursive_splitter = RecursiveCharacterTextSplitter(
    chunk_size=50,
    chunk_overlap=10,
    separators=["\n\n", "\n", ".", " ", ""]
)

recursive_chunks = recursive_splitter.split_text(sample_text)
print("\nRecursive Splitter Output:")
for i, chunk in enumerate(recursive_chunks):
    print(f"\nChunk {i+1}:\n{chunk}")


## Learning is Chracter does not respect the chunk size. It split based on the seperator we give, default is \n\n
## Recursive respect the chunk size and it will split the given data within the size, if the seperator is given it will take that seperator as priority and ignore the chunk size,
## if seperator is not given then it will take the default ones or is default ones are used as seperator then it respect the chunk size

messages = [
    (
        "system",
        "You are a helpful assistant that translates English to French. Translate the user sentence.",
    ),
    ("human", "I like programming."),
]

#ai_msg = model.invoke(messages)
#print(ai_msg.content)






