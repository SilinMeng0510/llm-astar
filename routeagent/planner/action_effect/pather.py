from ...utils.utils import parse, colors, list_parse
from ...model.chatgpt import ChatGPT
from routeagent.env import Environment

class ActionEffect():
    def __init__(self):
        sysprompt = """You are an AI assistant specialized in planning collision-free paths for drones in a two-dimensional environment. You will be given a specific start point, end points and circular obstable position with size. Your task is to calculate a path from the start point to the end point that avoids any circular, static obstacles.  Your solution should be a sequence of points in the format of [[x1, y1], [x2, y2], ..., [xn, yn]], forming a safe and efficient route to ensure collision-free movement. The path should be a series of straight lines between consecutive points, avoiding all circular obstacles' areas. """
        example = {
            "ae_1": "design a path from [10, 0] to [0, 10] that avoids crossing the area of circle centered at [5, 5] with a radius of 4.\n> search: [10, 0] and [0, 0].\nNo collision between [10, 0] and [0, 0].\n> search: [0, 0] and [0, 10].\nNo collision between [0, 0] and [0, 10].\n> finish:[[10, 0], [0, 0], [0, 10]].\n",
            "ae_2": "design a path from [80, 40] to [-10, 10] that avoids crossing the area of circle centered at [32, 32] with a radius of 30.\n> search: [80, 40] and [80, 0].\nNo collision between [80, 40] and [80, 0]. \n> search: [80, 0] and [-10, 10].\nCollision between [80, 0] and [-10, 10].\n> search: [80, 0] and [-10, 0].\nNo collision between [80, 0] and [-10, 0].\n> search: [-10, 0] and [-10, 10].\nNo collision between [-10, 0] and [-10, 10].\n> finish:[[80, 40], [80, 0], [-10, 0], [-10, 10]].\n",
            "ae_3": "design a path from [-2, 27] to [3, -50] that avoids crossing the area of circle centered at [-19, 6] with a radius of 23.\n> search: [-2, 27] and [10, 0].\nNo collision between [-2, 27] and [10, 0].\n> search: [10, 0] and [3, -50].\nNo collision between [10, 0] and [3, -50].\n> finish:[[-2, 27], [10, 0], [3, -50]].\n"
        }
        self.gpt = ChatGPT(method="AE", sysprompt=sysprompt, example=example)

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
        env = Environment(start=(object[0], object[1]), end=(object[2], object[3]), object=object[4:])
        prompt += "\n"
        while True:
            with open('outcome/AE/chat_history.txt', 'a+') as file:
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