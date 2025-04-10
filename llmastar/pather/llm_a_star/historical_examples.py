HISTORICAL_EXAMPLES = [
    {
        "barrier_description": "The environment contains a horizontal barrier at y=10 spanning from x=0 to x=25, and another horizontal barrier at y=15 spanning from x=30 to x=50. There is also a vertical barrier at x=25 spanning from y=10 to y=22.",
        "path_description": "From (5, 5) the path first goes to (26, 9) to bypass the horizontal barrier, then to (25, 23) to go around the vertical barrier, finally arriving at (20, 20).",
        "start": [5, 5],
        "goal": [20, 20],
        "horizontal_barriers": [[10, 0, 25], [15, 30, 50]],
        "vertical_barriers": [[25, 10, 22]]
    },
    {
        "barrier_description": "The environment contains a horizontal barrier at y=7 spanning from x=0 to x=10, and another horizontal barrier at y=5 spanning from x=30 to x=40. There are vertical barriers at x=14 spanning from y=12 to y=30, and at x=40 spanning from y=0 to y=11.",
        "path_description": "From (2, 3) the path goes to (11, 6) to avoid the horizontal barrier, then directly to (18, 8).",
        "start": [2, 3],
        "goal": [18, 8],
        "horizontal_barriers": [[7, 0, 10], [5, 30, 40]],
        "vertical_barriers": [[14, 12, 30], [40, 0, 11]]
    },
    {
        "barrier_description": "The environment contains horizontal barriers at y=7 spanning from x=0 to x=20, and at y=15 spanning from x=10 to x=15. There are vertical barriers at x=10 spanning from y=15 to y=30, at x=30 spanning from y=0 to y=18, and at x=10 spanning from y=0 to y=5.",
        "path_description": "From (25, 25) the path goes to (21, 7) to bypass the horizontal barriers, then to (10, 6) to navigate around the vertical barrier, finally arriving at (4, 4).",
        "start": [25, 25],
        "goal": [4, 4],
        "horizontal_barriers": [[7, 0, 20], [15, 10, 15]],
        "vertical_barriers": [[10, 15, 30], [30, 0, 18], [10, 0, 5]]
    }
] 