from langchain_community.document_loaders import PyPDFLoader


loader=PyPDFLoader("./data/focus-azurebilling.pdf")
docs=loader.load()
print(len(docs))

data=loader.load_and_split()
print(len(data))
print(data[0])