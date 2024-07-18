# SENI: Self-ENabling Intelligence
A self-improving GPT/CLAUDE-based Discord chatbot

## Usage Examples
### Example 1
```
User: Hello
User: Senya hello
seni: Hello, how can I help you?
User: Senya [calculate] 123**10
seni: This command does not exist.
User: Senya [Implement] Add a command [calculate] that uses Python's calculation function to compute the given expression
(Bot restarts)
User: Senya [calculate] 123**10
seni: The result of the calculation is 792594609605189126649.
User: Senya [Rollback]
(Bot restarts)
User: Senya [Implement] Add a command [calculate] that uses Python's eval function to compute the given expression. Output in the format "The result of [input] is [output]."
(Bot restarts)
User: Senya [calculate] 123**10
seni: The result of 123**10 is 792594609605189126649.
```
### Example 2
```
User: Senya [Implement] The [todo] command has sub-command keywords. First, if "add" keyword comes, save the following todo content in a list in todo_list.pkl. Also save the current timestamp as a tuple. Second, if "list" keyword comes, read todo_list.pkl and output the tuples of timestamps and todo contents in the list. Finally, "complete" keyword comes with a number, and it should remove the todo at that number from the list. Index starts from 1. Handle exceptions when todo_list.pkl doesn't exist.
Example) Senya [todo] add Test the bot
Example) Senya [todo] list
Example) Senya [todo] complete 2
(Bot restarts)
User: Senya [todo] list
seni: There are currently no todos.
User: Senya [todo] add Test the bot
seni: Todo list has been updated.
User: Senya [todo] list
seni: 1. [2024-07-18 15:51:16] Test the bot
User: Senya [todo] add Reply to emails
seni: Todo list has been updated.
User: Senya [todo] list
seni: 1. [2024-07-18 15:51:16] Test the bot
2. [2024-07-18 15:51:38] Reply to emails
User: Senya [todo] add Order lunch
seni: Todo list has been updated.
User: Senya [todo] list
seni: 1. [2024-07-18 15:51:16] Test the bot
2. [2024-07-18 15:51:38] Reply to emails
3. [2024-07-18 15:51:48] Order lunch
User: Senya [todo] complete 2
seni: Todo list has been updated.
User: Senya [todo] list
seni: 1. [2024-07-18 15:51:16] Test the bot
2. [2024-07-18 15:51:48] Order lunch
```
### Example 3
```
User: Senya [Implement] [drawgraph] Create a feature that uses sympy to input an equation in the form y = f(x), draws a graph using matplotlib, saves it as an image, and then sends it embedded in a message
(Bot restarts)
User: Senya [drawgraph] sin(x) / x
seni:
```
![plot](https://raw.githubusercontent.com/mori-mmmm/Seni/main/plot.png)
```
User: Senya [Implement] [draw3dgraph] Create a feature that outputs a 3D graph when an equation in the form z = f(x, y) is input. For example, if z = x**2 + y**2 is input, a paraboloid should appear, and if z = (x**2 + y**2) ** 0.5 is input, a cone should appear
(Bot restarts)
User: Senya [draw3dgraph] x*x+y*y
seni:
```
![plot3d](https://raw.githubusercontent.com/mori-mmmm/Seni/main/plot_3d.png)

## How to Run
### Step 1. Git Clone Repository
```
git clone https://github.com/mori-mmmm/Seni
cd Seni
```
### Step 2. Install Packages
```
pip install -r requirements.txt
```
### Step 3. Setup .env
```
cd ko
```
The .env file should include the following items:
```
DISCORD_TOKEN='Discord bot token'
OPENAI_API_KEY='Required if using gpt in llm_util.py'
ANTHROPIC_API_KEY='Required if using claude in llm_util.py'
```
### Step 4. Execute Runner
```
python runner.py
```
## Caution
This is still at a PoC level, and there's no guarantee that all features will be added easily and naturally at once.
If you have any ideas for improvement or new features, please feel free to leave an issue!
