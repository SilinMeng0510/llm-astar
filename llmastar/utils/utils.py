import re, ast, os, subprocess, base64, json

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

def extract_python_code(content):
    code_block_regex = re.compile(r"```(.*?)```", re.DOTALL)
    code_blocks = code_block_regex.findall(content)
    if code_blocks:
        full_code = "\n".join(code_blocks)
        if full_code.startswith("python"):
            full_code = full_code[7:]
        return full_code
    else:
        return None

def create_run_delete_file(code):
    # Step 1: Write the Python code to a file
    filename = 'temp_script.py'
    with open(filename, 'w') as file:
        file.write(code)

    # Step 2: Run the Python file and capture its output
    try:
        result = subprocess.run(['python', filename], text=True, capture_output=True)
    except Exception as e:
        print("Error running the script:", e)

    # Step 3: Remove the file after execution
    try:
        os.remove(filename)
    except OSError as e:
        print("Error removing the file:", e)
    
    return "Yes, so path is invalid." if bool(result.stdout) else "No, so path is valid."

def parse_selected_point(output_text):
    # Use regular expressions to find the coordinates of the selected point
    match = re.search(r'Selected Point\s*:\s*\[\s*([\d.]+)\s*,\s*([\d.]+)\s*\]', output_text)
    if match:
        x, y = float(match.group(1)), float(match.group(2))
        return [x, y]
    else:
        return None

def extract_json_from_text(text):
    # Use regular expression to find the JSON part of the text, including the `json` keyword
    json_match = re.search(r'```json\s*(\{.*\})\s*```', text, re.DOTALL)
    if json_match:
        json_str = json_match.group(1)  # Extract the JSON string without the ```json part
        try:
            json_data = json.loads(json_str)
            return json_data
        except json.JSONDecodeError as e:
            print(f"Failed to decode JSON: {e}")
            return None
    else:
        print("No JSON found in the text")
        return None

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')