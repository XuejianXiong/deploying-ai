from langchain.tools import tool
from langchain_community.tools.tavily_search import TavilySearchResults


#######################################
# Free Web Search
#######################################
@tool
def get_web_search(query: str):
    """
    Web searching for health trends, fitness news, nutrition facts, 
    or any general information not in the database.
    """
    
    search = TavilySearchResults(k=3)
    results = search.run(query)

    content_list = []
    for res in results:
        content_list.append(f"Source: {res.get('url')}\nContent: {res.get('content')}")
    
    return "\n\n".join(content_list)