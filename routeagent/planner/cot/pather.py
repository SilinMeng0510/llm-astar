from ...utils import parse, colors, list_parse, extract_python_code, create_run_delete_file, filter_collision_path
from ...model.chatgpt import ChatGPT
from .prompt import *
import json, time

class ChainOfThought():
    def __init__(self):
        sysprompt = """You are an AI assistant specialized in planning collision-free paths for drones in a two-dimensional environment. You will be given a specific start point, end points and circular obstable position with size. Your task is to calculate a path from the start point to the end point that avoids any circular, static obstacles.  Your solution should be a sequence of points in the format of [[x1, y1], [x2, y2], ..., [xn, yn]], forming a safe and efficient route to ensure collision-free movement. The path should be a series of straight lines between consecutive points, avoiding all circular obstacles' areas. """
        example = {
            "cot_1": "design a path from [10, 0] to [0, 10] that avoids crossing the area of circle centered at [5, 5] with a radius of 4.\n> Let's think step by step. To avoid the circular obstacle at [5, 5] with a radius of 4, we need to find an additional point in between the start and end points. [0, 0] connects [10, 0] and [0, 10] without crossing the circular obstacle. Therefore, the final path is [[10, 0], [0, 0], [0, 10]].\n",
            "cot_2": "design a path from [80, 40] to [-10, 10] that avoids crossing the area of circle centered at [32, 32] with a radius of 30.\n> Let's think step by step. To avoid the circular obstacle at [32, 32] with a radius of 30, we need to find an additional point in between the start and end points. [40, -10] connects [80, 40] and [-10, 10] without crossing the circular obstacle. Therefore, the final path is [[80, 40], [40, -10], [-10, 10]].\n",
            "cot_3": "design a path from [-2, 27] to [3, -50] that avoids crossing the area of circle centered at [-19, 6] with a radius of 23.\n> Let's think step by step. To avoid the circular obstacle at [-19, 6] with a radius of 23.68112539820996, we need to find an additional point in between the start and end points. [20, 0] connects [-2, 27] and [3, -50] without crossing the circular obstacle. Therefore, the final path is [[-2, 27], [20, 0], [3, -50]].\n"
        }
        self.gpt = ChatGPT(method="COT", sysprompt=sysprompt, example=example)


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
        with open('outcome/COT/chat_history.txt', 'a+') as file:
            file.write(f"\nCHAT-{self.gpt.id}\n")
            
            question = colors.YELLOW + "User> " + colors.ENDC
            print(f"\n{question}{prompt}\n")
            file.write(f"User> {prompt}\n")

            response = self.gpt.ask(prompt)[2:]
            
            answer = colors.RED + "GPT> " + colors.ENDC
            print(f"\n{answer}{response}\n")
            file.write(f"GPT> {response}\n")
        
        path = list_parse(response)
        print(f"PATH> {path}\n")
        
        path = [(point[0], point[1]) for point in path]
        
        return path


class RePE():
    def __init__(self):
        example =  {
            "repe_0" : repe_0,
            "repe_1" : repe_1,
            "repe_2" : repe_2
        }
        self.gpt = ChatGPT(method="RePE", sysprompt=sysprompt, example=example)


    def run(self, command):
        self.gpt.id += 1
        
        sample = parse(command)
        
        answer = self.gpt_chat(command, sample)
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
        with open('outcome/RePE/chat_history.txt', 'a+') as file:
            file.write(f"\nCHAT-{self.gpt.id}\n")
            question = colors.YELLOW + "User> " + colors.ENDC
            print(f"\n{question}{prompt}\n")
            file.write(f"User> {prompt}\n")
            answer = colors.RED + "GPT> " + colors.ENDC
            print(f"{answer}")
            file.write(f"GPT>\n")
            current = [object[0], object[1]]
            while True:
                response = self.gpt.ask(prompt, stop=["\n", ":"], max_tokens=100)
                if response.startswith("Generated Points") or response.startswith("Current Path"):
                    prompt += response + ":"
                    answer = self.gpt.ask(prompt, stop=["\n", ":"], max_tokens=100)
                    prompt += answer + "\n"
                    print(f"{response}:{answer}")
                    file.write(f"{response}:{answer}\n")
                elif response.startswith("Arrival Check"):
                    prompt += response + ":"
                    answer = self.gpt.ask(prompt, stop=["\n", ":"], max_tokens=100)
                    if "Yes" in answer:
                        prompt += answer + "\n\n"
                        print(f"{response}:{answer}\n")
                        file.write(f"{response}:{answer}\n\n")
                    else:
                        prompt += answer + "\n"
                        print(f"{response}:{answer}")
                        file.write(f"{response}:{answer}\n")
                elif response.startswith("Selected Point"):
                    prompt += response + ":"
                    answer = self.gpt.ask(prompt, stop=["\n", ":"], max_tokens=100)
                    prompt += answer + "\n"
                    current = json.loads(answer[1:])
                    print(f"{response}:{answer}")
                    file.write(f"{response}:{answer}\n")
                elif response.startswith("Filtered Points"):
                    pairs = answer[1:].strip("[]").split("], [")
                    coordinates = [list(map(int, pair.split(", "))) for pair in pairs]
                    path = filter_collision_path(current, coordinates, object[4:])   
                    answer = str(path)[1:-1]             
                    prompt += response + ": " + answer + "\n"
                    print(f"{response}: {answer}")
                    file.write(f"{response}: {answer}\n")
                elif response.startswith("Final Path"):
                    prompt += response + ":"
                    answer = self.gpt.ask(prompt, stop=["\n", ":"], max_tokens=100)
                    print(f"{response}:{answer}\n")
                    file.write(f"{response}:{answer}\n\n")
                    break
                else:
                    prompt += response + "\n"
                    print(f"{response}")
                    file.write(f"{response}\n")
                time.sleep(3)
        path = list_parse(answer)
        print(f"PATH> {path}\n")
        
        path = [(point[0], point[1]) for point in path]
        
        return path


    def gpt_chat(self, query, object):   
        prompt = ""     
        with open('outcome/RePE/chat_history.txt', 'a+') as file:
            file.write(f"\nCHAT-{self.gpt.id}\n")
            question = colors.YELLOW + "User> " + colors.ENDC
            print(f"\n{question}{query}\n")
            file.write(f"User> {query}\n")
            answer = colors.RED + "GPT> " + colors.ENDC
            print(f"{answer}")
            file.write(f"GPT>\n")
            current = [object[0], object[1]]
            while True:
                response = self.gpt.chat(query=query, prompt=prompt, stop=["\n", ":"], max_tokens=100)
                if response.startswith("Generated Points"):
                    prompt += response + ": "
                    answer = self.gpt.chat(query=query, prompt=prompt, stop=["\n", ":"], max_tokens=100)
                    prompt += answer + "\n"
                    print(f"{response}: {answer}")
                    file.write(f"{response}:{answer}\n")
                elif response.startswith("Current Path"):
                    prompt += response + ": "
                    answer = self.gpt.chat(query=query, prompt=prompt, stop=["\n", ":"], max_tokens=100)
                    prompt += answer + "\n"
                    print(f"{response}: {answer}")
                    file.write(f"{response}:{answer}\n")
                elif response.startswith("Arrival Check"):
                    prompt += response + ": "
                    answer = "Yes" if current[0] == object[2] and current[1] == object[3] else "No"
                    prompt += answer + "\n"
                    print(f"{response}: {answer}")
                    file.write(f"{response}: {answer}\n")
                elif response.startswith("Selected Point"):
                    prompt += response + ": "
                    answer = self.gpt.chat(query=query, prompt=prompt, stop=["\n", ":"], max_tokens=100)
                    prompt += answer + "\n"
                    current = json.loads(answer)
                    print(f"{response}: {answer}")
                    file.write(f"{response}: {answer}\n")
                elif response.startswith("Filtered Points"):
                    pairs = answer.strip("[]").split("], [")
                    coordinates = [list(map(int, pair.split(", "))) for pair in pairs]
                    path = filter_collision_path(current, coordinates, object[4:])   
                    answer = str(path)[1:-1]             
                    prompt += response + ": " + answer + "\n"
                    print(f"{response}: {answer}")
                    file.write(f"{response}: {answer}\n")
                elif response.startswith("Final Path"):
                    prompt += response + ": "
                    answer = self.gpt.chat(query=query, prompt=prompt, stop=["\n", ":"], max_tokens=100)
                    print(f"{response}: {answer}\n")
                    file.write(f"{response}: {answer}\n\n")
                    break
                else:
                    prompt += response + "\n"
                    print(f"{response}")
                    file.write(f"{response}\n")
                # time.sleep(3)
        path = list_parse(answer)
        print(f"PATH> {path}\n")
        
        path = [(point[0], point[1]) for point in path]
        
        return path

