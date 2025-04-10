import random
import numpy as np
from shapely.geometry import LineString, Point
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from llmastar.env.search import env as env_search, plotting as plotting_search
from llmastar.pather.a_star.a_star import AStar
import json, os
from pathlib import Path
from tqdm import tqdm


class Dataset:
    def __init__(self, root_dir="dataset", seed=42, maps=None, unique_env=100, unique_sg=10):
        """
        Initialize Dataset with configurable parameters
        
        Args:
            root_dir: Directory to store dataset
            seed: Random seed for reproducibility
            maps: List of tuples defining map dimensions [(width, height)]
            unique_env: Number of unique environments to generate
            unique_sg: Number of unique start-goal pairs per environment
        """
        self.MAP = maps if maps is not None else [(50, 30)]
        self.unique_env = unique_env
        self.unique_sg = unique_sg

        self.root_dir = Path(root_dir)
        self.root_dir.mkdir(parents=True, exist_ok=True)

        self.seed = seed
        random.seed(seed)
        np.random.seed(seed)
    
    def generate_environment_Astar(self, horizontal_range=(1, 4), vertical_range=(1, 4)):
        """
        Generate environments for A* pathfinding with verified paths
        
        Args:
            horizontal_range: Range of horizontal barriers (min, max)
            vertical_range: Range of vertical barriers (min, max)
        """
        for map in self.MAP:
            x_range, y_range = (0, map[0]+1), (0, map[1]+1)

            json_file = Path(f'{self.root_dir}/environment_{map[0]}_{map[1]}.json')

            environments = []

            if json_file.exists():
                with open(json_file, 'r') as file:
                    environments = json.load(file)
            
            # Create remaining environments
            remaining = self.unique_env - len(environments)
            if remaining > 0:
                pbar = tqdm(range(len(environments), self.unique_env), 
                           desc=f"Generating environments ({map[0]}x{map[1]})")
                for i in pbar:
                    num_h = round(random.uniform(horizontal_range[0], horizontal_range[1]))
                    num_v = round(random.uniform(vertical_range[0], vertical_range[1]))
                    data = {'id': i}
                    pbar.set_postfix(barriers=f"H:{num_h},V:{num_v}")
                    
                    # Generate environment with A*-verified paths
                    data.update(self._generate_random_obstacles_and_points_Astar(x_range, y_range, num_h, num_v))
                    
                    environments.append(data)

                    environment = environments[-1]

                    for index, sg in enumerate(environment['start_goal']):
                        pbar.set_postfix(map=f"{i}/{index}")
                        
                        map_dir = f"{self.root_dir}/environment_{x_range[1]}_{y_range[1]}_maps/map_{i}"
                        if not os.path.exists(map_dir):
                            os.makedirs(map_dir)
                        
                        # Extract start/goal from the verified paths
                        if isinstance(sg, dict):
                            s_start = sg['start']
                            s_goal = sg['goal']
                        else:
                            s_start, s_goal = sg[0], sg[1]
                        
                        # Visualize the environment and path
                        filepath = f"{map_dir}/{index}.png"
                        
                        # If we have a path, visualize it with the path
                        if isinstance(sg, dict) and 'path' in sg:
                            Env = env_search.Env(x_range[1], y_range[1], environment['horizontal_barriers'], environment['vertical_barriers'])
                            plot = plotting_search.Plotting(s_start, s_goal, Env)
                            plot.animation(sg['path'], sg['visited'], False, f"A* {i}-{index}", filepath)
                        else:
                            # Otherwise just plot the grid
                            self.plot_grid_Astar(s_start, s_goal, environment['range_x'], environment['range_y'], 
                                                environment['horizontal_barriers'], environment['vertical_barriers'], 
                                                f"A* {i}-{index}", filepath)
                
                    with open(json_file, 'w') as f:
                        json.dump(environments, f, indent=4)

            
            print(f"Environment generation complete: {json_file}")

    def _generate_random_obstacles_and_points_Astar(self, x_range, y_range, num_h_obstacles, num_v_obstacles):
        height = y_range[1] - y_range[0]
        width = x_range[1] - x_range[0]
        
        def generate_horizontal_obstacles(num_h_obstacles, x_range, y_range, existing_obstacles):
            horizontal_obstacles = []
            for _ in range(num_h_obstacles):
                while True:
                    y = round(random.uniform(y_range[0] + 2, y_range[1] - 2))
                    x_start = round(random.uniform(x_range[0], x_range[1]))
                    x_end = round(random.uniform(x_start, x_range[1]))
                    if x_end - x_start < 3 or x_end - x_start >= width - 5:
                        continue
                    horizontal = LineString([(x_start, y), (x_end, y)])
                    horizontal_obstacles.append([y, x_start, x_end])
                    existing_obstacles.append(horizontal)
                    break
            return horizontal_obstacles
        
        def generate_vertical_obstacles(num_v_obstacles, x_range, y_range, existing_obstacles):
            vertical_obstacles = []
            for _ in range(num_v_obstacles):
                while True:
                    x = round(random.uniform(x_range[0] + 2, x_range[1] - 2))
                    y_start = round(random.uniform(y_range[0], y_range[1]))
                    y_end = round(random.uniform(y_start, y_range[1]))
                    if y_end - y_start < 3 or y_end - y_start >= height - 5:
                        continue
                    vertical = LineString([(x, y_start), (x, y_end)])
                    vertical_obstacles.append([x, y_start, y_end])
                    existing_obstacles.append(vertical)
                    break
            return vertical_obstacles
        
        def generate_random_point(x_range, y_range, existing_obstacles):
            while True:
                x = round(random.uniform(x_range[0], x_range[1] - 2))
                y = round(random.uniform(y_range[0], y_range[1] - 2))
                point = Point(x, y)
                if not any(point.intersects(ob) for ob in existing_obstacles):
                    return [x, y]
        
        existing_obstacles = []
        for x in x_range:
            existing_obstacles.append(LineString([(x, y_range[0]), (x, y_range[1])]))
        for y in y_range:
            existing_obstacles.append(LineString([(x_range[0], y), (x_range[1], y)]))
            
        horizontal_barriers = generate_horizontal_obstacles(num_h_obstacles, x_range, y_range, existing_obstacles)
        vertical_barriers = generate_vertical_obstacles(num_v_obstacles, x_range, y_range, existing_obstacles)
        
        # Initialize A* for path validation
        astar = AStar()
        
        # Create a temporary environment for A* validation
        environment = {
            "range_x": x_range,
            "range_y": y_range,
            "horizontal_barriers": horizontal_barriers,
            "vertical_barriers": vertical_barriers,
            "start_goal": []
        }
        
        # Generate valid start-goal pairs with A* validation
        sg_list = []
        max_attempts = self.unique_sg * 10  # Maximum attempts to find valid paths
        attempts = 0
        pbar = tqdm(total=self.unique_sg, desc="Generating valid start-goal pairs")
        
        while len(sg_list) < self.unique_sg and attempts < max_attempts:
            attempts += 1
            
            # Generate random start and goal points
            start = generate_random_point(x_range, y_range, existing_obstacles)
            goal = generate_random_point(x_range, y_range, existing_obstacles)
            
            # Use A* to validate if there's a valid path
            query = {
                'start': start,
                'goal': goal,
                'range_x': x_range,
                'range_y': y_range,
                'horizontal_barriers': horizontal_barriers,
                'vertical_barriers': vertical_barriers
            }
            
            # No need for visualization during validation
            result = astar.searching(query, filepath=None)
            
            # Only add pairs where A* found a valid path
            if result['path'] and result['length'] >= 25:
                sg_list.append((start, goal))
                pbar.update(1)
                # Store the paths directly in the environment
                environment['start_goal'].append({
                    'start': start,
                    'goal': goal,
                    'path': result['path'],
                    'visited': result['visited'],
                    'metrics': {
                        'operations': result['operation'],
                        'storage': result['storage'],
                        'path_length': result['length']
                    }
                })
            else:
                # If no path found, don't count against max_attempts to avoid 
                # scenarios where it's impossible to find enough valid paths
                attempts -= 1
        
        
        pbar.close()
        
        if len(sg_list) < self.unique_sg:
            print(f"Warning: Could only find {len(sg_list)} valid start-goal pairs out of {self.unique_sg} requested")
        
        return environment

    def add_query_Astar(self, json_file=None):
        """
        Add query descriptions to each start-goal pair
        
        Args:
            json_file: Name of the JSON file to process
        """
        if json_file is None:
            json_files = [f for f in os.listdir(self.root_dir) if f.startswith("environment_") and f.endswith(".json")]
        else:
            json_files = [json_file]
            
        for json_file in json_files:
            filepath = Path(f'{self.root_dir}/{json_file}')
            
            if not filepath.exists():
                continue

            with open(filepath) as f:
                data = json.load(f)
            
            pbar = tqdm(enumerate(data), total=len(data), desc=f"Adding queries to {json_file}")
            for env_idx, environment in pbar:
                for sg_idx, sg in enumerate(environment['start_goal']):
                    pbar.set_postfix(env=env_idx, sg=sg_idx)
                    
                    if len(sg) > 2:  # Query already exists
                        continue
                        
                    start, goal = sg[0], sg[1]
                    x_range = environment['range_x']
                    y_range = environment['range_y']
                    horizontal_barriers = environment['horizontal_barriers']
                    vertical_barriers = environment['vertical_barriers']
                    query = f"""design a path from [{start[0]}, {start[1]}] to [{goal[0]}, {goal[1]}] on a {x_range[1]} by {y_range[1]} grid that avoids horizontal barriers centered at {horizontal_barriers} and vertical barriers at {vertical_barriers}."""
                    sg.append(query)
            
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=4)
    
    def generate_waypoints(self, json_file=None, waypoint_strategy='intelligent', num_waypoints=5, 
                           save_visualizations=True, overwrite_existing=False):
        """
        Generate waypoints for precomputed A* paths
        
        Args:
            json_file: Name of the JSON file to process (if None, process all environment JSON files)
            waypoint_strategy: Strategy for generating waypoints ('uniform', 'normal', 'intelligent')
            num_waypoints: Number of waypoints to generate per path
            save_visualizations: Whether to save visualizations of the waypoints
            overwrite_existing: Whether to overwrite existing waypoints
        """
        if json_file is None:
            json_files = [f for f in os.listdir(self.root_dir) if f.startswith("environment_") and f.endswith(".json")]
        else:
            json_files = [json_file]
            
        for json_file in json_files:
            filepath = Path(f'{self.root_dir}/{json_file}')
            
            if not filepath.exists():
                continue

            with open(filepath) as f:
                data = json.load(f)
                
            map_dims = json_file.replace("environment_", "").replace(".json", "").split("_")
            vis_folder = f"{self.root_dir}/astar_paths_{map_dims[0]}_{map_dims[1]}"
            
            if save_visualizations and not os.path.exists(vis_folder):
                os.makedirs(vis_folder)
            
            # Track if any changes were made
            changes_made = False
            
            pbar = tqdm(enumerate(data), total=len(data), desc=f"Generating {waypoint_strategy} waypoints for {json_file}")
            for env_idx, environment in pbar:
                for sg_idx, sg in enumerate(environment['start_goal']):
                    pbar.set_postfix(env=env_idx, sg=sg_idx)
                    
                    # Skip if not a dictionary (A* hasn't been run yet) or if doesn't have path
                    if not isinstance(sg, dict) or 'path' not in sg:
                        print(f"Warning: A* path not found for env {env_idx}, sg {sg_idx}. Skipping.")
                        continue
                    
                    # Skip if already has waypoints with this strategy and we're not overwriting
                    waypoint_key = f"waypoints_{waypoint_strategy}"
                    if not overwrite_existing and waypoint_key in sg:
                        print(f"Waypoints already exist for env {env_idx}, sg {sg_idx} with strategy {waypoint_strategy}, skipping...")
                        continue
                    
                    # Prepare query for waypoint generation
                    query = {
                        'start': sg['start'],
                        'goal': sg['goal'],
                        'range_x': environment['range_x'],
                        'range_y': environment['range_y'],
                        'horizontal_barriers': environment['horizontal_barriers'],
                        'vertical_barriers': environment['vertical_barriers']
                    }
                    
                    # Generate waypoints based on chosen strategy
                    waypoints = self._generate_waypoints(
                        sg['path'], 
                        query,
                        strategy=waypoint_strategy,
                        num_points=num_waypoints
                    )
                    
                    # Store waypoints with strategy-specific key
                    sg[waypoint_key] = waypoints
                    changes_made = True
                    
                    # Create visualizations
                    if save_visualizations:
                        # Visualization with just waypoints
                        waypoints_filepath = f"{vis_folder}/path_{env_idx}_{sg_idx}_with_{waypoint_strategy}_waypoints.png"
                        
                        # Plot with waypoints
                        self.plot_grid_Astar(
                            sg['start'], 
                            sg['goal'], 
                            environment['range_x'], 
                            environment['range_y'], 
                            environment['horizontal_barriers'], 
                            environment['vertical_barriers'],
                            f"A* {env_idx}-{sg_idx} with waypoints ({waypoint_strategy})",
                            waypoints_filepath,
                            show=False,
                            waypoints=waypoints
                        )
                        
                        # Full visualization with path, visited and waypoints
                        full_filepath = f"{vis_folder}/path_{env_idx}_{sg_idx}.png"
                        Env = env_search.Env(
                            environment['range_x'][1], 
                            environment['range_y'][1], 
                            environment['horizontal_barriers'], 
                            environment['vertical_barriers']
                        )
                        plot = plotting_search.Plotting(sg['start'], sg['goal'], Env)
                        plot.animation_with_waypoints(
                            sg['path'], 
                            sg['visited'], 
                            waypoints, 
                            False,  # don't show
                            f"A* {env_idx}-{sg_idx} with path and {waypoint_strategy} waypoints", 
                            full_filepath
                        )
            
            # Save updated data back to file only if changes were made
            if changes_made:
                with open(filepath, 'w') as f:
                    json.dump(data, f, indent=4)
                print(f"Waypoints with strategy '{waypoint_strategy}' saved to {filepath}")
            else:
                print(f"No changes made to {filepath}")
                
    def run_astar_and_add_waypoints(self, json_file=None, waypoint_strategy='intelligent', num_waypoints=5, 
                                   save_visualizations=True):
        """
        Add waypoints to the already computed A* paths (legacy method)
        
        This method is kept for backward compatibility but internally uses
        the decoupled generate_waypoints method. A* paths are assumed to be
        already computed during environment generation.
        
        Args:
            json_file: Name of the JSON file to process (if None, process all environment JSON files)
            waypoint_strategy: Strategy for generating waypoints ('uniform', 'normal', 'intelligent')
            num_waypoints: Number of waypoints to generate per path
            save_visualizations: Whether to save visualizations of the paths and waypoints
        """
        # Generate waypoints for the precomputed A* paths
        self.generate_waypoints(
            json_file=json_file,
            waypoint_strategy=waypoint_strategy,
            num_waypoints=num_waypoints,
            save_visualizations=save_visualizations,
            overwrite_existing=True  # Always overwrite in the legacy method
        )

    def _generate_waypoints(self, path, query, strategy='uniform', num_points=5):
        """
        Generate waypoints from a path based on the specified strategy
        
        Args:
            path: List of path points [(x1, y1), (x2, y2), ...]
            query: Original query with environment information
            strategy: 'uniform', 'normal', or 'intelligent'
            num_points: Number of waypoints to generate
            
        Returns:
            List of waypoints [(x1, y1), (x2, y2), ...]
        """
        if len(path) <= 2:  # No intermediate points to sample
            return path
            
        # Reverse path (A* returns path from goal to start)
        path = path[::-1]
        
        if strategy == 'uniform':
            # Uniform sampling along the path
            if num_points >= len(path):
                return path
            indices = np.linspace(0, len(path) - 1, num_points, dtype=int)
            return [path[i] for i in indices]
            
        elif strategy == 'normal':
            # Normal distribution sampling - more points in the middle
            if num_points >= len(path):
                return path
            # Calculate normalized positions (0 to 1)
            positions = np.linspace(0, 1, len(path))
            # Create normal distribution centered at 0.5
            weights = np.exp(-((positions - 0.5) ** 2) / 0.1)
            # Normalize weights to probabilities
            probs = weights / weights.sum()
            # Sample indices according to distribution
            indices = np.sort(np.random.choice(len(path), size=num_points, replace=False, p=probs))
            return [path[i] for i in indices]
            
        elif strategy == 'intelligent':
            # Line-of-sight based intelligent waypoint selection
            # Extract barriers and other environment information
            horizontal_barriers = query['horizontal_barriers']
            vertical_barriers = query['vertical_barriers']
            
            # Line-of-sight check function
            def has_line_of_sight(p1, p2):
                # Create a line between the two points
                line = LineString([(p1[0], p1[1]), (p2[0], p2[1])])
                
                # Check for intersections with horizontal barriers
                for barrier in horizontal_barriers:
                    y, x_start, x_end = barrier
                    barrier_line = LineString([(x_start, y), (x_end, y)])
                    if line.intersects(barrier_line):
                        return False
                
                # Check for intersections with vertical barriers
                for barrier in vertical_barriers:
                    x, y_start, y_end = barrier
                    barrier_line = LineString([(x, y_start), (x, y_end)])
                    if line.intersects(barrier_line):
                        return False
                
                # No intersections found
                return True
            
            # Always include start point
            waypoints = [path[0]]
            last_waypoint = path[0]
            
            # Walk along the path and add waypoints where line-of-sight is broken
            for i in range(1, len(path)):
                # Check if there's line-of-sight between current point and last waypoint
                if not has_line_of_sight(last_waypoint, path[i]):
                    # If line-of-sight is broken, add the previous point as a waypoint
                    # (unless it's already the last waypoint)
                    if path[i-1] != last_waypoint:
                        waypoints.append(path[i-1])
                        last_waypoint = path[i-1]
            
            # Always include the goal point (end of path)
            if waypoints[-1] != path[-1]:
                waypoints.append(path[-1])
            
            return waypoints
        
        else:
            raise ValueError(f"Unknown waypoint strategy: {strategy}")
            
    def plot_grid_Astar(self, s_start, s_goal, range_x, range_y, horizontal_barriers, vertical_barriers, name='A*', path="temp.png", show=False, waypoints=None):
        """
        Plot the grid with start, goal, and barriers. Optionally include waypoints.
        
        Args:
            s_start: Start coordinates [x, y]
            s_goal: Goal coordinates [x, y]
            range_x: Range of x coordinates (min, max)
            range_y: Range of y coordinates (min, max)
            horizontal_barriers: List of horizontal barriers
            vertical_barriers: List of vertical barriers
            name: Plot title
            path: Path to save the plot
            show: Whether to display the plot
            waypoints: Optional list of waypoints to plot as yellow stars
        """
        Env = env_search.Env(range_x[1], range_y[1], horizontal_barriers, vertical_barriers)  # class Env
        plot = plotting_search.Plotting(s_start, s_goal, Env)
        
        # If waypoints are provided, use the method that plots them
        if waypoints is not None:
            plt.clf()
            plot.plot_grid(name)
            plot.plot_waypoints(waypoints)
            plt.savefig(path)
            if show:
                plt.show()
            plt.close()
        else:
            plot.plot_map(name, path, show)