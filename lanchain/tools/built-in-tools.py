from langchain_community.tools import WikipediaQueryRun,YouTubeSearchTool
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_tavily import TavilySearch
from dotenv import load_dotenv 
import os

load_dotenv();
tavily_apikey= os.getenv("TAVILY_APIKEY")


########################  Built-In Tools   ######################
# Wiki Tool
apiWrapper=WikipediaAPIWrapper(top_k_results=3, doc_content_chars_max=500, lang ="en")
tool=WikipediaQueryRun(api_wrapper=apiWrapper)
#print(tool.name)
#print(tool.description)
#print(tool.args)
response=tool.invoke(input= "RCB")
#print(response)

## Youtube tool
youtubetool= YouTubeSearchTool()
youtuberesponse=youtubetool.run("IaminAzure")
#print(youtuberesponse)

## Tavily Tool
tavily_tool = TavilySearch(
    max_results=1,
    topic="general",
    tavily_api_key = tavily_apikey
    # include_answer=False,
    # include_raw_content=False,
    # include_images=False,
    # include_image_descriptions=False,
    # search_depth="basic",
    # time_range="day",
    # include_domains=None,
    # exclude_domains=None
)

tavily_response= tavily_tool.invoke({"query": "What s the latest trending news"})
print(tavily_response["results"][0]["content"])