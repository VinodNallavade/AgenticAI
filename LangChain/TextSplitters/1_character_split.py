from langchain_text_splitters import CharacterTextSplitter
from langchain_community.document_loaders import  
from azure.identity import DefaultAzureCredential,get_bearer_token_provider
from langchain_openai import AzureChatOpenAI




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

docs= Py



messages = [
    (
        "system",
        "You are a helpful assistant that translates English to French. Translate the user sentence.",
    ),
    ("human", "I like programming."),
]

ai_msg = model.invoke(messages)
print(ai_msg.content)






