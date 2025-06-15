from azure.identity import DefaultAzureCredential, get_bearer_token_provider

def get_azure_openai_model():
    token_provider = get_bearer_token_provider(
        DefaultAzureCredential(),
        "https://cognitiveservices.azure.com/.default"
    )

    from langchain_openai import AzureChatOpenAI
    return AzureChatOpenAI(
        api_version="2024-12-01-preview",
        azure_endpoint="https://azopenai-langchain.openai.azure.com/",
        azure_ad_token_provider=token_provider,
        model="gpt-4o-mini"
    )
