import logging
import warnings
import os
import sys


import anyio
from dotenv import load_dotenv
from ibm_watsonx_gov.tools import load_tool
from mcp.server import Server
from mcp.types import EmbeddedResource, ImageContent, TextContent, Tool
import mcp.types as types
from .utils.catalog_utils import list_gov_tools
from .utils.mcp_utils import catalog_crud_tools


warnings.filterwarnings("ignore")

# Set up logging
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO").upper(),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stderr,
)
logger = logging.getLogger(__name__)


app = Server("ibm-agentic-governance-catalog-mcp-server")

@app.call_tool()
async def fetch_tool(
    name: str,
    arguments: dict
):  
    
    if name == "register_tool":
        from ibm_watsonx_gov.tools.clients import register_tool,ToolRegistrationPayload    
        try:
            if arguments.get("tool_type") == "code":
                tool_code = arguments.pop("code",None)
                arguments["code"] = {
                    "source_code_base64": tool_code,
                    "run_time_details": {
                        "engine": "Python3.11"
                    }
                }
            elif arguments.get("tool_type") == "endpoint":
                arguments.pop("code",None)
                
            #Check for dependencies
            if len(arguments.get("dependencies",[])) > 0:
                dependencies =  arguments.pop("dependencies",None)
                arguments["dependencies"] = {
                    "run_time_packages": dependencies
                }
        except Exception as ex:
            logger.warning(f"Error getting the payload for tool registration.Details:{str(ex)}")
            response = ""
            return [TextContent(type="text", text=response)]
            
        response = register_tool(ToolRegistrationPayload(**arguments))
    elif name == "get_tool":
        from ibm_watsonx_gov.tools.clients import get_tool_info
        response = get_tool_info(tool_name=arguments['tool_name'])
    elif name == "delete_tool":
        from ibm_watsonx_gov.tools.clients import delete_tool_with_name
        response = delete_tool_with_name(tool_name=arguments['tool_name'])
    else:
        #Load the tool from SDK
        tool = load_tool(tool_name=name)

        # Invoke the tool
        response = tool.invoke(arguments)
    if isinstance(response, list):
        response = "".join(response)
    else:
        response = str(response)
    # logger.info(f"Value of response:{response}")
    return [TextContent(type="text", text=response)]


@app.list_tools()
async def list_tools() -> list[types.Tool]:
    tools_list = await list_gov_tools()
    catalog_tools = [types.Tool(**tool) for tool in tools_list]
    tools = catalog_tools + catalog_crud_tools
    return tools



def run_gov_catalog_mcp_server() -> int:
    load_dotenv()
    from mcp.server.stdio import stdio_server

    async def arun():
        async with stdio_server() as streams:
            await app.run(
                streams[0], streams[1], app.create_initialization_options()
            )

    anyio.run(arun)
