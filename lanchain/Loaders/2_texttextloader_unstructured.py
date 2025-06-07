from langchain_community.document_loaders import UnstructuredFileLoader


loader =UnstructuredFileLoader("./data/sample.txt")
data=loader.load()
print(data)

for doc in data:
    print(f"Content: {doc.page_content}")  # Access the textual content
    print(f"Metadata: {doc.metadata}")      # Access any metadata associated with the document