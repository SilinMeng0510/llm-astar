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