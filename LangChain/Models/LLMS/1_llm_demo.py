import os
from azure.identity import DefaultAzureCredential,get_bearer_token_provider
from langchain_openai import AzureOpenAI

token_provider = get_bearer_token_provider(DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default")
client = AzureOpenAI(
    api_version="2024-12-01-preview",
    azure_endpoint="https://azopenai-langchain.openai.azure.com/",
    azure_ad_token_provider= token_provider,
    azure_deployment= "gpt-35-turbo-instruct",
    model= "gpt-35-turbo-instruct"
)

response =client.invoke("I am going to Paris, what should I see?")
print(response)
