

from langchain_openai import AzureOpenAIEmbeddings
from azure.identity import DefaultAzureCredential,get_bearer_token_provider

token_provider= get_bearer_token_provider(DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default")



model= AzureOpenAIEmbeddings(
    api_version="2024-12-01-preview",
    azure_endpoint="https://azopenai-langchain.openai.azure.com/",
    azure_ad_token_provider= token_provider,
    azure_deployment= "text-embedding-ada-002",
    model= "text-embedding-ada-002"
)


embeddings_date=model.embed_query("hello")


print(len(embeddings_date))