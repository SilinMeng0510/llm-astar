sysprompt = """You are an AI assistant specialized in designing collision-free paths in a two-dimensional environment. Your primary task is to create a safe and efficient path from a designated start point to an endpoint, ensuring avoidance of any circular, static obstacles.

Input Details:
- Start Point: The initial coordinates where the path begins.
- End Point: The target coordinates that the path must reach.
- Obstacle: Position and size of any circular, static obstacles.

Output Details:
- Path: Provide a sequence of coordinates formatted as [[x1, y1], [x2, y2], ..., [xn, yn]]. Each coordinate pair represents a waypoint on the path. Consecutive waypoints should be connected by straight lines, ensuring no collisions with obstacles.

Task Details:
Path generation takes a iterative process in a step by step manner. Strictly follow the below instruction of iterative process from 1 to 5:

1. Generated Points:
  - Generate at least 10 candidate waypoints aiming toward the endpoint or directly at the endpoint. These should strategically progress the path.

2. Filtered Points:
  - Exclude any waypoints that would result in a collision with obstacles.

3. Select Point:
  - Select the best waypoint from the filtered candidates, that helps generation of the most efficient path to the endpoint with least operations. 
  - If the endpoint is a candidate, must select it immediately.

4. Arrival Check:
  - Determine if the endpoint has been reached. If not, continue from the most recently added waypoint.

5. Current Path/Final Path:
  - Update the path by adding the selected waypoint, must not modify the previous waypoints.
  - If the endpoint is reached and Arrival Check returns "Yes", output the Final Path, instead output the Current Path.

Repeat the iterative process until the endpoint is reached and Arrival Check ouput "Yes".
"""

repe_0 = """design a path from [10, 0] to [0, 10] that avoids crossing the area of circle centered at [5, 5] with a radius of 4.
> First Iteration on [10, 0]
Generated Points: [9, -1], [9, 0], [9, 1], [10, -1], [10, 1], [11, -1], [11, 0], [11, 1], [10, 10], [0, 10], [0, 10]
Filtered Points: [9, -1], [9, 0], [9, 1], [10, -1], [10, 1], [11, -1], [11, 0], [11, 1], [10, 10], [0, 10]
Selected Point: [10, 10]
Arrival Check: No
Current Path: [[10, 0], [10, 10]]
> Second Iteration on [10, 10]
Generated point: [9, 9], [9, 10], [9, 11], [10, 9], [10, 11], [11, 9], [11, 10], [11, 11], [0, 10], [10, 5]
Filtered Points: [9, 9], [9, 10], [9, 11], [10, 9], [10, 11], [11, 9], [11, 10], [11, 11], [0, 10], [10, 5]
Selected Point: [0, 10]
Arrival Check: Yes
Final Path: [[10, 0], [10, 10], [0, 10]]
"""

repe_1 = """design a path from [-2, 27] to [3, -50] that avoids crossing the area of circle centered at [-19, 6] with a radius of 23.
> First Iteration on [-2, 27]
Generated Points: [8, 37], [-12, 37], [8, 17], [-12, 17], [-2, 37], [-2, 17], [8, 27], [-12, 27], [3, -50], [-2, 6]
Filtered Points: [8, 37], [8, 17], [-2, 37], [8, 27], [-12, 27]
Selected Point: [8, 17]
Arrival Check: No
Current Path: [[-2, 27], [8, 17]]
> Second Iteration on [8, 17]
Generated Points: [18, 27], [-2, 27], [18, 7], [-2, 7], [8, 27], [8, 7], [18, 17], [-2, 17], [3, -50], [8, -50]
Filtered Points: [18, 27], [-2, 27], [18, 7], [8, 27], [8, 7], [18, 17], [3, -50], [8, -50]
Selected Point: [3, -50]
Arrival Check: Yes
Final Path: [[-2, 27], [8, 17], [3, -50]]
"""

repe_2 = """design a path from [80, 40] to [-10, 10] that avoids crossing the area of circle centered at [32, 32] with a radius of 30.
> First Iteration on [80, 40]
Generated Points: [90, 50], [70, 50], [90, 30], [70, 30], [80, 50], [80, 30], [90, 40], [70, 40], [-10, 10], [-10, 40]
Filtered Points: [90, 50], [70, 50], [90, 30], [70, 30], [80, 50], [80, 30], [90, 40], [70, 40]
Selected Point: [70, 30]
Arrival Check: No
Current Path: [[80, 40], [70, 30]]
> Second Iteration on [70, 30]
Generated Points: [80, 40], [60, 40], [80, 20], [60, 20], [70, 40], [70, 20], [80, 30], [60, 30], [-10, 30], [70, 30]
Filtered Points: [80, 40], [80, 20], [60, 20], [70, 40], [70, 20], [80, 30], [70, 30]
Selected Point: [60, 20]
Arrival Check: No
Current Path: [[80, 40], [70, 30], [60, 20]]
> Third Iteration on [60, 20]
Generated Points: [70, 30], [50, 30], [70, 10], [50, 10], [60, 30], [60, 10], [70, 20], [50, 20], [60, 0], [-10, 10]
Filtered Points: [70, 30], [70, 10], [60, 10], [70, 20], [60, 0]
Selected Point: [60, 0]
Arrival Check: No
Current Path: [[80, 40], [70, 30], [60, 20], [60, 0]]
> Fourth Iteration on [60, 0]
Generated Points: [70, 10], [50, 10], [70, -10], [50, -10], [60, 10], [60, -10], [70, 0], [50, 0], [-10, 0], [-10, 10]
Filtered Points: [70, 10], [70, -10], [50, -10], [60, 10], [60, -10], [70, 0], [50, 0], [-10, 0]
Selected Point: [-10, 0]
Arrival Check: No
Current Path: [[80, 40], [70, 30], [60, 20], [60, 0], [-10, 0]]
> Fifth Iteration on [-10, 0]
Generated Points: [0, 10], [-20, 10], [0, -10], [-20, -10], [-10, 10], [-10, -10], [0, 0], [-20, 0], [-10, 10], [-20, 10]
Filtered Points: [0, 10], [-20, 10], [0, -10], [-20, -10], [-10, 10], [-10, -10], [0, 0], [-20, 0], [-10, 10], [-20, 10]
Selected Point: [-10, 10]
Arrival Check: Yes
Final Path: [[80, 40], [70, 30], [60, 20], [60, 0], [-10, 0], [-10, 10]]
"""