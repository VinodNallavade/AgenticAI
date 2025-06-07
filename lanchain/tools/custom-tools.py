from langchain_core.tools import tool
#from langchain.agents import tool

@tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a*b

@tool
def Get_Word_Count(word:str) -> int:
    """This function return word length"""
    return len(word)

# Let's inspect some of the attributes associated with the tool.
print(multiply.name)
print(multiply.description)
print(multiply.args)
multiplyresponse=multiply.invoke({"a": 2, "b": 3})
print(multiplyresponse)

print(Get_Word_Count.description)
wordlength=Get_Word_Count.invoke("Hello")
print(wordlength)
