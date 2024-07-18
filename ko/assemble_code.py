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
BOT_PREFIX = '세니야'


class Bot(discord.Client):
    def __init__(self, intents, heartbeat_timeout):
        super(Bot, self).__init__(intents=intents, heartbeat_timeout=heartbeat_timeout)


    async def improve_bot(self, request, channel):
        current_code = open(__file__, 'r', encoding='utf-8').read()
        prompt = f\"\"\"{request}\\n이 요청을 구현하기 위해 파이썬 파일을 하나 만들고 함수를 하나 import해올거야.\\n네가 출력할건 다음 세 가지야:\\n1. {request}에서 사용자가 정한 명령어 이름. [ ] braket안에 적혀있을거야.\\n2. 파일 이름.\\n3. 함수 이름.\\n함수 이름은 _and_send로 끝나야해. 메세지를 전송하는 기능을 포함하고 있거든. 예를 들어서 사용자가 "[구글검색]이라는 명령어를 만들고 구글 검색 결과를 요약해줘"라고 한다면 from google_search import google_search_and_send 정도가 적당할거야. 그러면 너는 한 줄에 하나씩\\n[구글검색]\\ngoogle_search\\ngoogle_search_and_send\\n이렇게 딱 3줄을 출력하면 돼. 추가적인 문장 덧붙이지 말고 저 포맷을 지켜.\"\"\"
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

        prompt = f\"\"\"{request}\\n이 요청을 처리하기 위해 {file_name}.py에 들어갈 코드를 작성해야해.\\n이 코드는 다음과 같이 사용되고 있어:\\n{improved_code}\\n\\n위의 코드에서 from {file_name}에서 import하고 있는 함수들을 구현하면 돼. 코드 구현 중에 llm 사용이 필요하면 from llm_util import get_llm_ret 를 사용하도록 해. get_llm_ret는 메세지와 usage의 튜플을 리턴하니까 메세지만 필요하면 결과 튜플의 0번째 인자를 사용하면 돼. 추가적인 패키지가 필요할 경우 맨 처음에 os.system('pip install 어쩌구') 같은 형태로 실행되게 해줘. 그리고 전체가 바로 실행 가능한 형태여야 해. 쓸데없는말 덧붙이지마. 코드 설명, 수정 사항에 대한 설명 적으면 안 돼. 그리고 반드시 생략하는 부분 없이 전체 코드가 다 나와야해. 설치해야하는 패키지는 import os만 한 이후에 os.system('pip install ...')로 설치하고 그 이후에 import 해줘. 순서를 지켜. 패키지를 import하기 전에 설치해. 그리고 os.system을 쓸거니까 import os보단 나중에 나와야해. import os -> os.system('pip install ...') -> import ... 이 순서가 돼야해.
        그리고 함수의 이름은 항상 _and_send로 끝나. 메세지를 전송하는 기능을 포함하고 있거든. 그래서 전체적인 코드의 구성은
        async def function_name_and_send(message, ...):
            try:
                # function body
                await message.channel.sned(f" ... ")
            execpt Exception as e:
                await message.channel.send(f" ... Error message ... {{str(e)}}")
        같은 형태가 돼야해.\"\"\"
        llm_res = await get_llm_ret(prompt)
        res = llm_res[0]
        prompt = f\"\"\"{res}\n위의 텍스트에서 코드에 해당하는 부분만 추출해줘. 만약 코드가 ```와 같이 코드 블록으로 감싸져 있다거나, 부가적인 코드에 대한 설명이 붙어있다면 제거하고, 그 자체로 실행가능한 형태로 코드 영역만 추출해줘. 코드블록으로 감싸지도 말고 아무 추가적인 말도 덧붙이지 말아줘.\"\"\"
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
        
        await channel.send("봇 업데이트에 실패했습니다.")

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
            await channel.send("백업 파일이 없습니다.")

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
                if in_msg.startswith('[구현]'):
                    request = in_msg[len('[구현]'):].lstrip()
                    await self.improve_bot(request, message.channel)
                elif in_msg.startswith('[롤백]'):
                    await self.rollback_code(message.channel)"""

p3 = """
                else:
                    await message.channel.send("존재하지 않는 명령어입니다.")
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
