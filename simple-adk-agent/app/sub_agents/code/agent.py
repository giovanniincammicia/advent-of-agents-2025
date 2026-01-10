from google.adk.agents import Agent
from google.adk.models import Gemini
from google.genai import types
from google.adk.code_executors import BuiltInCodeExecutor


agent = Agent(
    name='code_agent',
    description='An agent that generates code and executes it.',
    model=Gemini(
        model="gemini-3-flash-preview",
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    instruction='You are an agent that generates and executes code based on user instructions.',
    code_executor=BuiltInCodeExecutor()
)