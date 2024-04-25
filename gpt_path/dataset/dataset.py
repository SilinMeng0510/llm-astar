import random
from shapely.geometry import LineString, Point
import matplotlib.pyplot as plt


class Dataset:
    def __init__(self):
        self.MAP = (100, 100)

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