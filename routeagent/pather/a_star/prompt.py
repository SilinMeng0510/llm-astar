sysprompt_parse = """You are a code generation assistant. Your task is to convert natural language descriptions of pathfinding problems into structured JSON objects that can be used as input for a pathfinding algorithm. The input will describe start and goal points, horizontal and vertical barriers, and the boundaries of the environment. 

For each input, extract the following information and format it into a JSON object:
1. "start": The starting point coordinates as [x, y].
2. "goal": The goal point coordinates as [x, y].
3. "range_x": The minimum and maximum x-coordinates of the environment range as [x_min, x_max].
4. "range_y": The minimum and maximum y-coordinates of the environment range as [y_min, y_max].
5. "horizontal_barriers": A list of horizontal barriers, each represented as [y, x_start, x_end].
6. "vertical_barriers": A list of vertical barriers, each represented as [x, y_start, y_end].

Ensure the JSON object is properly formatted and matches the required structure."""

example_parse = {
    "sample1": 'find the shortest path from (5, 5) to (45, 25) on a 51x31 grid, avoiding horizontal barriers at [15, 10-21] and vertical barriers at [20, 0-15], [30, 15-30], and [40, 0-16].\n{"start": [5, 5], "goal": [45, 25], "range_x": [0, 51], "range_y": [0, 31], "horizontal_barriers": [[15, 10, 21]], "vertical_barriers": [[20, 0, 15], [30, 15, 30], [40, 0, 16]]}'
}

parse_llama = """
<|begin_of_text|>
<|start_header_id|>system<|end_header_id|>
You are a code generation assistant. Your task is to convert natural language descriptions of pathfinding problems into structured JSON objects that can be used as input for a pathfinding algorithm. The input will describe start and goal points, horizontal and vertical barriers, and the boundaries of the environment. 

For each input, extract the following information and format it into a JSON object:
1. "start": The starting point coordinates as [x, y].
2. "goal": The goal point coordinates as [x, y].
3. "range_x": The minimum and maximum x-coordinates of the environment range as [x_min, x_max].
4. "range_y": The minimum and maximum y-coordinates of the environment range as [y_min, y_max].
5. "horizontal_barriers": A list of horizontal barriers, each represented as [y, x_start, x_end].
6. "vertical_barriers": A list of vertical barriers, each represented as [x, y_start, y_end].

Ensure the JSON object is properly formatted, matches the required structure, and values are correctly extracted. (Do not return any comment, just the JSON)
<|eot_id|>
<|start_header_id|>user<|end_header_id|>
find the shortest path from (5, 5) to (45, 25) on a 51x31 grid, avoiding horizontal barriers at [15, 10-21] and vertical barriers at [20, 0-15], [30, 15-30], and [40, 0-16].
<|eot_id|>
<|start_header_id|>assistant<|end_header_id|>
{{"start": [5, 5], "goal": [45, 25], "range_x": [0, 51], "range_y": [0, 31], "horizontal_barriers": [[15, 10, 21]], "vertical_barriers": [[20, 0, 15], [30, 15, 30], [40, 0, 16]]}}
<|eot_id|>
<|start_header_id|>user<|end_header_id|>
design a path from [29, 4] to [22, 21] on a 51 by 31 grid that avoids horizontal barriers centered at [[7, 21, 33]] and vertical barriers at [[16, 7, 31], [39, 3, 23], [1, 24, 24]].
<|eot_id|>
<|start_header_id|>assistant<|end_header_id|>
{{'start': [29, 4], 'goal': [22, 21], 'range_x': [0, 51], 'range_y': [0, 31], 'horizontal_barriers': [[7, 21, 33]], 'vertical_barriers': [[16, 7, 31], [39, 3, 23], [1, 24, 24]]}}
<|eot_id|>
<|start_header_id|>user<|end_header_id|>
design a path from [44, 29] to [5, 23] on a 51 by 31 grid that avoids horizontal barriers centered at [[7, 21, 33]] and vertical barriers at [[16, 7, 31], [39, 3, 23], [1, 24, 24]].
<|eot_id|>
<|start_header_id|>assistant<|end_header_id|>
{{'start': [44, 29], 'goal': [5, 23], 'range_x': [0, 51], 'range_y': [0, 31], 'horizontal_barriers': [[7, 21, 33]], 'vertical_barriers': [[16, 7, 31], [39, 3, 23], [1, 24, 24]]}}
<|eot_id|>
<|start_header_id|>user<|end_header_id|>
{query}
<|eot_id|>
<|start_header_id|>assistant<|end_header_id|>
"""

prompt_gpt = """
Identify a path between the start and goal points to navigate around obstacles and find the shortest path to the goal. 
Horizontal barriers are represented as [y, x_start, x_end], and vertical barriers are represented as [x, y_start, y_end].
Conclude your response with the generated path in the format "Generated Path: [[x1, y1], [x2, y2], ...]".

Start Point: [5, 5]
Goal Point: [20, 20]
Horizontal Barriers: [[10, 0, 25], [15, 30, 50]]
Vertical Barriers: [[25, 10, 22]]
Generated Path: [[5, 5], [26, 9], [25, 23], [20, 20]]

Start Point: [2, 3]
Goal Point: [18, 8]
Horizontal Barriers: [[7, 0, 10], [5, 30, 40]]
Vertical Barriers: [[14, 12, 30], [40, 0, 11]] 
Generated Path: [[2, 3], [11, 6], [18, 8]]

Start Point: [40, 20]
Goal Point: [10, 10]
Horizontal Barriers: [[15, 20, 30], [15, 35, 50]]
Vertical Barriers: [[20, 4, 30]]
Generated Path: [[40, 20], [31, 15], [20, 3], [10, 10]]

Start Point: [4, 4]
Goal Point: [16, 16]
Horizontal Barriers: [[20, 0, 20], [5, 30, 40]]
Vertical Barriers: [[40, 0, 15], [20, 10, 21]]
Generated Path: [[4, 4], [16, 16]]

Start Point: [25, 25]
Goal Point: [4, 4]
Horizontal Barriers: [[7, 0, 20], [15, 10, 15]]
Vertical Barriers: [[10, 15, 30], [30, 0, 18], [10, 0, 5]]
Generated Path: [[25, 25], [21, 7], [10, 6], [4, 4]]

Start Point: {start}
Goal Point: {goal}
Horizontal Barriers: {horizontal_barriers}
Vertical Barriers: {vertical_barriers}
Generated Path: 
"""

prompt_llama = """
<|begin_of_text|>
<|start_header_id|>system<|end_header_id|>
You need to find the shortest path between the start and goal points that navigates around barriers. 
Horizontal barriers are represented as [y, x_start, x_end], and vertical barriers are represented as [x, y_start, y_end].
Conclude your response with the generated path in the format "Generated Path: [[x1, y1], [x2, y2], ...]".
<|eot_id|>
<|start_header_id|>user<|end_header_id|>
Start Point: [5, 5]
Goal Point: [20, 20]
Horizontal Barriers: [[10, 0, 25], [15, 30, 50]]
Vertical Barriers: [[25, 10, 22]]
<|eot_id|>
<|start_header_id|>assistant<|end_header_id|>
Generated Path: [[5, 5], [26, 9], [25, 23], [20, 20]]
<|eot_id|>
<|start_header_id|>user<|end_header_id|>
Start Point: [2, 3]
Goal Point: [18, 8]
Horizontal Barriers: [[7, 0, 10], [5, 30, 40]]
Vertical Barriers: [[14, 12, 30], [40, 0, 11]] 
<|eot_id|>
<|start_header_id|>assistant<|end_header_id|>
Generated Path: [[2, 3], [11, 6], [18, 8]]
<|eot_id|>
<|start_header_id|>user<|end_header_id|>
Start Point: [40, 20]
Goal Point: [10, 10]
Horizontal Barriers: [[15, 20, 30], [15, 35, 50]]
Vertical Barriers: [[20, 4, 30]]
<|eot_id|>
<|start_header_id|>assistant<|end_header_id|>
Generated Path: [[40, 20], [31, 15], [20, 3], [10, 10]]
<|eot_id|>
<|start_header_id|>user<|end_header_id|>
Start Point: [4, 4]
Goal Point: [16, 16]
Horizontal Barriers: [[20, 0, 20], [5, 30, 40]]
Vertical Barriers: [[40, 0, 15], [20, 10, 21]]
<|eot_id|>
<|start_header_id|>assistant<|end_header_id|>
Generated Path: [[4, 4], [16, 16]]
<|eot_id|>
<|start_header_id|>user<|end_header_id|>
Start Point: [25, 25]
Goal Point: [4, 4]
Horizontal Barriers: [[7, 0, 20], [15, 10, 15]]
Vertical Barriers: [[10, 15, 30], [30, 0, 18], [10, 0, 5]]
<|eot_id|>
<|start_header_id|>assistant<|end_header_id|>
Generated Path: [[25, 25], [21, 7], [10, 6], [4, 4]]
<|eot_id|>
<|start_header_id|>user<|end_header_id|>
Start Point: {start}
Goal Point: {goal}
Horizontal Barriers: {horizontal_barriers}
Vertical Barriers: {vertical_barriers}
<|eot_id|>
<|start_header_id|>assistant<|end_header_id|>
"""