from google.adk.agents import Agent
from google.adk.models import Gemini
from google.genai import types

def sum(a: int, b: int) -> int:
    """
    Returns the sum of two integers.

    Args:
        a (int): The first integer.
        b (int): The second integer.

    Returns:
        int: The sum of a and b.
    """
    return a + b

agent = Agent(
    name='sum_agent',
    description='An agent that generates a random number between two given integers.',
    model=Gemini(
        model="gemini-3-flash-preview",
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    instruction='You are an agent that sums two provided integers. The user will provide the integers, and you will return their sum.',
    tools=[sum]
)