samples = {
    "sample1": """Design a path from [18, 8] to [17, 18] that avoids circles centered at [7, 12] with radius 3, [46, 20] with radius 2, [15, 5] with radius 2, [37, 7] with radius 3, and [37, 23] with radius 3, as well as rectangles at [14, 12] with width 8 and length 2, [18, 22] with width 8 and length 2, [26, 7] with width 2 and length 12, and [32, 14] with width 10 and length 2. The boundary of the environment is defined by the rectangle with vertices at [0, 0], [0, 30], [50, 30], and [50, 0].
{
  "start": [18, 8],
  "goal": [17, 18],
  "boundary_x": [0, 50],
  "boundary_y": [0, 30],
  "circle_obstacles": [    [7, 12, 3],
    [46, 20, 2],
    [15, 5, 2],
    [37, 7, 3],
    [37, 23, 3]
  ],
  "rectangle_obstacles": [    [14, 12, 8, 2],
    [18, 22, 8, 2],
    [26, 7, 2, 12],
    [32, 14, 10, 2]
  ]
}
"""
}
print(samples)

