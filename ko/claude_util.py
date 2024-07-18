import aiohttp
import json
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.environ.get("ANTHROPIC_API_KEY")

async def get_llm_ret(query):
    headers = {
        "Content-Type": "application/json",
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01",
    }

    data = {
        "model": "claude-3-5-sonnet-20240620",
        "messages": [{"role": "user", "content": query}],
        "max_tokens": 4096
    }

    async with aiohttp.ClientSession() as session:
        async with session.post("https://api.anthropic.com/v1/messages", headers=headers, json=data) as response:
            if response.status == 200:
                result = await response.json()
                return result["content"][0]["text"], None
            else:
                error_message = await response.text()
                raise Exception(f"API 요청 실패: {response.status}, {error_message}")
