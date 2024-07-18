import os
import openai
import tiktoken
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
openai_client = OpenAI(api_key=openai.api_key)

async def get_llm_ret(query):
    completion = openai_client.chat.completions.create(
        model="gpt-4",
        messages=[{
            "role": "user",
            "content": f"""[{query}]""",
        }],
    )
    usage = completion.usage
    ret = completion.choices[0].message.content
    return ret, usage

