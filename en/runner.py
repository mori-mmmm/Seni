import os
from time import sleep

os.system("python base.py")
while True:
    sleep(2)
    with open('improved_code.py', 'r') as f:
        r = f.read()
    r = r.strip()
    if r.startswith('```python'):
        r = r.replace('```python','')
    if r.endswith('```'):
        r = r.replace('```','')
    if r.startswith('['):
        r = r[1:]
    if r.endswith(']'):
        r = r[:-1]
    with open('improved_code.py', 'w') as f:
        f.write(r)
    if os.system("python improved_code.py") != 0:
        os.system('cp backup.py improved_code.py')
        os.system('cp cmd_list_backup.pkl cmd_list.pkl')
        print('Rollback!')
