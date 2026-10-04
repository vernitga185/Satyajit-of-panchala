import json
import openai
from .config import settings

client = openai.AsyncClient(api_key=settings.TOGETHER_API_KEY, base_url="https://api.together.xyz/v1")

async def chat_with_agent(messages: list, tools: list = None) -> dict:
    try:
        response = await client.chat.completions.create(
            model=settings.MODEL_NAME,
            messages=messages,
            tools=tools,
            temperature=0.0
        )
        return response.choices[0].message
    except Exception as e:
        print(f"Agent error: {e}")
        return None
