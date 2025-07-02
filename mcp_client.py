# client.py

from mcp import ClientSession, StdioServerParameters

from mcp.client.stdio import stdio_client

from langchain_mcp_adapters.tools import load_mcp_tools

from langgraph.prebuilt import create_react_agent

from langchain_groq import ChatGroq

import asyncio

import os

# Set your API key (replace with your actual key or use environment variables)

GROQ_API_KEY = "" # Replace with your key

os.environ["GROQ_API_KEY"] = GROQ_API_KEY

# OPENAI_API_KEY = "YOUR_OPENAI_API_KEY"

# os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

# Initialize the LLM model

model = ChatGroq(model="llama3-8b-8192", temperature=0)

# model = ChatOpenAI(model="gpt-4o-mini", temperature=0)

server_params = StdioServerParameters(

   command="python",      # Command to execute

   args=["mcp_server.py"] # Arguments for the command (our server script)

)

async def run_agent():

   async with stdio_client(server_params) as (read, write):

       async with ClientSession(read, write) as session:

           await session.initialize()

           print("MCP Session Initialized.")

           tools = await load_mcp_tools(session)

           print(f"Loaded Tools: {[tool.name for tool in tools]}")

           agent = create_react_agent(model, tools)

           print("ReAct Agent Created.")

           print(f"Invoking agent with query")

           while True:
                response = await agent.ainvoke({

                    "messages": [("user", "Hows the weather in Pune and Mumbai today and what is the product of 5 and 7 ?")]

                })

                print("Agent invocation complete.")

                # Return the content of the last message (usually the agent's final answer)

                return response["messages"][-1].content
# Standard Python entry point check

if __name__ == "__main__":

   # Run the asynchronous run_agent function and wait for the result

   print("Starting MCP Client...")

   result = asyncio.run(run_agent())

   print("\nAgent Final Response:")

   print(result)