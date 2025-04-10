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

standard_gpt = """
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

standard_llama = """
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

cot_gpt = """
Identify a path between the start and goal points to navigate around obstacles and find the shortest path to the goal. 
Horizontal barriers are represented as [y, x_start, x_end], and vertical barriers are represented as [x, y_start, y_end].
Conclude your response with the generated path in the format "Generated Path: [[x1, y1], [x2, y2], ...]".

Start Point: [5, 5]
Goal Point: [20, 20]
Horizontal Barriers: [[10, 0, 25], [15, 30, 50]]
Vertical Barriers: [[25, 10, 22]]
Thought: Identify a path from [5, 5] to [20, 20] while avoiding the horizontal barrier at y=10 spanning x=0 to x=25 by moving upwards and right, then bypass the vertical barrier at x=25 spanning y=10 to y=22, and finally move directly to [20, 20].
Generated Path: [[5, 5], [26, 9], [25, 23], [20, 20]]

Start Point: [2, 3]
Goal Point: [18, 8]
Horizontal Barriers: [[7, 0, 10], [5, 30, 40]]
Vertical Barriers: [[14, 12, 30], [40, 0, 11]]
Thought: Navigate from [2, 3] to [18, 8] by moving upward-right to avoid the horizontal barrier at y=7 spanning x=0 to x=10, then proceed directly to [18, 8].
Generated Path: [[2, 3], [11, 6], [18, 8]]

Start Point: [25, 25]
Goal Point: [4, 4]
Horizontal Barriers: [[7, 0, 20], [15, 10, 15]]
Vertical Barriers: [[10, 15, 30], [30, 0, 18], [10, 0, 5]]
Thought: Move from [25, 25] to [4, 4] by heading downward to bypass the horizontal barrier at y=7 spanning x=0 to x=20, and finally move directly to [4, 4], where bypass the vertical barrier at x=10 spanning y=0 to y=5.
Generated Path: [[25, 25], [21, 7], [10, 6], [4, 4]]

Start Point: {start}
Goal Point: {goal}
Horizontal Barriers: {horizontal_barriers}
Vertical Barriers: {vertical_barriers}
"""

cot_llama = """
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
Thought: Identify a path from [5, 5] to [20, 20] while avoiding the horizontal barrier at y=10 spanning x=0 to x=25 by moving upwards and right, then bypass the vertical barrier at x=25 spanning y=10 to y=22, and finally move directly to [20, 20].
Generated Path: [[5, 5], [26, 9], [25, 23], [20, 20]]
<|eot_id|>
<|start_header_id|>user<|end_header_id|>
Start Point: [2, 3]
Goal Point: [18, 8]
Horizontal Barriers: [[7, 0, 10], [5, 30, 40]]
Vertical Barriers: [[14, 12, 30], [40, 0, 11]] 
<|eot_id|>
<|start_header_id|>assistant<|end_header_id|>
Thought: Navigate from [2, 3] to [18, 8] by moving upward-right to avoid the horizontal barrier at y=7 spanning x=0 to x=10, then proceed directly to [18, 8].
Generated Path: [[2, 3], [11, 6], [18, 8]]
<|eot_id|>
<|start_header_id|>user<|end_header_id|>
Start Point: [25, 25]
Goal Point: [4, 4]
Horizontal Barriers: [[7, 0, 20], [15, 10, 15]]
Vertical Barriers: [[10, 15, 30], [30, 0, 18], [10, 0, 5]]
<|eot_id|>
<|start_header_id|>assistant<|end_header_id|>
Thought: Move from [25, 25] to [4, 4] by heading downward to bypass the horizontal barrier at y=7 spanning x=0 to x=20, and finally move directly to [4, 4], where bypass the vertical barrier at x=10 spanning y=0 to y=5.
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

repe_gpt = """
Identify a path between the start and goal points to navigate around obstacles and find the shortest path to the goal. 
Horizontal barriers are represented as [y, x_start, x_end], and vertical barriers are represented as [x, y_start, y_end].
Conclude your response with the generated path in the format "Generated Path: [[x1, y1], [x2, y2], ...]".

Start Point: [5, 5]
Goal Point: [20, 20]
Horizontal Barriers: [[10, 0, 25], [15, 30, 50]]
Vertical Barriers: [[25, 10, 22]]
- First Iteration on [5, 5]
Thought: The horizontal barrier at y=10 spanning x=0 to x=25 blocks the direct path to the goal. To navigate around it, we should move to the upper-right corner of the barrier.
Selected Point: [26, 9]
Evaluation: The selected point [26, 9] effectively bypasses the horizontal barrier, positioning us at its corner and maintaining progress toward the goal without encountering additional obstacles.
- Second Iteration on [26, 9]
Thought: Now that we have bypassed the horizontal barrier, the path to the goal seems clear.
Selected Point: [20, 20]
Evaluation: The path is obstructed by the vertical barrier, leading to a collision. A more effective route involves moving around this vertical barrier.
Thought: To bypass the vertical barrier at x=25, we should move along its length and then turn around it to continue toward the goal.
Selected Point: [25, 23]
Evaluation: The selected point [25, 23] successfully avoids the vertical barrier and brings us closer to the goal without encountering further obstacles.
- Third Iteration on [25, 23]
Thought: From this position, there are no barriers directly obstructing the path to the goal.
Selected Point: [20, 20]
Evaluation: The path to the goal is clear from here, allowing a direct move to the goal.
Generated Path: [[5, 5], [26, 9], [25, 23], [20, 20]]

Start Point: [2, 3]
Goal Point: [18, 8]
Horizontal Barriers: [[7, 0, 10], [5, 30, 40]]
Vertical Barriers: [[14, 12, 30], [40, 0, 11]]
- First Iteration on [2, 3]
Thought: The horizontal barrier at y=7 spanning x=0 to x=10 obstructs the direct path. To bypass it, move to the end of the barrier.
Selected Point: [11, 6]
Evaluation: The point [11, 6] navigates around the horizontal barrier, positioning us at its edge and closer to the goal.
- Second Iteration on [11, 6]
Thought: With the barrier behind us, the path to the goal is clear, allowing us to proceed directly to the goal.
Selected Point: [18, 8]
Evaluation: The path is unobstructed from here to the goal, enabling a straightforward move to [18, 8].
Generated Path: [[2, 3], [11, 6], [18, 8]]

Start Point: [25, 25]
Goal Point: [4, 4]
Horizontal Barriers: [[7, 0, 20], [15, 10, 15]]
Vertical Barriers: [[10, 15, 30], [30, 0, 18], [10, 0, 5]]
- First Iteration on [25, 25]
Thought: The horizontal barrier at y=15 spanning x=10 to x=15 blocks the direct path. To avoid it, we should move downward and then navigate around it.
Selected Point: [10, 10]
Evaluation: Moving to [10, 10] positions us midway toward a different horizontal barrier at y=7 spanning x=0 to x=20, which may unnecessarily increase path length.
Thought: To bypass the horizontal barrier at y=7, we need to move downward until we clear its end.
Selected Point: [21, 7]
Evaluation: The selected point [21, 7] successfully clears the horizontal barrier at y=7, setting us up for a more direct path to the goal.
- Second Iteration on [21, 7]
Thought: The vertical barrier at x=10 spanning y=0 to y=5 obstructs the direct path. We should navigate around it.
Selected Point: [10, 6]
Evaluation: The point [10, 6] effectively bypasses the vertical barrier, bringing us closer to the goal.
- Third Iteration on [10, 6]
Thought: There are no obstacles between the current position and the goal, allowing a direct move to the goal.
Selected Point: [4, 4]
Evaluation: The path to the goal is clear from here, permitting a direct move to [4, 4].
Generated Path: [[25, 25], [21, 7], [10, 6], [4, 4]]

Start Point: {start}
Goal Point: {goal}
Horizontal Barriers: {horizontal_barriers}
Vertical Barriers: {vertical_barriers}
"""

repe_llama = """
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
- First Iteration on [5, 5]
Thought: The horizontal barrier at y=10 spanning x=0 to x=25 blocks the direct path to the goal. To navigate around it, we should move to the upper-right corner of the barrier.
Selected Point: [26, 9]
Evaluation: The selected point [26, 9] effectively bypasses the horizontal barrier, positioning us at its corner and maintaining progress toward the goal without encountering additional obstacles.
- Second Iteration on [26, 9]
Thought: Now that we have bypassed the horizontal barrier, the path to the goal seems clear.
Selected Point: [20, 20]
Evaluation: The path is obstructed by the vertical barrier, leading to a collision. A more effective route involves moving around this vertical barrier.
Thought: To bypass the vertical barrier at x=25, we should move along its length and then turn around it to continue toward the goal.
Selected Point: [25, 23]
Evaluation: The selected point [25, 23] successfully avoids the vertical barrier and brings us closer to the goal without encountering further obstacles.
- Third Iteration on [25, 23]
Thought: From this position, there are no barriers directly obstructing the path to the goal.
Selected Point: [20, 20]
Evaluation: The path to the goal is clear from here, allowing a direct move to the goal.
Generated Path: [[5, 5], [26, 9], [25, 23], [20, 20]]
<|eot_id|>
<|start_header_id|>user<|end_header_id|>
Start Point: [2, 3]
Goal Point: [18, 8]
Horizontal Barriers: [[7, 0, 10], [5, 30, 40]]
Vertical Barriers: [[14, 12, 30], [40, 0, 11]] 
<|eot_id|>
<|start_header_id|>assistant<|end_header_id|>
- First Iteration on [2, 3]
Thought: The horizontal barrier at y=7 spanning x=0 to x=10 obstructs the direct path. To bypass it, move to the end of the barrier.
Selected Point: [11, 6]
Evaluation: The point [11, 6] navigates around the horizontal barrier, positioning us at its edge and closer to the goal.
- Second Iteration on [11, 6]
Thought: With the barrier behind us, the path to the goal is clear, allowing us to proceed directly to the goal.
Selected Point: [18, 8]
Evaluation: The path is unobstructed from here to the goal, enabling a straightforward move to [18, 8].
Generated Path: [[2, 3], [11, 6], [18, 8]]
<|eot_id|>
<|start_header_id|>user<|end_header_id|>
Start Point: [25, 25]
Goal Point: [4, 4]
Horizontal Barriers: [[7, 0, 20], [15, 10, 15]]
Vertical Barriers: [[10, 15, 30], [30, 0, 18], [10, 0, 5]]
<|eot_id|>
<|start_header_id|>assistant<|end_header_id|>
- First Iteration on [25, 25]
Thought: The horizontal barrier at y=15 spanning x=10 to x=15 blocks the direct path. To avoid it, we should move downward and then navigate around it.
Selected Point: [10, 10]
Evaluation: Moving to [10, 10] positions us midway toward a different horizontal barrier at y=7 spanning x=0 to x=20, which may unnecessarily increase path length.
Thought: To bypass the horizontal barrier at y=7, we need to move downward until we clear its end.
Selected Point: [21, 7]
Evaluation: The selected point [21, 7] successfully clears the horizontal barrier at y=7, setting us up for a more direct path to the goal.
- Second Iteration on [21, 7]
Thought: The vertical barrier at x=10 spanning y=0 to y=5 obstructs the direct path. We should navigate around it.
Selected Point: [10, 6]
Evaluation: The point [10, 6] effectively bypasses the vertical barrier, bringing us closer to the goal.
- Third Iteration on [10, 6]
Thought: There are no obstacles between the current position and the goal, allowing a direct move to the goal.
Selected Point: [4, 4]
Evaluation: The path to the goal is clear from here, permitting a direct move to [4, 4].
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

# RAG-specific prompts
standard_gpt_rag = """
You are provided with a barrier description based on a similar pathfinding problem:
{retrieved_barrier}

Additionally, you have an example of a successful path for navigating around similar barriers:
{retrieved_path}

Identify a path between the start and goal points to navigate around obstacles and find the shortest path to the goal. 
Horizontal barriers are represented as [y, x_start, x_end], and vertical barriers are represented as [x, y_start, y_end].
Conclude your response with the generated path in the format "Generated Path: [[x1, y1], [x2, y2], ...]".

Start Point: {start}
Goal Point: {goal}
Horizontal Barriers: {horizontal_barriers}
Vertical Barriers: {vertical_barriers}
Generated Path: 
"""

standard_llama_rag = """
<|begin_of_text|>
<|start_header_id|>system<|end_header_id|>
You are provided with a barrier description based on a similar pathfinding problem:
{retrieved_barrier}

Additionally, you have an example of a successful path for navigating around similar barriers:
{retrieved_path}

You need to find the shortest path between the start and goal points that navigates around barriers. 
Horizontal barriers are represented as [y, x_start, x_end], and vertical barriers are represented as [x, y_start, y_end].
Conclude your response with the generated path in the format "Generated Path: [[x1, y1], [x2, y2], ...]".
<|eot_id|>
<|start_header_id|>user<|end_header_id|>
Start Point: {start}
Goal Point: {goal}
Horizontal Barriers: {horizontal_barriers}
Vertical Barriers: {vertical_barriers}
<|eot_id|>
<|start_header_id|>assistant<|end_header_id|>
"""

cot_gpt_rag = """
You are provided with a barrier description based on a similar pathfinding problem:
{retrieved_barrier}

Additionally, you have an example of a successful path for navigating around similar barriers:
{retrieved_path}

Identify a path between the start and goal points to navigate around obstacles and find the shortest path to the goal. 
Horizontal barriers are represented as [y, x_start, x_end], and vertical barriers are represented as [x, y_start, y_end].
Think step by step about how to navigate around the barriers efficiently.
Conclude your response with the generated path in the format "Generated Path: [[x1, y1], [x2, y2], ...]".

Start Point: {start}
Goal Point: {goal}
Horizontal Barriers: {horizontal_barriers}
Vertical Barriers: {vertical_barriers}
Thought: 
"""

cot_llama_rag = """
<|begin_of_text|>
<|start_header_id|>system<|end_header_id|>
You are provided with a barrier description based on a similar pathfinding problem:
{retrieved_barrier}

Additionally, you have an example of a successful path for navigating around similar barriers:
{retrieved_path}

You need to find the shortest path between the start and goal points that navigates around barriers. 
Horizontal barriers are represented as [y, x_start, x_end], and vertical barriers are represented as [x, y_start, y_end].
Think step by step about how to navigate around the barriers efficiently.
Conclude your response with the generated path in the format "Generated Path: [[x1, y1], [x2, y2], ...]".
<|eot_id|>
<|start_header_id|>user<|end_header_id|>
Start Point: {start}
Goal Point: {goal}
Horizontal Barriers: {horizontal_barriers}
Vertical Barriers: {vertical_barriers}
<|eot_id|>
<|start_header_id|>assistant<|end_header_id|>
Thought: 
"""

repe_gpt_rag = """
You are provided with a barrier description based on a similar pathfinding problem:
{retrieved_barrier}

Additionally, you have an example of a successful path for navigating around similar barriers:
{retrieved_path}

Identify a path between the start and goal points to navigate around obstacles and find the shortest path to the goal. 
Horizontal barriers are represented as [y, x_start, x_end], and vertical barriers are represented as [x, y_start, y_end].
For each iteration point, analyze the barriers, select a next point, and evaluate your choice.
Conclude your response with the generated path in the format "Generated Path: [[x1, y1], [x2, y2], ...]".

Start Point: {start}
Goal Point: {goal}
Horizontal Barriers: {horizontal_barriers}
Vertical Barriers: {vertical_barriers}
- First Iteration on {start}
Thought: 
"""

repe_llama_rag = """
<|begin_of_text|>
<|start_header_id|>system<|end_header_id|>
You are provided with a barrier description based on a similar pathfinding problem:
{retrieved_barrier}

Additionally, you have an example of a successful path for navigating around similar barriers:
{retrieved_path}

You need to find the shortest path between the start and goal points that navigates around barriers.
Horizontal barriers are represented as [y, x_start, x_end], and vertical barriers are represented as [x, y_start, y_end].
For each iteration point, analyze the barriers, select a next point, and evaluate your choice.
Conclude your response with the generated path in the format "Generated Path: [[x1, y1], [x2, y2], ...]".
<|eot_id|>
<|start_header_id|>user<|end_header_id|>
Start Point: {start}
Goal Point: {goal}
Horizontal Barriers: {horizontal_barriers}
Vertical Barriers: {vertical_barriers}
<|eot_id|>
<|start_header_id|>assistant<|end_header_id|>
- First Iteration on {start}
Thought: 
"""

# Update prompt dictionaries to include RAG versions
gpt_prompt = {'standard': standard_gpt, 'cot': cot_gpt, 'repe': repe_gpt}
llama_prompt = {'standard': standard_llama, 'cot': cot_llama, 'repe': repe_llama}
gpt_prompt_rag = {'standard': standard_gpt_rag, 'cot': cot_gpt_rag, 'repe': repe_gpt_rag}
llama_prompt_rag = {'standard': standard_llama_rag, 'cot': cot_llama_rag, 'repe': repe_llama_rag}

parse_qwen = """
<|im_start|>system
You are a code generation assistant. Your task is to convert natural language descriptions of pathfinding problems into structured JSON objects that can be used as input for a pathfinding algorithm. The input will describe start and goal points, horizontal and vertical barriers, and the boundaries of the environment. 

For each input, extract the following information and format it into a JSON object:
1. "start": The starting point coordinates as [x, y].
2. "goal": The goal point coordinates as [x, y].
3. "range_x": The minimum and maximum x-coordinates of the environment range as [x_min, x_max].
4. "range_y": The minimum and maximum y-coordinates of the environment range as [y_min, y_max].
5. "horizontal_barriers": A list of horizontal barriers, each represented as [y, x_start, x_end].
6. "vertical_barriers": A list of vertical barriers, each represented as [x, y_start, y_end].

Ensure the JSON object is properly formatted, matches the required structure, and values are correctly extracted. (Do not return any comment, just the JSON)
<|im_end|>
<|im_start|>user
find the shortest path from (5, 5) to (45, 25) on a 51x31 grid, avoiding horizontal barriers at [15, 10-21] and vertical barriers at [20, 0-15], [30, 15-30], and [40, 0-16].
<|im_end|>
<|im_start|>assistant
{"start": [5, 5], "goal": [45, 25], "range_x": [0, 51], "range_y": [0, 31], "horizontal_barriers": [[15, 10, 21]], "vertical_barriers": [[20, 0, 15], [30, 15, 30], [40, 0, 16]]}
<|im_end|>
<|im_start|>user
design a path from [29, 4] to [22, 21] on a 51 by 31 grid that avoids horizontal barriers centered at [[7, 21, 33]] and vertical barriers at [[16, 7, 31], [39, 3, 23], [1, 24, 24]].
<|im_end|>
<|im_start|>assistant
{'start': [29, 4], 'goal': [22, 21], 'range_x': [0, 51], 'range_y': [0, 31], 'horizontal_barriers': [[7, 21, 33]], 'vertical_barriers': [[16, 7, 31], [39, 3, 23], [1, 24, 24]]}
<|im_end|>
<|im_start|>user
design a path from [44, 29] to [5, 23] on a 51 by 31 grid that avoids horizontal barriers centered at [[7, 21, 33]] and vertical barriers at [[16, 7, 31], [39, 3, 23], [1, 24, 24]].
<|im_end|>
<|im_start|>assistant
{'start': [44, 29], 'goal': [5, 23], 'range_x': [0, 51], 'range_y': [0, 31], 'horizontal_barriers': [[7, 21, 33]], 'vertical_barriers': [[16, 7, 31], [39, 3, 23], [1, 24, 24]]}
<|im_end|>
<|im_start|>user
{query}
<|im_end|>
<|im_start|>assistant
"""

standard_qwen = """
<|im_start|>system
You need to find the shortest path between the start and goal points that navigates around barriers. 
Horizontal barriers are represented as [y, x_start, x_end], and vertical barriers are represented as [x, y_start, y_end].
Conclude your response with the generated path in the format "Generated Path: [[x1, y1], [x2, y2], ...]".
<|im_end|>
<|im_start|>user
Start Point: [5, 5]
Goal Point: [20, 20]
Horizontal Barriers: [[10, 0, 25], [15, 30, 50]]
Vertical Barriers: [[25, 10, 22]]
<|im_end|>
<|im_start|>assistant
Generated Path: [[5, 5], [26, 9], [25, 23], [20, 20]]
<|im_end|>
<|im_start|>user
Start Point: [2, 3]
Goal Point: [18, 8]
Horizontal Barriers: [[7, 0, 10], [5, 30, 40]]
Vertical Barriers: [[14, 12, 30], [40, 0, 11]] 
<|im_end|>
<|im_start|>assistant
Generated Path: [[2, 3], [11, 6], [18, 8]]
<|im_end|>
<|im_start|>user
Start Point: [40, 20]
Goal Point: [10, 10]
Horizontal Barriers: [[15, 20, 30], [15, 35, 50]]
Vertical Barriers: [[20, 4, 30]]
<|im_end|>
<|im_start|>assistant
Generated Path: [[40, 20], [31, 15], [20, 3], [10, 10]]
<|im_end|>
<|im_start|>user
Start Point: [4, 4]
Goal Point: [16, 16]
Horizontal Barriers: [[20, 0, 20], [5, 30, 40]]
Vertical Barriers: [[40, 0, 15], [20, 10, 21]]
<|im_end|>
<|im_start|>assistant
Generated Path: [[4, 4], [16, 16]]
<|im_end|>
<|im_start|>user
Start Point: [25, 25]
Goal Point: [4, 4]
Horizontal Barriers: [[7, 0, 20], [15, 10, 15]]
Vertical Barriers: [[10, 15, 30], [30, 0, 18], [10, 0, 5]]
<|im_end|>
<|im_start|>assistant
Generated Path: [[25, 25], [21, 7], [10, 6], [4, 4]]
<|im_end|>
<|im_start|>user
Start Point: {start}
Goal Point: {goal}
Horizontal Barriers: {horizontal_barriers}
Vertical Barriers: {vertical_barriers}
<|im_end|>
<|im_start|>assistant
"""

cot_qwen = """
<|im_start|>system
You need to find the shortest path between the start and goal points that navigates around barriers. 
Horizontal barriers are represented as [y, x_start, x_end], and vertical barriers are represented as [x, y_start, y_end].
Conclude your response with the generated path in the format "Generated Path: [[x1, y1], [x2, y2], ...]".
<|im_end|>
<|im_start|>user
Start Point: [5, 5]
Goal Point: [20, 20]
Horizontal Barriers: [[10, 0, 25], [15, 30, 50]]
Vertical Barriers: [[25, 10, 22]]
<|im_end|>
<|im_start|>assistant
Thought: Identify a path from [5, 5] to [20, 20] while avoiding the horizontal barrier at y=10 spanning x=0 to x=25 by moving upwards and right, then bypass the vertical barrier at x=25 spanning y=10 to y=22, and finally move directly to [20, 20].
Generated Path: [[5, 5], [26, 9], [25, 23], [20, 20]]
<|im_end|>
<|im_start|>user
Start Point: [2, 3]
Goal Point: [18, 8]
Horizontal Barriers: [[7, 0, 10], [5, 30, 40]]
Vertical Barriers: [[14, 12, 30], [40, 0, 11]] 
<|im_end|>
<|im_start|>assistant
Thought: Navigate from [2, 3] to [18, 8] by moving upward-right to avoid the horizontal barrier at y=7 spanning x=0 to x=10, then proceed directly to [18, 8].
Generated Path: [[2, 3], [11, 6], [18, 8]]
<|im_end|>
<|im_start|>user
Start Point: [25, 25]
Goal Point: [4, 4]
Horizontal Barriers: [[7, 0, 20], [15, 10, 15]]
Vertical Barriers: [[10, 15, 30], [30, 0, 18], [10, 0, 5]]
<|im_end|>
<|im_start|>assistant
Thought: Move from [25, 25] to [4, 4] by heading downward to bypass the horizontal barrier at y=7 spanning x=0 to x=20, and finally move directly to [4, 4], where bypass the vertical barrier at x=10 spanning y=0 to y=5.
Generated Path: [[25, 25], [21, 7], [10, 6], [4, 4]]
<|im_end|>
<|im_start|>user
Start Point: {start}
Goal Point: {goal}
Horizontal Barriers: {horizontal_barriers}
Vertical Barriers: {vertical_barriers}
<|im_end|>
<|im_start|>assistant
"""

repe_qwen = """
<|im_start|>system
You need to find the shortest path between the start and goal points that navigates around barriers. 
Horizontal barriers are represented as [y, x_start, x_end], and vertical barriers are represented as [x, y_start, y_end].
Conclude your response with the generated path in the format "Generated Path: [[x1, y1], [x2, y2], ...]".
<|im_end|>
<|im_start|>user
Start Point: [5, 5]
Goal Point: [20, 20]
Horizontal Barriers: [[10, 0, 25], [15, 30, 50]]
Vertical Barriers: [[25, 10, 22]]
<|im_end|>
<|im_start|>assistant
- First Iteration on [5, 5]
Thought: The horizontal barrier at y=10 spanning x=0 to x=25 blocks the direct path to the goal. To navigate around it, we should move to the upper-right corner of the barrier.
Selected Point: [26, 9]
Evaluation: The selected point [26, 9] effectively bypasses the horizontal barrier, positioning us at its corner and maintaining progress toward the goal without encountering additional obstacles.
- Second Iteration on [26, 9]
Thought: Now that we have bypassed the horizontal barrier, the path to the goal seems clear.
Selected Point: [20, 20]
Evaluation: The path is obstructed by the vertical barrier, leading to a collision. A more effective route involves moving around this vertical barrier.
Thought: To bypass the vertical barrier at x=25, we should move along its length and then turn around it to continue toward the goal.
Selected Point: [25, 23]
Evaluation: The selected point [25, 23] successfully avoids the vertical barrier and brings us closer to the goal without encountering further obstacles.
- Third Iteration on [25, 23]
Thought: From this position, there are no barriers directly obstructing the path to the goal.
Selected Point: [20, 20]
Evaluation: The path to the goal is clear from here, allowing a direct move to the goal.
Generated Path: [[5, 5], [26, 9], [25, 23], [20, 20]]
<|im_end|>
<|im_start|>user
Start Point: [2, 3]
Goal Point: [18, 8]
Horizontal Barriers: [[7, 0, 10], [5, 30, 40]]
Vertical Barriers: [[14, 12, 30], [40, 0, 11]] 
<|im_end|>
<|im_start|>assistant
- First Iteration on [2, 3]
Thought: The horizontal barrier at y=7 spanning x=0 to x=10 obstructs the direct path. To bypass it, move to the end of the barrier.
Selected Point: [11, 6]
Evaluation: The point [11, 6] navigates around the horizontal barrier, positioning us at its edge and closer to the goal.
- Second Iteration on [11, 6]
Thought: With the barrier behind us, the path to the goal is clear, allowing us to proceed directly to the goal.
Selected Point: [18, 8]
Evaluation: The path is unobstructed from here to the goal, enabling a straightforward move to [18, 8].
Generated Path: [[2, 3], [11, 6], [18, 8]]
<|im_end|>
<|im_start|>user
Start Point: [25, 25]
Goal Point: [4, 4]
Horizontal Barriers: [[7, 0, 20], [15, 10, 15]]
Vertical Barriers: [[10, 15, 30], [30, 0, 18], [10, 0, 5]]
<|im_end|>
<|im_start|>assistant
- First Iteration on [25, 25]
Thought: The horizontal barrier at y=15 spanning x=10 to x=15 blocks the direct path. To avoid it, we should move downward and then navigate around it.
Selected Point: [10, 10]
Evaluation: Moving to [10, 10] positions us midway toward a different horizontal barrier at y=7 spanning x=0 to x=20, which may unnecessarily increase path length.
Thought: To bypass the horizontal barrier at y=7, we need to move downward until we clear its end.
Selected Point: [21, 7]
Evaluation: The selected point [21, 7] successfully clears the horizontal barrier at y=7, setting us up for a more direct path to the goal.
- Second Iteration on [21, 7]
Thought: The vertical barrier at x=10 spanning y=0 to y=5 obstructs the direct path. We should navigate around it.
Selected Point: [10, 6]
Evaluation: The point [10, 6] effectively bypasses the vertical barrier, bringing us closer to the goal.
- Third Iteration on [10, 6]
Thought: There are no obstacles between the current position and the goal, allowing a direct move to the goal.
Selected Point: [4, 4]
Evaluation: The path to the goal is clear from here, permitting a direct move to [4, 4].
Generated Path: [[25, 25], [21, 7], [10, 6], [4, 4]]
<|im_end|>
<|im_start|>user
Start Point: {start}
Goal Point: {goal}
Horizontal Barriers: {horizontal_barriers}
Vertical Barriers: {vertical_barriers}
<|im_end|>
<|im_start|>assistant
"""

qwen_prompt = {'standard': standard_qwen, 'cot': cot_qwen, 'repe': repe_qwen}