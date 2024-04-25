from ...utils.utils import parse, colors, list_parse
from ...model.chatgpt import ChatGPT
from routeagent.env import Environment
import time


class ReAct():
    def __init__(self, correction=False):
        sysprompt = """You are an AI assistant specialized in planning collision-free paths for drones in a two-dimensional environment. You will be given a specific start point, end points and circular obstable position with size. Your task is to calculate a path from the start point to the end point that avoids any circular, static obstacles.  Your solution should be a sequence of points in the format of [[x1, y1], [x2, y2], ..., [xn, yn]], forming a safe and efficient route to ensure collision-free movement. The path should be a series of straight lines between consecutive points, avoiding all circular obstacles' areas. """
        example = {
            "react_1": "design a path from [10, 0] to [0, 10] that avoids crossing the area of circle centered at [5, 5] with a radius of 4.\n> think: To move from [10, 0] to [0, 10] while avoid crossing the area of circle centered at [5, 5] with a radius of 4, I need to find one or more points connecting [10, 0] and [0, 10] that is not in the range of circle.\nOk.\n> think: The point of [0, 0] seems not in the range of circle, and is in range of the eucliean distance of [10, 0] and [0, 10]. I can check if this path is valid.\nOK.\n> search: [10, 0] and [0, 0].\nNo collision between [10, 0] and [0, 0].\n> think: If there is no collision between [10, 0] and [0, 0], then I can reach [0, 0] and find the path to endpoint [0, 10] from [0, 0]. The circle obstacle seems not between the path between [0, 0] and [0, 10], so I can check if this path is valid.\nOk.\n> search: [0, 0] and [0, 10].\nNo collision between [0, 0] and [0, 10].\n> think: There is no obstacle between [0, 0] and [0, 10] so I can continue my move on this path and reach the goal.\nOk.\n> finish:[[10, 0], [0, 0], [0, 10]].\n",
            "react_2": "design a path from [80, 40] to [-10, 10] that avoids crossing the area of circle centered at [32, 32] with a radius of 30.\n> think: To move from [80, 40] to [-10, 10] while avoid crossing the area of circle centered at [32, 32] with a radius of 30, I need to find one or more points connecting [80, 40] and [-10, 10] that is not in the range of circle.\nOk.\n> think: Circle is on the left of start point [80, 40] and endpoint [-10, 10] is on the bottom left of start pont [80, 40]. I can first move down until out of circle's y boundary. So I can check if path to [80, 0] is valid.\nOk.\n> search: [80, 40] and [80, 0].\nNo collision between [80, 40] and [80, 0].\n> think: Now I can reach [80, 0] which is out of circle's y boundary, I may be able to directly move to the endpoint [-10, 10]. Let's check the path.\nOk.\n> search: [80, 0] and [-10, 10]\nCollision between [80, 0] and [-10, 10].\n> think: So path to [-10, 10] from [80, 0] doesn't work, then I can try directly move left to where enpoint position in x axis which is -10.\nOk.\n> search: [80, 0] and [-10, 0].\nNo collision between [80, 0] and [-10, 0].\n> think: There is no circle or obstacle between the path to the endpoint.\nOk.\n> search: [-10, 0] and [-10, 10].\nNo collision between [-10, 0] and [-10, 10].\n> think: There is no collision from [-10, 0] and [-10, 10], so I can continue the path to the endpoint [-10, 10].\nOk.\n> finish:[[80, 40], [80, 0], [-10, 0], [-10, 10]].\n",
            "react_3": "design a path from [-2, 27] to [3, -50] that avoids crossing the area of circle centered at [-19, 6] with a radius of 23.\n> think: To move from [-2, 27] to [3, -50] while avoid crossing the area of circle centered at [-19, 6] with a radius of 23, I need to find one or more points connecting [-2, 27] and [3, -50] that is not in the range of circle. Start point and end point are close to each other in x axis.\nOk.\n> think: There seems no obstacle in between the path from start point [-2, 27] to the point [10, 0]. And [10, 0] is closer to the endpoint [3, -50].\nOk.\n> search: [-2, 27] and [10, 0].\nNo collision between [-2, 27] and [10, 0].\n> think: There is no obstacle between the path from current position to endpoint. So we check the path to the endpoint.\nOk\n> search: [10, 0] and [3, -50].\nNo collision between [10, 0] and [3, -50].\n> think: So I can move directly to the endpoint [3, -50] and finish the task.\nOk.\n> finish:[[-2, 27], [10, 0], [3, -50]].\n"
        }
        self.gpt = ChatGPT(method="ReAct", sysprompt=sysprompt, example=example)
        self.correction = correction


    def run(self, command):
        self.gpt.id += 1
        
        sample = parse(command)
        
        answer = self.gpt_feed(command, sample)
        if self.gpt.id % 5 == 0:
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
            with open('outcome/ReAct/chat_history.txt', 'a+') as file:
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
                
                if check.startswith("Failed:") or env.index > 20:
                    path = [[object[0], object[1]], [object[2], object[3]]]
                    break
        
        path = [(point[0], point[1]) for point in path]
        return path