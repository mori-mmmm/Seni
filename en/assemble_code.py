import pickle

p1 = """import discord
from discord.ext import tasks
import random
import json
import os
import sys
import pickle
from time import time, sleep
from datetime import datetime
from dotenv import load_dotenv

from llm_util import get_llm_ret
from assemble_code import get_improved_code
"""

p2 = """
load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
BOT_PREFIX = 'Senya'


class Bot(discord.Client):
    def __init__(self, intents, heartbeat_timeout):
        super(Bot, self).__init__(intents=intents, heartbeat_timeout=heartbeat_timeout)


    async def improve_bot(self, request, channel):
        current_code = open(__file__, 'r', encoding='utf-8').read()
        prompt = f\"\"\"{request}\\nTo implement this request, we'll create a Python file and import one function.\\nYou'll output the following three things:\\n1. The command name specified by the user in the {request}. It will be inside [ ] brackets.\\n2. The file name.\\n3. The function name.\\nThe function name should end with _and_send because it includes the functionality to send a message. For example, if the user says "Create a command [GoogleSearch] and summarize Google search results", then from google_search import google_search_and_send would be appropriate. So you should output exactly 3 lines, one for each:\\n[GoogleSearch]\\ngoogle_search\\ngoogle_search_and_send\\nDon't add any additional sentences and stick to this format.\"\"\"
        llm_res = await get_llm_ret(prompt)
        print('gr:', llm_res[0])
        res = llm_res[0].split('\\n')
        cmd = res[0].strip()
        file_name = res[1].strip()
        function_name = res[2].strip()
        try:
            with open('cmd_list.pkl', 'rb') as f:
                cl = pickle.load(f)
        except:
            cl = []
        with open('cmd_list_backup.pkl', 'wb') as f:
            pickle.dump(cl, f)
        cl.append((cmd, file_name, function_name))
        with open('cmd_list.pkl', 'wb') as f:
            pickle.dump(cl, f)

        improved_code = get_improved_code()
        print(improved_code)
        with open('backup.py', 'w') as f:
            f.write(current_code)
        with open('improved_code.py', 'w') as f:
            f.write(improved_code)

        prompt = f\"\"\"{request}\\nTo handle this request, we need to write code that will go into {file_name}.py.\\nThis code is being used as follows:\\n{improved_code}\\n\\nImplement the functions that are being imported from {file_name} in the code above. If you need to use an LLM during code implementation, use from llm_util import get_llm_ret. get_llm_ret returns a tuple of message and usage, so if you only need the message, use the 0th element of the result tuple. If additional packages are needed, make sure they're installed at the beginning with something like os.system('pip install something'). The whole thing should be in a form that can be executed immediately. Don't add unnecessary comments. Don't write explanations about the code or modifications. And make sure the entire code is there without any omissions. For packages that need to be installed, only import os first, then use os.system('pip install ...') to install, and then import afterwards. Follow this order. Install the package before importing it. And since we're using os.system, it should come after import os. The order should be: import os -> os.system('pip install ...') -> import ...
        Also, the function name always ends with _and_send because it includes the functionality to send a message. So the overall structure of the code should be:
        async def function_name_and_send(message, ...):
            try:
                # function body
                await message.channel.send(f" ... ")
            except Exception as e:
                await message.channel.send(f" ... Error message ... {{str(e)}}")
        It should follow this format.\"\"\"
        llm_res = await get_llm_ret(prompt)
        res = llm_res[0]
        prompt = f\"\"\"{res}\\nExtract only the code part from the text above. If the code is wrapped in a code block like ```, extract only the contents. If there are additional explanations about the code, remove them and extract only the code area in a form that can be executed on its own. Don't wrap it in a code block and don't add any additional comments.\"\"\"
        llm_res = await get_llm_ret(prompt)
        res = llm_res[0]
        
        res = res.strip()
        print('bf:', res, '```' in res, '```python' in res)
        res = res.replace('```python','')
        print('ff:', res)
        res = res.replace('```','')
        print('af:', res)
        if res.startswith('['):
            res = res[1:]
        if res.endswith(']'):
            res = res[:-1]

        with open(f"{file_name}.py", "w") as f:
            f.write(res)
        sys.exit(0)
        
        await channel.send("Failed to update the bot.")

    async def rollback_code(self, channel):
        if os.path.exists('backup.py') and os.path.exists('cmd_list_backup.pkl'):
            with open('cmd_list_backup.pkl', 'rb') as f:
                clb = pickle.load(f)
            with open('cmd_list.pkl', 'wb') as f:
                pickle.dump(clb, f)
            backup_code = open('backup.py', 'r', encoding='utf-8').read()
            with open(__file__, 'w', encoding='utf-8') as f:
                f.write(backup_code)
            sys.exit(0)
        else:
            await channel.send("No backup file exists.")

    async def on_ready(self):
        pass

    async def on_message(self, message):
        if message.author == self.user:
            return

        in_msg = message.content
        print(f'[{str(datetime.now())}] [{message.guild.name}({message.guild.id})] [{message.channel.name}({message.channel.id})] [{message.author.name}({message.author.id})] ' + in_msg)
        server_id = message.guild.id
        channel_id = message.channel.id
        if in_msg.startswith(BOT_PREFIX):
            in_msg = in_msg[len(BOT_PREFIX):].lstrip()
            if in_msg.startswith('['):
                if in_msg.startswith('[Implement]'):
                    request = in_msg[len('[Implement]'):].lstrip()
                    await self.improve_bot(request, message.channel)
                elif in_msg.startswith('[Rollback]'):
                    await self.rollback_code(message.channel)"""

p3 = """
                else:
                    await message.channel.send("This command does not exist.")
            else:
                llm_res, usage = await get_llm_ret(in_msg)
                await message.channel.send(llm_res)
                

intents = discord.Intents.default()
intents.message_content = True
discord_client = Bot(intents=intents, heartbeat_timeout=3600)
discord_client.run(TOKEN)
"""

def get_improved_code():
    with open('cmd_list.pkl', 'rb') as f:
        cl = pickle.load(f)
    ret = p1
    for cmd, file_name, function_name in cl:
        ret += f"""from {file_name} import {function_name}\n"""
    ret += p2
    for cmd, file_name, function_name in cl:
        ret +=f"""
                elif in_msg.startswith('{cmd}'):
                    query = in_msg[len('{cmd}'):].strip()
                    await {function_name}(message, query)"""
    ret += p3
    return ret
