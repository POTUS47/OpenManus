import asyncio
from typing import List
from baidusearch.baidusearch import search
from app.tool.base import BaseTool

class BaiduSearchTool(BaseTool):
    name:str='baidu_search'
    description :str ='''Perform a Baidu search and return a list of relevant links
Use this tool when you need to find information on the web, get up-to-date data, or research
specific topics.
The tool returns a list of URLs that match the search query'''
    parameters:dict = {
        "type":"object",
        "properties":{
            "query":{
                "type":"string",
                "description":"(required) The search query to submit to Baidu",
            },
            "num_results":{
                "type":"integer",
                "description":"(optional) The number of results to return.Default is 10.",
                "default":10,
            },
        },
        "required":["query"],
    }
    async def execute(self,query:str,num_results:int=10)->List[dict]:
        loop = asyncio.get_event_loop()
        links = await loop.run_in_executor(None,
        lambda:[result['url'] for result in search(query, num_results=num_results)])
        return links