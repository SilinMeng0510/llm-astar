from .planner import ActionEffect, FewShot, ChainOfThought, RePE, ReAct
from .agent import ActionEffectAgent, ReActAgent
from .dataset import Dataset

from shapely.geometry import LineString, Point
import matplotlib.pyplot as plt

import sys
import time
import inquirer

commands = Dataset().generate(sample_num=30, ratio=1, fix=True, visual=False)
# commands = ["design a path from [-5, -22] to [38, 19] that avoids crossing the area of circle centered at [-10, 6] with a radius of 26."]
records = []

action_planner = [
    inquirer.List(
        'approach',
        message="Choose your approach",
        choices=[('Model as Agent', 0), ('Model as Planner', 1)],
        carousel=False
    )
]
decision = inquirer.prompt(action_planner)['approach']

if decision == 1:
    methods = [
        inquirer.List(
            "technique",
            message="Which Agent are you using",
            choices=[('Standard (FewShot)', "FS"), ('RePE', 'RePE'), ('Read-Only (CoT)', "COT"), ('Act-Only', "AE"), ('ReAct', "ReAct")],
        )
    ]
    method = inquirer.prompt(methods)['technique']

    if method == "COT":
        pather = ChainOfThought()
    elif method == "RePE":
        pather = RePE()
    elif method == "FS":
        pather = FewShot()
    elif method == "ReAct":
        pather = ReAct()
    elif method == "AE":
        pather = ActionEffect()
    else:
        print("Invalid method id")
        sys.exit()
else:
    methods = [
        inquirer.List(
            "technique",
            message="Which Agent are you using",
            choices=[('Act-Only', "AE_A"), ('ReAct', "ReAct_A")],
        )
    ]
    method = inquirer.prompt(methods)['technique']

    if method == "ReAct_A":
        pather = ReActAgent()
    elif method == "AE_A":
        pather = ActionEffectAgent()
    else:
        print("Invalid method id")
        sys.exit()
    

for i in range(len(commands)): records.append(pather.run(commands[i]))

with open(f"outcome/{method}/evaluation.txt", 'w') as file:
    count = 0
    se_count = 0
    collision_free_count = 0
    sat_set = set()
    for record in records:
        count += 1
        
        object = record["object"]
        path = record["path"]
        
        
        # print out the record
        file.write(f"START-{count}: ")
        file.write(f"({object[0]}, {object[1]}), ")
        file.write(f"END-{count}: ")
        file.write(f"({object[2]}, {object[3]})\n")
        file.write(f"OBJECT-{count}: ")
        file.write(f"circle:({object[4]}, {object[5]}) with radius={object[6]}\n")
        file.write(f"PATH-{count}: ")
        file.write(f"{path}\n")
        
        # Evaluate the Result
        path_list = [(point[0], point[1]) for point in path]
        if len(path_list) < 2:
            file.write(f"START-END EVALUATION-{count}: ")
            file.write("Not Satisfied\n")
            
            file.write(f"PATH EVALUATION-{count}: ")
            file.write("Collide\n\n")
        
        line = LineString(path_list)
        circle = Point(object[4], object[5]).buffer(object[6])
        
        sat = 0
        if object[0] == path[0][0] and object[1] == path[0][1] and object[2] == path[-1][0] and object[3] == path[-1][1]:
            file.write(f"START-END EVALUATION-{count}: ")
            file.write("Satisfied\n")
            se_count += 1
            sat = 1
        else:
            file.write(f"START-END EVALUATION-{count}: ")
            file.write("Not Satisfied\n")
        
        if line.intersects(circle):
            file.write(f"PATH EVALUATION-{count}: ")
            file.write("Collide\n\n")
        else:
            file.write(f"PATH EVALUATION-{count}: ")
            file.write("Not Collide\n\n")
            collision_free_count += sat
            if sat: sat_set.add(count)
        
        # Visualize the answer
        fig, ax = plt.subplots(figsize=(5, 5))

        circle = plt.Circle((object[4], object[5]), object[6], color='blue', fill=False)
        ax.add_artist(circle)
        ax.plot([point[0] for point in path], [point[1] for point in path], color='red', linestyle='-')

        ax.set_xlim(-65, 65)
        ax.set_ylim(-65, 65)
        plt.savefig(f"outcome/{method}/plots/plot-{count}.png")
    
    file.write("******************************************************************************************\n")
    file.write(f"SE_SAT RATIO: {se_count}/{count}\n")
    file.write(f"COLLISION_FREE ACCURACY: {collision_free_count}/{count}\n")
    file.write(f"COLLISION_FREE TO SE_SAT RATIO: {collision_free_count}/{se_count}\n\n")
    
    
    file.write(f"SATISFIED SAMPLE ID: {sat_set}")
        
