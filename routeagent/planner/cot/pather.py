from ...utils.utils import parse, colors, list_parse
from ...model.chatgpt import ChatGPT

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
        sysprompt = """You are an AI assistant specialized in planning collision-free paths for drones in a two-dimensional environment. You will be given a specific start point, end points and circular obstable position with size. Your task is to calculate a path from the start point to the end point that avoids any circular, static obstacles.  Your solution should be a sequence of points in the format of [[x1, y1], [x2, y2], ..., [xn, yn]], forming a safe and efficient route to ensure collision-free movement. The path should be a series of straight lines between consecutive points, avoiding all circular obstacles' areas. """
        example =  {
            "repe_0" : "design a path from [10, 0] to [0, 10] that avoids crossing the area of circle centered at [5, 5] with a radius of 4.\n> First Iteration:\n- Generated point: [10, 10]\nDoes path from [10, 0] to [10, 10] cross the range of circular obstacle centered at [5, 5] with a radius of 4?\nNo, so path is valid.\n- Modified path: [[10, 0], [10, 10]]\nIs the path reaching the end point at [0, 10]?\nNo, so we move on next iteration.\n> Second Iteration:\n- Generated point: [0, 10]\nDoes path from [10, 10] to [0, 10] cross the range of circular obstacle centered at [5, 5] with a radius of 4?\nNo, so path is valid.\n- Modified path: [[10, 0], [10, 10], [0, 10]]\nIs the path reaching the end point at [0, 10]?\nYes, so we return the final path.\nFinal answer:   [[10, 0], [10, 10], [0, 10]]\n\n",
            "repe_1" : "design a path from [80, 40] to [-10, 10] that avoids crossing the area of circle centered at [32, 32] with a radius of 30.\n> First Iteration:\n- Generated point: [80, 10]\nDoes the path from [80, 40] to [80, 10] cross the range of circular obstacle centered at [32, 32] with a radius of 30?\nNo, so path is valid.\n- Modified path: [[80, 40], [80, 10]]\nIs the path reaching the end point at [-10, 10]?\nNo, so we move on next iteration.\n> Second Iteration:\n- Generated point: [-10, 10]\nDoes the path from [80, 10] to [-10, 10] cross the range of circular obstacle centered at [32, 32] with a radius of 30?\nYes, so path is invalid, so we remove [-10, 10] from the path.\n- Modified path: [[80, 40], [80, 10]]\nIs the path reaching the end point at [-10, 10]?\nNo, so we move on next iteration.\n> Third Iteration:\n- Generated point: [45, 0]\nDoes the path from [80, 10] to [45, 0] cross the range of circular obstacle centered at [32, 32] with a radius of 30?\n No, so path is valid.\n- Modified path: [[80, 40], [80, 10], [45, 0]]\nIs the path reaching the end point at [-10, 10]?\nNo, so we move on next iteration.\n> Fourth Iteration:\n- Generated point: [-10, 10]\nDoes the path from [45, 0] to [-10, 10] cross the range of circular obstacle centered at [32, 32] with a radius of 30?\nYes, so path is invalid, so we remove [-10, 10] from the path.\n- Modified path: [[80, 40], [80, 10], [45, 0]]\nIs the path reaching the end point at [-10, 10]?\n No, so we move on next iteration.\n> Fifth Iteration:\n- Generated point: [20, 0]\nDoes the path from [45, 0] to [20, 10] cross the range of circular obstacle centered at [32, 32] with a radius of 30?\nNo, so path is valid.\n- Modified path: [[80, 40], [80, 10], [45, 0], [20, 0]]\nIs the path reaching the end point at [-10, 10]?\nNo, so we move on next iteration.\n> Sixth Iteration:\n- Generated point: [-10, 10]\nDoes the path from [20, 0] to [-10, 10] cross the range of circular obstacle centered at [32, 32] with a radius of 30?\n No, so path is valid.\n- Modified path: [[80, 40], [80, 10], [45, 0], [20, 0], [-10, 10]]\nIs the path reaching the end point at [-10, 10]?\nYes, so we return the final path.\nFinal answer:  [[80, 40], [80, 10], [45, 0], [20, 0], [-10, 10]]\n\n",
            "repe_2" : "design a path from [-2, 27] to [3, -50] that avoids crossing the area of circle centered at [-19, 6] with a radius of 23.68112539820996.\n> First Iteration:\n- Generated point: [-2, -50]\nDoes path from [-2, 27] to [-2, -50] cross the range of circular obstacle centered at [-19, 6] with a radius of 23.68112539820996?\nYes, so path is invalid.\n- Modified path: [[-2, 27]]\nIs the path reaching the end point at [3, -50]?\nNo, so we move on next iteration.\n> Second Iteration:\n- Generated point: [20, 0]\nDoes path from [-2, 27] to [20, 0] cross the range of circular obstacle centered at [-19, 6] with a radius of 23.68112539820996?\nNo, so path is valid.\n- Modified path: [[-2, 27], [20, 0]]\nIs the path reaching the end point at [3, -50]?\nNo, so we move on next iteration.\n> Third Iteration:\n- Generated point: [3, -50]\nDoes path from [20, 0] to [3, -50] cross the range of circular obstacle centered at [-19, 6] with a radius of 23.68112539820996?\n No, so path is valid.\n- Modified path: [[-2, 27], [20, 0], [3, -50]]\nIs the path reaching the end point at [3, -50]?\n Yes, so we return the final path.\nFinal answer:   [[-2, 27], [20, 0], [3, -50]]\n\n"
        }
        self.gpt = ChatGPT(method="RePE", sysprompt=sysprompt, example=example)


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
        with open('outcome/RePE/chat_history.txt', 'a+') as file:
            file.write(f"\nCHAT-{self.gpt.id}\n")
            
            question = colors.YELLOW + "User> " + colors.ENDC
            print(f"\n{question}{prompt}\n")
            file.write(f"User> {prompt}\n")

            response = self.gpt.ask(prompt, stop=None, max_tokens=2500)
            
            answer = colors.RED + "GPT> " + colors.ENDC
            print(f"\n{answer}\n{response}\n")
            file.write(f"GPT> {response}\n")
        
        path = list_parse(response)
        print(f"PATH> {path}\n")
        
        path = [(point[0], point[1]) for point in path]
        
        return path


