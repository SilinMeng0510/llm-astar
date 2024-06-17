"""
RRT_star 2D
@author: huiming zhou
"""

import os
import sys
import math, json
import numpy as np

from routeagent.env.sample import env, plotting, utils, queue
from routeagent.model import ChatGPT
from routeagent.utils import parse_selected_point, encode_image
from .prompt import *

np.random.seed(69)

class Node:
    def __init__(self, n):
        self.x = n[0]
        self.y = n[1]
        self.parent = None


class RrtStar:
    def __init__(self, query, step_len,
                goal_sample_rate, llm_sample_rate, search_radius, iter_max, llm=False):
        response = ChatGPT(method="PARSE", sysprompt=sysprompt_parse, example=example_parse).chat(query, stop=None, max_tokens=None)
        input = json.loads(response)
        print(input)
        x_start = (input["start"][0], input["start"][1])
        x_goal = (input["goal"][0], input["goal"][1])
        
        self.llm = llm
        if self.llm:
            # self.rrt_score = rrt_score
            self.gpt = ChatGPT(method="RRT*", sysprompt=sysprompt_generate, example=None)
        self.s_start = Node(x_start)
        self.s_goal = Node(x_goal)
        self.step_len = step_len
        self.goal_sample_rate = goal_sample_rate
        self.llm_sample_rate = llm_sample_rate
        self.search_radius = search_radius
        self.iter_max = iter_max
        self.vertex = [self.s_start]
        self.vertexstat = [[self.s_start.x, self.s_start.y]]
        self.path = []

        self.env = env.Env(x_range=input["range_x"], y_range=input["range_y"], obs_circle=input["circle_obstacles"], obs_rectangle=input["rectangle_obstacles"])
        self.plotting = plotting.Plotting(x_start, x_goal, self.env)
        self.utils = utils.Utils(self.env)

        self.x_range = self.env.x_range
        self.y_range = self.env.y_range
        self.obs_circle = self.env.obs_circle
        self.obs_rectangle = self.env.obs_rectangle
        self.obs_boundary = self.env.obs_boundary
        
        self.last_generated = ([self.s_start.x, self.s_start.y], "Successfully Added")
        self.chat_history = []

    def update_query_and_history(self):
        query = prompt.format(
            start=[self.s_start.x, self.s_start.y], goal=[self.s_goal.x, self.s_goal.y],
            range_x=[self.x_range[0], self.x_range[1]], range_y=[self.y_range[0], self.y_range[1]],
            circle_obstacles=self.obs_circle, rectangle_obstacles=self.obs_rectangle, vertex=self.vertexstat
        )
        self.chat_history = [
            {"role": "user", "content": query}
        ]

    def planning(self):
        operations = 0
        if self.llm:
            self.plotting.animation(self.vertex, self.path, "rrt*", plot_path=False)
            self.update_query_and_history()

        for k in range(self.iter_max):
            operations += 1
            node_rand = self.generate_random_node(self.goal_sample_rate, self.llm_sample_rate)
            node_near = self.nearest_neighbor(self.vertex, node_rand)
            node_new = self.new_state(node_near, node_rand)
            print(f'Rand: ({node_rand.x}, {node_rand.y})', f'Near: ({node_near.x}, {node_near.y})')
            if k % 500 == 0:
                print(k)

            if node_new and not self.utils.is_collision(node_near, node_new):
                neighbor_index = self.find_near_neighbor(node_new)
                self.vertex.append(node_new)
                self.vertexstat.append([node_new.x, node_new.y])

                if neighbor_index:
                    self.choose_parent(node_new, neighbor_index)
                    self.rewire(node_new, neighbor_index)
                
                self.plotting.animation(self.vertex, self.path, "rrt*", plot_path=False, map=True)

        index = self.search_goal_parent()
        self.path = self.extract_path(self.vertex[index])
        cost = self.get_path_length(self.path)

        self.plotting.animation(self.vertex, self.path, "rrt*, N = " + str(self.iter_max))
        result = {"path": self.path, "operations": operations, "cost": cost}
        print(result)
        return result

    def new_state(self, node_start, node_goal):
        dist, theta = self.get_distance_and_angle(node_start, node_goal)

        dist = min(self.step_len, dist)
        node_new = Node((node_start.x + dist * math.cos(theta),
                         node_start.y + dist * math.sin(theta)))

        node_new.parent = node_start

        return node_new

    def choose_parent(self, node_new, neighbor_index):
        cost = [self.get_new_cost(self.vertex[i], node_new) for i in neighbor_index]

        cost_min_index = neighbor_index[int(np.argmin(cost))]
        node_new.parent = self.vertex[cost_min_index]

    def rewire(self, node_new, neighbor_index):
        for i in neighbor_index:
            node_neighbor = self.vertex[i]

            if self.cost(node_neighbor) > self.get_new_cost(node_new, node_neighbor):
                node_neighbor.parent = node_new

    def search_goal_parent(self):
        dist_list = [math.hypot(n.x - self.s_goal.x, n.y - self.s_goal.y) for n in self.vertex]
        node_index = [i for i in range(len(dist_list)) if dist_list[i] <= self.step_len]

        if len(node_index) > 0:
            cost_list = [dist_list[i] + self.cost(self.vertex[i]) for i in node_index
                        if not self.utils.is_collision(self.vertex[i], self.s_goal)]
            return node_index[int(np.argmin(cost_list))]

        return len(self.vertex) - 1

    def get_new_cost(self, node_start, node_end):
        dist, _ = self.get_distance_and_angle(node_start, node_end)

        return self.cost(node_start) + dist

    def generate_random_node(self, goal_sample_rate, llm_sample_rate):
        delta = self.utils.delta
        if np.random.random() > goal_sample_rate:
            if self.llm and np.random.random() < llm_sample_rate:
                self.plotting.animation(self.vertex, self.path, "rrt*", plot_path=False, map=True)
                self.update_query_and_history()
                
                response = self.gpt.chat_with_image(chat_history=self.chat_history, stop=None, max_tokens=None)
                self.chat_history.append({"role": "assistant", "content": response})
                print(response)
                return Node(parse_selected_point(response, [self.s_goal.x, self.s_goal.y]))
            
            return Node((np.random.uniform(self.x_range[0] + delta, self.x_range[1] - delta),
                        np.random.uniform(self.y_range[0] + delta, self.y_range[1] - delta)))

        return self.s_goal

    def find_near_neighbor(self, node_new):
        n = len(self.vertex) + 1
        r = min(self.search_radius * math.sqrt((math.log(n) / n)), self.step_len)

        dist_table = [math.hypot(nd.x - node_new.x, nd.y - node_new.y) for nd in self.vertex]
        dist_table_index = [ind for ind in range(len(dist_table)) if dist_table[ind] <= r and
                            not self.utils.is_collision(node_new, self.vertex[ind])]

        return dist_table_index
    
    def get_path_length(self, path):
        for i in range(len(path) - 1):
            node_front = Node((path[i][0], path[i][1]))
            node_back = Node((path[i + 1][0], path[i + 1][1]))
            if self.utils.is_collision(node_front, node_back):
                print(path[i], path[i+1])
                return float('inf')
        return sum([math.hypot(path[i][0] - path[i + 1][0], path[i][1] - path[i + 1][1]) for i in range(len(path) - 1)])

    @staticmethod
    def nearest_neighbor(node_list, n):
        return node_list[int(np.argmin([math.hypot(nd.x - n.x, nd.y - n.y)
                                        for nd in node_list]))]

    @staticmethod
    def cost(node_p):
        node = node_p
        cost = 0.0

        while node.parent:
            cost += math.hypot(node.x - node.parent.x, node.y - node.parent.y)
            node = node.parent

        return cost

    def update_cost(self, parent_node):
        OPEN = queue.QueueFIFO()
        OPEN.put(parent_node)

        while not OPEN.empty():
            node = OPEN.get()

            if len(node.child) == 0:
                continue

            for node_c in node.child:
                node_c.Cost = self.get_new_cost(node, node_c)
                OPEN.put(node_c)

    def extract_path(self, node_end):
        path = [[self.s_goal.x, self.s_goal.y]]
        node = node_end

        while node.parent is not None:
            path.append([node.x, node.y])
            node = node.parent
        path.append([node.x, node.y])

        return path

    @staticmethod
    def get_distance_and_angle(node_start, node_end):
        dx = node_end.x - node_start.x
        dy = node_end.y - node_start.y
        return math.hypot(dx, dy), math.atan2(dy, dx)