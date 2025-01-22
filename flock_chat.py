import os
from duckMGPT import DuckGPT
import threading
import time

def ask(model: str, prompt: str, output: str = None):
    if output is None: output = model
    try:
        client = DuckGPT(model=model)
        response = client.Chat(prompt, [])
        op = f'responses{os.sep}{output.split("/")[0]}.md'
        with open(op, 'w', encoding='utf-8') as f:
            # print(f'{model} responded: {response}')
            f.write(response)
            print(f'Wrote {op}')
    except DuckGPT.OperationError as e:
        print(f'{model} had an error')
        print(e)

# Initialize the client with the desired model
client = DuckGPT()

models = [model for model in client.Models()]

threads = []

with open("prompt.txt", 'r', encoding='utf-8') as f:
    prompt = f.read()

for model in models:
    threads.append(threading.Thread(target=ask, args=(model, prompt)))
    threads[-1].start()
    time.sleep(1)

for thread in threads:
    thread.join()
try:
    r = ['responses'+os.sep+i for i in os.listdir(os.getcwd()+os.sep+'responses') if '.md' in i and 'summary' not in i.lower()]
    responses = []
    for i in r:
        with open(i, 'r', encoding='utf-8') as f:
            responses.append(f.read())


    prompt = "Please summarise the following responses for me and provide examples\n"
    subprompt = "Response {index} {model}:\n{i}\n\n"

    for i, j in enumerate(responses):
        prompt += subprompt.format(index=i, model=r[i], i=j)
    ask("gpt-4o-mini", prompt, "GPT Summary")
except FileNotFoundError as e:
    print(f'Summary failed, response folder not found')
