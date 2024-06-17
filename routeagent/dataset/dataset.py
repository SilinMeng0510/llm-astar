import random
from shapely.geometry import LineString, Point, box
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from routeagent.env.sample import env as env_sample
from routeagent.env.search import env as env_search, plotting as plotting_search
import json, os
import inquirer


class Dataset:
    def __init__(self):
        self.MAP = [(50, 30)]
        self.unique_env = 100
        self.unique_sg = 10
    
    def generate_environment_Astar(self):
        for map in self.MAP:
            x_range, y_range = (0, map[0]+1), (0, map[1]+1)
            with open('dataset/A*/environment_50_30.json', 'r') as file:
                environments = json.load(file)
            
            for i in range(len(environments), self.unique_env):
                decision = False
                while not decision:
                    num_h = round(random.uniform(1, 4))
                    num_v = round(random.uniform(1, 4))
                    data = {'id': i}
                    data.update(self._generate_random_obstacles_and_points_Astar(x_range, y_range, num_h, num_v))
                    self.plot_grid_Astar(data['start_goal'][0][0], data['start_goal'][0][1], data['range_x'], data['range_y'], data['horizontal_barriers'], data['vertical_barriers'], show=False)
                    action_planner = [
                        inquirer.List(
                            'approach',
                            message=f"Choose your approach on {i}",
                            choices=[('Bad', False), ('Good', True)],
                            default=False
                        )
                    ]
                    decision = inquirer.prompt(action_planner)['approach']
                environments.append(data)
                
        with open('dataset/A*/environment_50_30.json', 'w') as f:
            json.dump(environments, f, indent=4)
        
        for i in range(len(environments)):
            data = environments[i]
            for index in range(len(data['start_goal'])): 
                sg = data['start_goal'][index]
                if not os.path.exists(f"dataset/A*/environment_{x_range[1]}_{y_range[1]}_maps/map_{i}"):
                    os.makedirs(f"dataset/A*/environment_{x_range[1]}_{y_range[1]}_maps/map_{i}")
                self.plot_grid_Astar(sg[0], sg[1], data['range_x'], data['range_y'], data['horizontal_barriers'], data['vertical_barriers'], f"A* {i}-{index}", f"dataset/A*/environment_{x_range[1]}_{y_range[1]}_maps/map_{i}/{index}.png")
        
    def _generate_random_obstacles_and_points_Astar(self, x_range, y_range, num_h_obstacles, num_v_obstacles):
        def generate_horizontal_obstacles(num_h_obstacles, x_range, y_range, existing_obstacles):
            horizontal_obstacles = []
            for _ in range(num_h_obstacles):
                while True:
                    y = round(random.uniform(y_range[0], y_range[1]))
                    x_start = round(random.uniform(x_range[0], x_range[1]))
                    x_end = round(random.uniform(x_start, x_range[1]))
                    horizontal = LineString([(x_start, y), (x_end, y)])
                    horizontal_obstacles.append([y, x_start, x_end])
                    existing_obstacles.append(horizontal)
                    break
            return horizontal_obstacles
        
        def generate_vertical_obstacles(num_v_obstacles, x_range, y_range, existing_obstacles):
            vertical_obstacles = []
            for _ in range(num_v_obstacles):
                while True:
                    x = round(random.uniform(x_range[0], x_range[1]))
                    y_start = round(random.uniform(y_range[0], y_range[1]))
                    y_end = round(random.uniform(y_start, y_range[1]))
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
        
        sg_list = []
        while len(sg_list) < self.unique_sg:
            start = generate_random_point(x_range, y_range, existing_obstacles)
            goal = generate_random_point(x_range, y_range, existing_obstacles)
            if any(LineString([start, goal]).intersects(ob) for ob in existing_obstacles):
                sg_list.append((start, goal))
        
        environment = {
            "range_x": x_range,
            "range_y": y_range,
            "horizontal_barriers": horizontal_barriers,
            "vertical_barriers": vertical_barriers,
            "start_goal": sg_list
        }
        print(environment)

        return environment

    def add_query_Astar(self, filepath='dataset/A*/environment_50_30.json'):
        with open(filepath) as f:
            data = json.load(f)
        
        for environment in data:
            for sg in environment['start_goal']:
                start, goal = sg[0], sg[1]
                x_range = environment['range_x']
                y_range = environment['range_y']
                horizontal_barriers = environment['horizontal_barriers']
                vertical_barriers = environment['vertical_barriers']
                query = f"""design a path from [{start[0]}, {start[1]}] to [{goal[0]}, {goal[1]}] on a {x_range[1]} by {y_range[1]} grid that avoids horizontal barriers centered at {horizontal_barriers} and vertical barriers at {vertical_barriers}."""
                sg.append(query)
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=4)
            
    def plot_grid_Astar(self, s_start, s_goal, range_x, range_y, horizontal_barriers, vertical_barriers, name='A*', path="temp.png", show=False):
        Env = env_search.Env(range_x[1], range_y[1], horizontal_barriers, vertical_barriers)  # class Env
        plot = plotting_search.Plotting(s_start, s_goal, Env)
        plot.plot_map(name, path, show)
    
    def _generate_random_obstacles_and_points_RRT(self, x_range, y_range, num_circles, num_rectangles):
        def generate_circular_obstacles(num_circles, x_range, y_range, existing_obstacles):
            circle_obstacles = []
            for _ in range(num_circles):
                while True:
                    x = round(random.uniform(x_range[0], x_range[1]))
                    y = round(random.uniform(y_range[0], y_range[1]))
                    radius = round(random.uniform(1, 5))  # Random radius between 1 and 5
                    circle = Point(x, y).buffer(radius)
                    if not any(circle.intersects(ob) for ob in existing_obstacles):
                        circle_obstacles.append([x, y, radius])
                        existing_obstacles.append(circle)
                        break
            return circle_obstacles

        def generate_rectangular_obstacles(num_rectangles, x_range, y_range, existing_obstacles):
            rectangle_obstacles = []
            for _ in range(num_rectangles):
                while True:
                    x = round(random.uniform(x_range[0], x_range[1]))
                    y = round(random.uniform(y_range[0], y_range[1]))
                    width = round(random.uniform(2, 10))  # Random width between 2 and 10
                    height = round(random.uniform(2, 10)) # Random height between 2 and 10
                    rectangle = box(x, y, x + width, y + height)
                    if not any(rectangle.intersects(ob) for ob in existing_obstacles):
                        rectangle_obstacles.append([x, y, width, height])
                        existing_obstacles.append(rectangle)
                        break
            return rectangle_obstacles

        def generate_random_point(x_range, y_range, existing_obstacles):
            while True:
                x = round(random.uniform(x_range[0], x_range[1]))
                y = round(random.uniform(y_range[0], y_range[1]))
                point = Point(x, y)
                if not any(point.intersects(ob) for ob in existing_obstacles):
                    return [x, y]

        existing_obstacles = [
            LineString([(x_range[0]+1, y_range[0]+1), (x_range[1]-1, y_range[0]+1)]),  
            LineString([(x_range[1]-1, y_range[0]+1), (x_range[1]-1, y_range[1]-1)]),  
            LineString([(x_range[1]-1, y_range[1]-1), (x_range[0]+1, y_range[1]-1)]),  
            LineString([(x_range[0]+1, y_range[1]-1), (x_range[0]+1, y_range[0]+1)]),
            LineString([(x_range[0], y_range[0]), (x_range[1], y_range[0])]),
            LineString([(x_range[1], y_range[0]), (x_range[1], y_range[1])]),
            LineString([(x_range[1], y_range[1]), (x_range[0], y_range[1])]),
            LineString([(x_range[0], y_range[1]), (x_range[0], y_range[0])])  
        ]
        
        circle_obstacles = generate_circular_obstacles(num_circles, x_range, y_range, existing_obstacles)
        rectangle_obstacles = generate_rectangular_obstacles(num_rectangles, x_range, y_range, existing_obstacles)
        
        sg_list = []
        while len(sg_list) < self.unique_sg:
            start = generate_random_point(x_range, y_range, existing_obstacles)
            goal = generate_random_point(x_range, y_range, existing_obstacles)
            if any(LineString([start, goal]).intersects(ob) for ob in existing_obstacles):
                sg_list.append((start, goal))
        
        environment = {
            "range_x": x_range,
            "range_y": y_range,
            "circle_obstacles": circle_obstacles,
            "rectangle_obstacles": rectangle_obstacles,
            "start_goal": sg_list
        }

        return environment
    
    def generate_environment_RRT(self):
        for map in self.MAP:
            x_range, y_range = (0, map[0]), (0, map[1])
            environments = []
            
            for i in range(self.unique_env):
                num_cir = round(random.uniform(0, round((map[0] + map[1]) / 10)))
                num_rec = round(random.uniform(0, round((map[0] + map[1]) / 10)))
                data = {'id': i}
                data.update(self._generate_random_obstacles_and_points_RRT(x_range, y_range, num_cir, num_rec))
                environments.append(data)
                ev = env_sample.Env(x_range, y_range, data['circle_obstacles'], data['rectangle_obstacles'])
                for index in range(len(data['start_goal'])): 
                    sg = data['start_goal'][index]
                    self.plot_grid_RRT(ev.obs_boundary, ev.obs_rectangle, ev.obs_circle, sg[0], sg[1], f'Environment {x_range[1]}x{y_range[1]}: {i}-{index}', f'environment_{x_range[1]}_{y_range[1]}_images', f'{i}-{index}')
            with open(f'dataset/environment_{x_range[1]}_{y_range[1]}.json', 'w') as f:
                json.dump(environments, f, indent=4)

    def plot_grid_RRT(self, obs_bound, obs_rectangle, obs_circle, xI, xG, name, dirname, index):
        fig, ax = plt.subplots(figsize=(12, 8))

        for (ox, oy, w, h) in obs_bound:
            ax.add_patch(
                patches.Rectangle(
                    (ox, oy), w, h,
                    edgecolor='black',
                    facecolor='black',
                    fill=True
                )
            )

        for (ox, oy, w, h) in obs_rectangle:
            ax.add_patch(
                patches.Rectangle(
                    (ox, oy), w, h,
                    edgecolor='black',
                    facecolor='gray',
                    fill=True
                )
            )

        for (ox, oy, r) in obs_circle:
            ax.add_patch(
                patches.Circle(
                    (ox, oy), r,
                    edgecolor='black',
                    facecolor='gray',
                    fill=True
                )
            )

        plt.plot(xI[0], xI[1], "bs", linewidth=1)
        plt.plot(xG[0], xG[1], "rs", linewidth=1)
        
        plt.axhline(0, color='black',linewidth=0.5)
        plt.axvline(0, color='black',linewidth=0.5)
        plt.grid(color = 'gray', linestyle = '-', linewidth = 0.5)
        
        # plt.xticks(np.arange(0, 51, 1))
        # plt.yticks(np.arange(0, 31, 1))

        plt.title(name)
        plt.axis("equal")
        plt.savefig(f"dataset/{dirname}/{index}.png")
    
    def add_query_RRT(self, filepath='dataset/RRT*/environment_50_30.json'):
        with open(filepath) as f:
            data = json.load(f)
        
        for environment in data:
            for sg in environment['start_goal']:
                start, goal = sg[0], sg[1]
                query = f"""design a path from [{start[0]}, {start[1]}] to [{goal[0]}, {goal[1]}] that avoids circles centered at {environment['circle_obstacles']} and rectangles at {environment['rectangle_obstacles']}. The boundaries of the area are defined by the rectangle with vertices at [{environment['range_x'][0]}, {environment['range_y'][0]}], [{environment['range_x'][0]}, {environment['range_y'][1]}], [{environment['range_x'][1]}, {environment['range_y'][0]}], [{environment['range_x'][1]}, {environment['range_y'][1]}]."""
                sg.append(query)
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=4)

    def generate(self, sample_num=1, ratio=1, fix=False, visual=False):
        # Return fix commands with 30 samples
        if fix:
            commands = ['design a path from [32, -18] to [-47, 23] that avoids crossing the area of circle centered at [-20, 3] with a radius of 13.', 'design a path from [-25, -25] to [49, 39] that avoids crossing the area of circle centered at [41, 30] with a radius of 3.', 'design a path from [-19, -8] to [22, -20] that avoids crossing the area of circle centered at [-1, -20] with a radius of 13.', 'design a path from [-46, 4] to [41, 0] that avoids crossing the area of circle centered at [13, 10] with a radius of 10.', 'design a path from [-27, -28] to [2, -21] that avoids crossing the area of circle centered at [-15, -25] with a radius of 11.', 'design a path from [-14, 49] to [42, -43] that avoids crossing the area of circle centered at [-19, 17] with a radius of 29.', 'design a path from [21, 33] to [-33, -4] that avoids crossing the area of circle centered at [-27, 9] with a radius of 11.', 'design a path from [-39, -38] to [48, 10] that avoids crossing the area of circle centered at [-3, -10] with a radius of 20.', 'design a path from [-43, -3] to [35, -16] that avoids crossing the area of circle centered at [14, 12] with a radius of 27.', 'design a path from [-40, 11] to [43, -42] that avoids crossing the area of circle centered at [2, -24] with a radius of 10.', 'design a path from [-2, -17] to [23, -40] that avoids crossing the area of circle centered at [22, -32] with a radius of 7.', 'design a path from [-45, -37] to [32, -45] that avoids crossing the area of circle centered at [6, -41] with a radius of 3.', 'design a path from [42, -32] to [-17, -5] that avoids crossing the area of circle centered at [3, -10] with a radius of 15.', 'design a path from [2, 10] to [27, 13] that avoids crossing the area of circle centered at [15, 12] with a radius of 5.', 'design a path from [43, 48] to [6, -33] that avoids crossing the area of circle centered at [2, -6] with a radius of 21.', 'design a path from [-21, 33] to [38, -38] that avoids crossing the area of circle centered at [-14, -13] with a radius of 35.', 'design a path from [49, -16] to [-44, 50] that avoids crossing the area of circle centered at [24, 12] with a radius of 20.', 'design a path from [-42, 27] to [-14, -38] that avoids crossing the area of circle centered at [-30, -20] with a radius of 12.', 'design a path from [42, 19] to [-23, -12] that avoids crossing the area of circle centered at [8, -8] with a radius of 26.', 'design a path from [16, 49] to [37, 15] that avoids crossing the area of circle centered at [20, 43] with a radius of 2.', 'design a path from [-48, -24] to [11, -26] that avoids crossing the area of circle centered at [-10, -18] with a radius of 7.', 'design a path from [22, 45] to [-32, -10] that avoids crossing the area of circle centered at [-24, 17] with a radius of 20.', 'design a path from [23, -7] to [13, -44] that avoids crossing the area of circle centered at [9, -24] with a radius of 19.', 'design a path from [-14, 20] to [28, 1] that avoids crossing the area of circle centered at [8, -16] with a radius of 25.', 'design a path from [-19, 1] to [21, 44] that avoids crossing the area of circle centered at [4, 32] with a radius of 14.', 'design a path from [-20, -39] to [-16, 33] that avoids crossing the area of circle centered at [-20, 7] with a radius of 15.', 'design a path from [0, 4] to [4, -27] that avoids crossing the area of circle centered at [9, -12] with a radius of 8.', 'design a path from [24, 25] to [38, -7] that avoids crossing the area of circle centered at [29, -1] with a radius of 7.', 'design a path from [-31, -29] to [23, 9] that avoids crossing the area of circle centered at [-5, -26] with a radius of 19.', 'design a path from [28, -24] to [-36, -41] that avoids crossing the area of circle centered at [12, -23] with a radius of 8.']
            return commands[:sample_num]
        
        
        # Create sample with collision
        sample_list = set()
        while len(sample_list) < sample_num * ratio:
            random_x_start = random.randint(-self.MAP[0]/2, self.MAP[0]/2)
            random_y_start = random.randint(-self.MAP[1]/2, self.MAP[1]/2)
            start = Point(random_x_start, random_y_start)
            
            random_x_end = random.randint(-self.MAP[0]/2, self.MAP[0]/2)
            random_y_end = random.randint(-self.MAP[1]/2, self.MAP[1]/2)
            end = Point(random_x_end, random_y_end)
            
            line = LineString([(random_x_start, random_y_start), (random_x_end, random_y_end)])
            
            random_x_circle = random.randint(-self.MAP[0]/2, self.MAP[0]/2)
            random_y_circle = random.randint(-self.MAP[1]/2, self.MAP[1]/2)
            random_radius_circle = random.randint(1, min(self.MAP[0]/2 - abs(random_x_circle), self.MAP[1]/2 - abs(random_y_circle)))
            circle = Point(random_x_circle, random_y_circle).buffer(random_radius_circle)
            
            if circle.contains(start) or circle.contains(end) or not line.intersects(circle):
                continue
            
            sample_list.add((random_x_start, random_y_start, random_x_end, random_y_end, random_x_circle, random_y_circle, random_radius_circle))


        # Create sample without collision
        while len(sample_list) < sample_num:
            random_x_start = random.randint(-self.MAP[0]/2, self.MAP[0]/2)
            random_y_start = random.randint(-self.MAP[1]/2, self.MAP[1]/2)
            start = Point(random_x_start, random_y_start)
            
            random_x_end = random.randint(-self.MAP[0]/2, self.MAP[0]/2)
            random_y_end = random.randint(-self.MAP[1]/2, self.MAP[1]/2)
            end = Point(random_x_end, random_y_end)
            
            line = LineString([(random_x_start, random_y_start), (random_x_end, random_y_end)])
            
            random_x_circle = random.randint(-self.MAP[0]/2, self.MAP[0]/2)
            random_y_circle = random.randint(-self.MAP[1]/2, self.MAP[1]/2)
            random_radius_circle = random.randint(1, min(self.MAP[0]/2 - abs(random_x_circle), self.MAP[1]/2 - abs(random_y_circle)))
            circle = Point(random_x_circle, random_y_circle).buffer(random_radius_circle)
            
            if circle.contains(start) or circle.contains(end) or line.intersects(circle):
                continue
            
            sample_list.add((random_x_start, random_y_start, random_x_end, random_y_end, random_x_circle, random_y_circle, random_radius_circle))


        # Create prompts for all list
        commands = []
        for sample in sample_list:
            commands.append(f"""design a path from [{sample[0]}, {sample[1]}] to [{sample[2]}, {sample[3]}] that avoids crossing the area of circle centered at [{sample[4]}, {sample[5]}] with a radius of {sample[6]}.""")
        print(f"Total Number of Samples: {len(commands)}")
        

        # This code is visualization of samples with matplotlib
        if visual:
            for sample in sample_list:
                fig, ax = plt.subplots(figsize=(5, 5))

                circle = plt.Circle((sample[4], sample[5]), sample[6], color='blue', fill=False)
                ax.add_artist(circle)
                ax.plot([sample[0], sample[2]], [sample[1], sample[3]], color='red', linestyle='-')

                ax.set_xlim(-50, 50)
                ax.set_ylim(-50, 50)
                plt.show()
        

        return commands
    
    def parse(start, end, obstacle):
        return f"""design a path from [{start[0]}, {start[1]}] to [{end[0]}, {end[1]}] that avoids crossing the area of circle centered at [{obstacle[0]}, {obstacle[1]}] with a radius of {obstacle[2]}."""