sysprompt_parse = """You are a code generation assistant. Your task is to convert natural language descriptions of pathfinding problems into structured JSON objects that can be used as input for a pathfinding algorithm. The input will describe start and goal points, circular and rectangular obstacles, and the boundaries of the environment. 

For each input, extract the following information and format it into a JSON object:
1. "start": The starting point coordinates as [x, y].
2. "goal": The goal point coordinates as [x, y].
3. "range_x": The minimum and maximum x-coordinates of the environment range as [x_min, x_max].
4. "range_y": The minimum and maximum y-coordinates of the environment range as [y_min, y_max].
5. "circle_obstacles": A list of circular obstacles, each represented as [x, y, radius].
6. "rectangle_obstacles": A list of rectangular obstacles, each represented as [x, y, width, length].

Ensure the JSON object is properly formatted and matches the required structure."""

example_parse = {
    "sample1": 'Design a path from [18, 8] to [17, 18] that avoids circles centered at [7, 12] with radius 3, [46, 20] with radius 2, [15, 5] with radius 2, [37, 7] with radius 3, and [37, 23] with radius 3, as well as rectangles at [14, 12] with width 8 and length 2, [18, 22] with width 8 and length 2, [26, 7] with width 2 and length 12, and [32, 14] with width 10 and length 2. The boundary of the environment is defined by the rectangle with vertices at [0, 0], [0, 30], [50, 30], and [50, 0].\n{"start": [18, 8], "goal": [17, 18], "range_x": [0, 50], "range_y": [0, 30], "circle_obstacles": [[7, 12, 3], [46, 20, 2], [15, 5, 2], [37, 7, 3], [37, 23, 3]], "rectangle_obstacles": [[14, 12, 8, 2], [18, 22, 8, 2], [26, 7, 2, 12], [32, 14, 10, 2]]}'
}

sysprompt_generate = """You are an advanced AI model specializing in robotics and path planning algorithms. Your task is to enhance the Rapidly-exploring Random Tree (RRT) algorithm by selecting the next vertex that will contribute to generating the most efficient path towards the goal. Consider the following inputs:

1. "start": The starting point coordinates as [x, y].
2. "goal": The goal point coordinates as [x, y].
3. "range_x": The minimum and maximum x-coordinates of the environment range as [x_min, x_max].
4. "range_y": The minimum and maximum y-coordinates of the environment range as [y_min, y_max].
5. "circle_obstacles": A list of circular obstacles, each represented as [x, y, radius].
6. "rectangle_obstacles": A list of rectangular obstacles, each represented as [x, y, width, length].
7. "self.vertex": A list of generated vertices, each represented as [x, y].
8. "environment_image": An image of the current environment showing obstacles and the path.

Your objective is to analyze the current map, obstacles, vertices, and the environment image to determine the next point that optimizes the path efficiency towards the goal while avoiding obstacles. Use your understanding of geometry, spatial relationships, visual information from the image, and path planning principles to make an informed decision."""

query_generate = """Given the following inputs, the current RRT* algorithm graph, and the attached environment image:

- Start coordinates: {start} (represented by the blue dot)
- Goal coordinates: {goal} (represented by the red dot)
- Environment range (x): {range_x}
- Environment range (y): {range_y}
- Circular obstacles: {circle_obstacles} (represented by the grey shapes)
- Rectangular obstacles: {rectangle_obstacles} (represented by the grey shapes)
- Generated vertices: {vertex} (represented by the green paths)
- Environment image: [Analyze the provided image]

Analyze the provided data and image to select the next point that optimizes the path to the goal following the instruction of RRT* algorithm. Take into account factors such as the distance from the current path, the avoidance of obstacles, and the directness of the route to the goal. Use common sense and visual information to guide your decision.
Please don't select point that already exist in the Generated vertices, which is unnecessary because they are already selected.

Output the coordinates of the selected point and explain why it is considered optimal in guiding the RRT* algorithm towards the most efficient path. Conclude your response with the selected vertex coordinates in the format "**Selected Point: [x, y]**"."""

prompt = """
Identify intermediate points between the start and goal points to navigate around obstacles and find the shortest path to the goal. 
Rectangle obstacles are represented by their center coordinates, width, and length in [x, y, width, length], while circular obstacles are represented by their center coordinates and radius in [x, y, radius].
Conclude your response with the selected point coordinates in the format "Selected Point: [x, y]".

Start Point: 
Goal Point:
Rectangle Obstacles: 
Circular Obsatcles: 
Selected Point: 

Start Point:
Goal Point:
Rectangle Obstacles: 
Circular Obsatcles: 
Selected Point: 

Start Point:
Goal Point:
Rectangle Obstacles: 
Circular Obsatcles: 
Selected Point: 

Start Point:
Goal Point:
Rectangle Obstacles: 
Circular Obsatcles: 
Selected Point: 

Start Point:
Goal Point:
Rectangle Obstacles: 
Circular Obsatcles: 
Selected Point: 

Start Point:
Goal Point:
Rectangle Obstacles: 
Circular Obsatcles: 
Selected Point: 

Start Point: {start}
Goal Point: {goal}
Rectangle Obstacles: {rectangle_obstacles}
Circular Obsatcles: {circle_obstacles}
Selected Point: 
"""
# start point从vertices中随机筛选一个点，然后和goal point计算中间的obstacles。最后交给模型来操作。
# {'path': [[18, 20], [23.158416982223034, 19.725859240148086], [28.832092952925265, 17.278826739704943], [30.733072899061337, 13.728863115123218], [34.42507074287456, 10.144957554275265], [43, 5]], 'operations': 100, 'score': 30.516890773803347}
# {'path': [[18, 20], [25.201280920226917, 18.009269000879385], [30.545092264364357, 17.177235213500833], [33.60980033035909, 8.438626203046182], [43, 5]], 'operations': 100, 'score': 32.140011898242086}