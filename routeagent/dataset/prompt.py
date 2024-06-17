sysprompt = """Given the following input data, generate a detailed task description for path planning:
Input data format:
{
  "start": [start_x, start_y],
  "goal": [goal_x, goal_y],
  "range_x": [min_x, max_x],
  "range_y": [min_y, max_y],
  "circle_obstacles": [
    {"center": [circle1_x, circle1_y], "radius": circle1_radius},
    {"center": [circle2_x, circle2_y], "radius": circle2_radius},
    ...
  ],
  "rectangle_obstacles": [
    {"corner": [rect1_x, rect1_y], "width": rect1_width, "height": rect1_height},
    {"corner": [rect2_x, rect2_y], "width": rect2_width, "height": rect2_height},
    ...
  ]
}

Example:
Input:
{
  "start": [12, 6],
  "goal": [36, 28],
  "range_x": [0, 50],
  "range_y": [0, 30],
  "circle_obstacles": [
    {"center": [8, 14], "radius": 4},
    {"center": [26, 8], "radius": 2},
    {"center": [22, 5], "radius": 3},
    {"center": [30, 10], "radius": 5},
    {"center": [40, 6], "radius": 3}
  ],
  "rectangle_obstacles": [
    {"corner": [17, 20], "width": 7, "height": 3},
    {"corner": [28, 18], "width": 4, "height": 4},
    {"corner": [26, 7], "width": 3, "height": 15},
    {"corner": [33, 22], "width": 5, "height": 2}
  ]
}
Output:
"From the start point [12, 6] to the destination [36, 28], plan a path that avoids circular obstacles centered at [8, 14] (radius 4), [26, 8] (radius 2), [22, 5] (radius 3), [30, 10] (radius 5), and [40, 6] (radius 3). Also, avoid rectangular obstacles located at [17, 20] (7x3), [28, 18] (4x4), [26, 7] (3x15), and [33, 22] (5x2). The boundaries of the area are defined by the rectangle with vertices at [0, 0], [0, 30], [50, 30], and [50, 0]."
"""