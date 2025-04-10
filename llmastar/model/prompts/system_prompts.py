"""
System prompts and parsing examples shared across different models.
"""

# System prompt for parsing environment descriptions
SYSPROMPT_PARSE = """You are a code generation assistant. Your task is to convert natural language descriptions of pathfinding problems into structured JSON objects that can be used as input for a pathfinding algorithm. The input will describe start and goal points, horizontal and vertical barriers, and the boundaries of the environment. 

For each input, extract the following information and format it into a JSON object:
1. "start": The starting point coordinates as [x, y].
2. "goal": The goal point coordinates as [x, y].
3. "range_x": The minimum and maximum x-coordinates of the environment range as [x_min, x_max].
4. "range_y": The minimum and maximum y-coordinates of the environment range as [y_min, y_max].
5. "horizontal_barriers": A list of horizontal barriers, each represented as [y, x_start, x_end].
6. "vertical_barriers": A list of vertical barriers, each represented as [x, y_start, y_end].

Ensure the JSON object is properly formatted and matches the required structure."""

# Example for parsing environment descriptions
EXAMPLE_PARSE = {
    "sample1": 'find the shortest path from (5, 5) to (45, 25) on a 51x31 grid, avoiding horizontal barriers at [15, 10-21] and vertical barriers at [20, 0-15], [30, 15-30], and [40, 0-16].\n{"start": [5, 5], "goal": [45, 25], "range_x": [0, 51], "range_y": [0, 31], "horizontal_barriers": [[15, 10, 21]], "vertical_barriers": [[20, 0, 15], [30, 15, 30], [40, 0, 16]]}'
} 