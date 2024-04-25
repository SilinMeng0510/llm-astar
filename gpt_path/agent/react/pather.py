from ...utils import parse, colors, list_parse
from ...model import ChatGPT
from gpt_path.env import Environment
import time


class ReActAgent():
    def __init__(self, correction=False):
        system_path = "gpt_path/agent/react/system_prompts/system.txt"
        example_path = 'gpt_path/agent/react/system_prompts/example_agent.json'
        self.gpt = ChatGPT(method="ReAct_A", system_path=system_path, example_path=example_path)
        self.correction = correction


    def run(self, command):
        self.gpt.id += 1
        
        sample = parse(command)
        
        answer = self.gpt_feed(command, sample)
        if self.gpt.id % 3 == 0:
            time.sleep(30)
        # clean the answer
        index = 0
        while index < len(answer) - 1:
            if answer[index][0] == answer[index + 1][0] and answer[index][1] == answer[index + 1][1]:
                del answer[index]
                continue
            index += 1
        return {"object" : sample, "path" : answer}


    def gpt_feed(self, prompt, object): 
        env = Environment(start=(object[0], object[1]), end=(object[2], object[3]), object=object[4:])
        prompt += "\n"
        while True:
            with open('outcome/ReAct_A/chat_history.txt', 'a+') as file:
                file.write(f"\nCHAT-{self.gpt.id}\n")
                
                question = colors.YELLOW + "User> " + colors.ENDC
                print(f"\n{question}{prompt}\n")
                file.write(f"User> {prompt}\n")

                response = self.gpt.ask(prompt)
                
                answer = colors.RED + "GPT> " + colors.ENDC
                print(f"\n{answer}{response[2:]}\n")
                file.write(f"GPT> {response[2:]}\n")

                if response.startswith("> finish:"):
                    path = list_parse(response)
                    break
                
                check = env.step(response)

                answer = colors.BLUE + "ENV> " + colors.ENDC
                print(f"\n{answer}{check}\n")
                file.write(f"ENV> {check}\n")

                prompt += response + "\n" + check
                
                if check.startswith('Success:'):
                    return env.path
                
                if check.startswith("Failed:") or env.index > 20:
                    path = [[object[0], object[1]], [object[2], object[3]]]
                    break
        
        path = [(point[0], point[1]) for point in path]
        return path