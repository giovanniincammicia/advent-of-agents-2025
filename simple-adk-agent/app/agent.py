import os
import asyncio
from google.adk.agents import Agent
from google.adk.models import Gemini
from google.adk.sessions import InMemorySessionService, Session
from google.adk.runners import Runner
from google.genai import types
from app.sub_agents.sum.agent import agent as sum_agent
from app.sub_agents.code.agent import agent as code_agent
from google.adk.tools import agent_tool

import warnings
# Ignore all warnings
warnings.filterwarnings("ignore")

import logging
logging.basicConfig(level=logging.ERROR)

os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "False"
os.environ["GOOGLE_API_KEY"] = "AIzaSyAIZhIdhXiholaNQuVOnnHCnoO_2Z_jWsU"

def generate_random_number_between(from_value: int, to_value: int) -> int:
    """
    Generate a random integer between 1 and 100.

    Args:
        from_value (int): The lower bound of the range (inclusive).
        to_value (int): The upper bound of the range (inclusive).

    Returns:
        int: A random integer between from_value and to_value.
    """
    import random
    return random.randint(from_value, to_value)

APP_NAME = 'random_number_app'
USER_ID = 'user_123'
SESSION_ID = 'random_number_session'

agent = Agent(
    name=APP_NAME,
    description="An agent that generates a random number between two given integers."
    "You have specialized sub-agents:"
    "- sum_agent for summing two integers."
    "- code_agent for generating and executing code."
    "Use them as needed to fulfill user requests.",
    model=Gemini(
        model="gemini-3-flash-preview",
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    instruction='You are an agent that generates a random integer between two provided integers. The user will provide the range, and you will return a random integer within that range.',
    # Two approaches here. The first one uses agents as tools. This is needed when one of the agents use built-in tools like code execution
    # Otherwise you get the "Tool use with function calling is unsupported" error.
    tools=[generate_random_number_between, agent_tool.AgentTool(agent=sum_agent), agent_tool.AgentTool(agent=code_agent)]
    # The second approach uses sub_agents directly.
    # tools=[generate_random_number_between],
    # sub_agents=[sum_agent, code_agent]
    # The difference is that subagents take over the full conversation when invoked, while agent tools only get the tool-specific input.
)

session_service = InMemorySessionService()
runner = Runner(agent=agent, app_name=APP_NAME, session_service=session_service)

async def init_session(app_name:str, user_id:str, session_id:str) -> Session:
    session = await session_service.create_session(
        app_name=app_name,
        user_id=user_id,
        session_id=session_id
    )
    return session

async def call_agent_async(query: str, runner, user_id, session_id):
  """Sends a query to the agent and prints the final response."""
  print(f"\n>>> User Query: {query}")

  # Prepare the user's message in ADK format
  content = types.Content(role='user', parts=[types.Part(text=query)])

  final_response_text = "Agent did not produce a final response." # Default

  # Key Concept: run_async executes the agent logic and yields Events.
  # We iterate through events to find the final answer.
  async for event in runner.run_async(user_id=user_id, session_id=session_id, new_message=content):
      # You can uncomment the line below to see *all* events during execution
      print(f"  [Event] Author: {event.author}, Type: {type(event).__name__}, Final: {event.is_final_response()}, Content: {event.content}")

      # Key Concept: is_final_response() marks the concluding message for the turn.
      if event.is_final_response():
          if event.content and event.content.parts:
             # Assuming text response in the first part
             final_response_text = event.content.parts[0].text
          elif event.actions and event.actions.escalate: # Handle potential errors/escalations
             final_response_text = f"Agent escalated: {event.error_message or 'No specific message.'}"
          # Add more checks here if needed (e.g., specific error codes)
          break # Stop processing events once the final response is found

  print(f"<<< Agent Response: {final_response_text}")

async def run_conversation():
    await call_agent_async("Generate a random number between 1 and 10",
                            runner=runner,
                            user_id=USER_ID,
                            session_id=SESSION_ID)

    await call_agent_async("generate a number between 6 and 9, then generate a number between 1 and 3, then sum them",
                            runner=runner,
                            user_id=USER_ID,
                            session_id=SESSION_ID)

if __name__ == "__main__":
  try:
      session = asyncio.run(init_session(APP_NAME, USER_ID, SESSION_ID))

      asyncio.run(run_conversation())
  except Exception as e:
      print(f"An error occurred: {e}")

root_agent = agent