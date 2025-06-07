from langchain_community.document_loaders import AzureBlobStorageContainerLoader
from dotenv import load_dotenv
import os

load_dotenv()
azureblobconn = os.getenv('AzureSTG_CONN')
azure_loader=AzureBlobStorageContainerLoader(conn_str=azureblobconn,container="ailearn")
data=azure_loader.load()
print(len(data))
