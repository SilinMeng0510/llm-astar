import openai
import argparse, json, os

# This class instantiate the API, used to communicate with GPT
class ChatGPT:
    def __init__(self, method, sysprompt, example):
        with open("config.json", "r") as f:
            config = json.load(f)
        openai.api_key = config["OPENAI_API_KEY"]
        openai.organization = config["ORGANIZATION"]
        
        self.id = 0
        self.prompt = sysprompt.replace("\n", "") + f" Here are {len(example)} examples.\n"
        
        keys = list(example.keys())
        # keys.pop(0)
        for key in keys:
            self.prompt += f"{example[key]}"
        self.prompt += "\nHere is the task.\n"
        
        if not os.path.exists(f'outcome/{method}/'):
            os.makedirs(f'outcome/{method}/', exist_ok=True)
            os.makedirs(f'outcome/{method}/plots/', exist_ok=True)
            
        with open(f'outcome/{method}/chat_history.txt', 'w') as file:
            file.write("PROMPT & INCONTEXT SAMPLES\n")
            file.write(self.prompt)
            file.write("\n*********************************************************************************************\n")
            file.write("\nCHAT HISTORY WITH GPT-3.5\n")

        
    def ask(self, prompt, stop=["\n"], max_tokens=100):
        response = openai.Completion.create(
            model="gpt-3.5-turbo-instruct",
            prompt=self.prompt + prompt,
            temperature=0,
            max_tokens=max_tokens,
            stop=stop
        )
        return response["choices"][0]["text"]