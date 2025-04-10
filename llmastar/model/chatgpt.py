import openai
import os
from .prompts.system_prompts import SYSPROMPT_PARSE, EXAMPLE_PARSE
from .prompts.gpt_prompts import GPT_PROMPTS

# This class instantiate the API, used to communicate with GPT
class ChatGPT:
    def __init__(self, method, sysprompt=None, example=None):
        self.id = 0
        self.method = method
        
        # Use provided sysprompt or default to system parsing prompt
        self.sysprompt = sysprompt if sysprompt else SYSPROMPT_PARSE
        self.example = example if example else EXAMPLE_PARSE
        
        self.chat_history = [
            {"role": "system", "content": self.sysprompt}
        ]
        
        if self.example:
            self.prompt = self.sysprompt + f'\nFollow these examples delimited with """ as a guide.\n'
            keys = list(self.example.keys())
            # keys.pop(0)
            for key in keys:
                input = self.example[key]
                index = input.find("\n") + 1
                self.prompt += f'"""\nUser: {input[:index - 1]}\nAssistant: {input[index:]}"""\n'
                self.chat_history.append({"role": "user", "content": input[:index - 1]})
                self.chat_history.append({"role": "assistant", "content": input[index:]})
        else:
            self.prompt = self.sysprompt

        
    def ask(self, prompt, stop=["\n"], max_tokens=100):
        response = openai.Completion.create(
            model="gpt-3.5-turbo-instruct",
            prompt=prompt,
            temperature=0,
            max_tokens=max_tokens,
            stop=stop
        )
        return response["choices"][0]["text"]
    
    def chat(self, query, prompt="", stop=["\n"], max_tokens=100):
        # new = self.chat_history + [{"role": "user", "content": query}, {"role": "assistant", "content": prompt}]
        # print(new)
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": self.prompt},
                {"role": "user", "content": query},
                {"role": "assistant", "content": prompt}
            ],
            temperature=0,
            max_tokens=max_tokens,
            stop=stop
        )
        return response["choices"][0]["message"]["content"]
    
    def chat_with_image(self, chat_history, stop=["\n"], max_tokens=100):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=chat_history,
            temperature=0
        )
        return response["choices"][0]["message"]["content"]