import re
import ast

class colors:  
    RED = "\033[31m"
    ENDC = "\033[m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"

def parse(command):
    sample = re.findall(r"-?\d+\.\d+|-?\d+", command)
    sample = [float(num) if '.' in num else int(num) for num in sample] 
    return sample

def parse_search(command):
    sample = re.findall(r'\[(-?\d+),\s*(-?\d+)\]', command)
    return [(int(x), int(y)) for x, y in sample]

def list_parse(text):
    # Find the pattern of the entire list with potential expressions
    lists = re.findall(r'\[\[.*?\]\]', text, re.DOTALL)

    if lists:
        # The last found list is our target list
        last_list_str = lists[-1]

        # Replace mathematical expressions with evaluated results
        evaluated_list_str = re.sub(r'(\d+ - \d+\.\d+)', lambda x: str(eval(x.group(1))), last_list_str)

        # Convert the string representation of the list to an actual list
        try:
            evaluated_list = ast.literal_eval(evaluated_list_str)
            return evaluated_list
        except Exception as e:
            return f"Error evaluating list: {e}"
    else:
        return [[0, 0],[0, 0]]

def pack(sample):
    prompt = f"design a path from [{sample[0]}, {sample[1]}] to [{sample[2]}, {sample[3]}] that avoids crossing the area of circle centered at [{sample[4]}, {sample[5]}] with a radius of {sample[6]}."
    return {"prompt" : prompt, "sample" : sample}