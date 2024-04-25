from ...utils.utils import parse, colors, list_parse
from ...model.chatgpt import ChatGPT

import json

class FewShot():
    def __init__(self):
        system_path = "gpt_path/planner/few_shot/system_prompts/system.txt"
        example_path = 'gpt_path/planner/few_shot/system_prompts/example.json'
        self.gpt = ChatGPT(method="FS", system_path=system_path, example_path=example_path)


    def run(self, command):
        self.gpt.id += 1
        
        sample = parse(command)
        
        answer = self.gpt_feed(command, sample)
        # clean the answer
        index = 0
        while index < len(answer) - 1:
            if answer[index][0] == answer[index + 1][0] and answer[index][1] == answer[index + 1][1]:
                del answer[index]
                continue
            index += 1
        return {"object" : sample, "path" : answer}


    def gpt_feed(self, prompt, object):
        prompt += "\n"     
        with open('outcome/FS/chat_history.txt', 'a+') as file:
            file.write(f"\nCHAT-{self.gpt.id}\n")
            
            question = colors.YELLOW + "User> " + colors.ENDC
            print(f"\n{question}{prompt}\n")
            file.write(f"User> {prompt}\n")

            response = self.gpt.ask(prompt)[2:]
            
            answer = colors.RED + "GPT> " + colors.ENDC
            print(f"\n{answer}{response}\n")
            file.write(f"GPT> {response}\n")
        
        path = [(point[0], point[1]) for point in json.loads(response)]
        
        return path