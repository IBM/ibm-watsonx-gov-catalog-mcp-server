import mcp.types as types

catalog_crud_tools = [types.Tool(
            name="register_tool",
            description="Tool to register new custom tool using tool code or rest api",
            inputSchema={
                "type":"object",
                "properties":{
                    "tool_name": {
                        "type": "string",
                        "description": "Unique name for the tool"
                    },
                    "description": {
                        "type": "string",
                        "description": "Tool description"
                    },
                    "tool_type": {
                        "type": "string",
                        "description": "Tool type."
                    },
                    "schema":{
                        "type":"object",
                        "properties":{
                            "type":{
                                "type":"string",
                                "description": "Datatype of the property"
                            },
                            "description":{
                                "type":"string",
                                "description": "Descriptionof the property"
                            }
                        }
                    },
                    "code":{
                        "type":"string",
                        "description":"Tool code"
                    },
                    "endpoint":{
                        "type":"object",
                        "properties":{
                            "url":{
                                "type":"string",
                                "description":"RESTAPI endpoint url"
                            },
                            "headers":{
                                "type":"object",
                                "description":"Headers to be passed for tool"
                            },
                            "method":{
                                "type":"string",
                                "description":"HTTP method",
                                "default":"POST"
                            }
                        }
                    },
                    "dependencies":{
                        "type":"array",
                        "description":"Array of python packages"
                    },
                    "environment_variables":{
                        "type":"array",
                        "description":"Array of env variables"
                    }
                }
            }
    ),
    types.Tool(
        name="get_tool",
        description="Get tool details based on name of tool",
        inputSchema={
            "type":"object",
            "required":["tool_name"],
            "properties":{
                    "tool_name": {
                        "type": "string",
                        "description": "Unique name for the tool"
                    }
            }
        }
    ),
    types.Tool(
        name="delete_tool",
        description="Get tool details based on name of tool",
        inputSchema={
            "type":"object",
            "required":["tool_name"],
            "properties":{
                    "tool_name": {
                        "type": "string",
                        "description": "Unique name for the tool"
                    }
            }
        }
    )]