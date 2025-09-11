
import pandas as pd
import asyncio

from ibm_watsonx_gov.tools.clients import list_tools,get_tool
from ibm_watsonx_gov.utils.python_utils import get


async def list_gov_tools() -> list:
        tools = list_tools()
        tools_list = tools['tools']
        tool_details = await get_tool_details(tools_list)

        tool_values = pd.DataFrame(tool_details)["entity"].values
        df = pd.DataFrame(list(tool_values))[
            ["tool_name", "description", "schema","tool_type"]]
        
        # Exclude listing of  RESTAPI tools as they involve headers
        df.query("tool_type != 'endpoint'",inplace=True)
        
        #Rename the columns as per the MCP needs
        df.rename(columns={'tool_name': 'name',
                'schema': 'inputSchema'}, inplace=True)

        tools_1 = df.to_dict(orient="records")
        return tools_1

async def get_tool_details(tool_list: list):
    tasks = [asyncio.to_thread(get_tool, get(tool, "metadata.id"), get(tool, "entity.inventory_id"))
            for tool in tool_list]
    return await asyncio.gather(*tasks)