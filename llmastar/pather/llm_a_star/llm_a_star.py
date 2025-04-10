import json
import math
import heapq
import torch

from llmastar.env.search import env, plotting
from llmastar.model import ChatGPT, Llama3, Qwen, RAG
from llmastar.utils import is_lines_collision, list_parse

class LLMAStar:
    """LLM-A* algorithm with cost + heuristics as the priority."""
    
    GPT_METHOD_PARSE = "PARSE"
    GPT_METHOD_LLMASTAR = "LLM-A*"

    def __init__(self, llm='qwen', variant='Qwen2.5-7B-Instruct', prompt='standard', device=None, use_rag=False, dataset_path='dataset_sft/environment_50_30.json'):
        if device is None:
            device=torch.device("cuda:0")
        self.llm = llm
        self.prompt_type = prompt
        self.use_rag = use_rag
        
        # Initialize RAG if enabled
        if self.use_rag:
            self.rag = RAG(dataset_path=dataset_path)
        
        assert self.prompt_type in ['standard', 'cot', 'repe'], "Invalid prompt type. Choose 'standard', 'cot', or 'repe'."
        
        if self.llm == 'gpt':
            self.parser = ChatGPT(method=self.GPT_METHOD_PARSE)
            self.model = ChatGPT(method=self.GPT_METHOD_LLMASTAR)
        elif self.llm == 'llama':
            self.model = Llama3(device=device, variant=variant)
        elif self.llm == 'qwen':
            self.model = Qwen(device=device, variant=variant)
        else:
            raise ValueError("Invalid LLM model. Choose 'gpt', 'llama', or 'qwen'.")

    def _parse_query(self, query):
        """Parse input query using the specified LLM model."""
        if isinstance(query, str):
            if self.llm == 'gpt':
                response = self.parser.chat(query)
                print(response)
                return json.loads(response)
            elif self.llm == 'llama':
                response = self.model.ask(self.model.get_prompt("parse", query=query))
                print(response)
                return json.loads(response)
            elif self.llm == 'qwen':
                response = self.model.ask(self.model.get_prompt("parse", query=query))
                print(response)
                return json.loads(response)
            else:
                raise ValueError("Invalid LLM model.")
        return query

    def _initialize_parameters(self, input_data):
        """Initialize environment parameters from input data."""
        self.s_start = tuple(input_data['start'])
        self.s_goal = tuple(input_data['goal'])
        self.horizontal_barriers = input_data['horizontal_barriers']
        self.vertical_barriers = input_data['vertical_barriers']
        self.range_x = input_data['range_x']
        self.range_y = input_data['range_y']
        self.Env = env.Env(self.range_x[1], self.range_y[1], self.horizontal_barriers, self.vertical_barriers)
        self.plot = plotting.Plotting(self.s_start, self.s_goal, self.Env)
        # Adjust range limits
        self.range_x[1] -= 1
        self.range_y[1] -= 1
        self.u_set = self.Env.motions
        self.obs = self.Env.obs
        self.OPEN = []
        self.CLOSED = []
        self.PARENT = dict()
        self.g = dict()

    def _initialize_llm_paths(self):
        """Initialize paths using LLM suggestions."""
        start, goal = list(self.s_start), list(self.s_goal)
        prompt_params = {
            'start': start, 
            'goal': goal,
            'horizontal_barriers': self.horizontal_barriers,
            'vertical_barriers': self.vertical_barriers
        }

        # Enhance prompt with RAG if enabled
        rag_examples = ""
        if self.use_rag:
            # Create a query dict for RAG
            rag_query = {
                'start': start,
                'goal': goal,
                'horizontal_barriers': self.horizontal_barriers,
                'vertical_barriers': self.vertical_barriers,
                'range_x': self.range_x,
                'range_y': self.range_y,
                'start_goal': [
                    {
                        'start': start,
                        'goal': goal,
                        # Use waypoints_intelligent key for RAG similarity
                    }
                ]
            }
            
            # Retrieve similar examples
            examples = self.rag.retrieve_examples(rag_query, top_k=3)
            
            # Format examples for the prompt
            if examples:
                rag_examples = self.rag.format_examples_for_prompt(examples)
                print("RAG examples found:", len(examples))
                print("RAGGGG:", rag_examples)
            else:
                print("No RAG examples found")

        if self.llm == 'gpt':
            # For GPT, we need to manually format the prompt
            from llmastar.model.prompts.gpt_prompts import GPT_PROMPTS
            query = GPT_PROMPTS[self.prompt_type].format(**prompt_params)
            
            # Add RAG examples if available
            if self.use_rag and rag_examples:
                query = query + rag_examples
                
            response = self.model.ask(prompt=query, max_tokens=1000)
        elif self.llm == 'llama':
            # For Llama, we use the get_prompt method
            prompt = self.model.get_prompt(self.prompt_type, **prompt_params)
            
            # Add RAG examples if available
            if self.use_rag and rag_examples:
                prompt_parts = prompt.split("<|eot_id|>")
                # Insert RAG examples before the last assistant part
                if len(prompt_parts) >= 3:
                    prompt_parts[-2] = prompt_parts[-2] + rag_examples
                    prompt = "<|eot_id|>".join(prompt_parts)
                
            response = self.model.ask(prompt)
        elif self.llm == 'qwen':
            # For Qwen, we use the get_prompt method
            prompt = self.model.get_prompt(self.prompt_type, **prompt_params)
            
            # Add RAG examples if available
            if self.use_rag and rag_examples:
                prompt_parts = prompt.split("<|eot_id|>")
                # Insert RAG examples before the last assistant part
                if len(prompt_parts) >= 3:
                    prompt_parts[-2] = prompt_parts[-2] + rag_examples
                    prompt = "<|eot_id|>".join(prompt_parts)
                
            response = self.model.ask(prompt)
        else:
            raise ValueError("Invalid LLM model.")

        nodes = list_parse(response)
        self.target_list = self._filter_valid_nodes(nodes)

        if not self.target_list or self.target_list[0] != self.s_start:
            self.target_list.insert(0, self.s_start)
        if not self.target_list or self.target_list[-1] != self.s_goal:
            self.target_list.append(self.s_goal)
        print(self.target_list)
        self.i = 1
        self.s_target = self.target_list[1]
        print(self.target_list[0], self.s_target)

    def _filter_valid_nodes(self, nodes):
        """Filter out invalid nodes based on environment constraints."""
        return [(node[0], node[1]) for node in nodes
                if (node[0], node[1]) not in self.obs
                and self.range_x[0] + 1 < node[0] < self.range_x[1] - 1
                and self.range_y[0] + 1 < node[1] < self.range_y[1] - 1]

    def searching(self, query, filepath='temp.png'):
        """
        A* searching algorithm.
        :return: Path and search metrics.
        """
        self.filepath = filepath
        print(query)
        input_data = self._parse_query(query)
        self._initialize_parameters(input_data)
        self._initialize_llm_paths()
        
        self.PARENT[self.s_start] = self.s_start
        self.g[self.s_start] = 0
        heapq.heappush(self.OPEN, (self.f_value(self.s_start), self.s_start))

        while self.OPEN:
            _, s = heapq.heappop(self.OPEN)
            self.CLOSED.append(s)

            if s == self.s_goal:  # stop condition
                break

            for s_n in self.get_neighbor(s):
                if s_n == self.s_target and self.s_goal != self.s_target :
                    self._update_target()
                    self._update_queue()
                    print(s_n, self.s_target)
                    
                if s_n in self.CLOSED:
                    continue

                new_cost = self.g[s] + self.cost(s, s_n)
                if s_n not in self.g:
                    self.g[s_n] = math.inf
                    
                if new_cost < self.g[s_n]:  # conditions for updating Cost
                    self.g[s_n] = new_cost
                    self.PARENT[s_n] = s
                    heapq.heappush(self.OPEN, (self.f_value(s_n), s_n))

        path = self.extract_path(self.PARENT)
        visited = self.CLOSED
        result = {
            "operation": len(self.CLOSED),
            "storage": len(self.g),
            "length": sum(self._euclidean_distance(path[i], path[i+1]) for i in range(len(path)-1)),
            "llm_output": self.target_list
        }
        print(result)
        self.plot.animation_with_waypoints(path, visited, self.target_list, True, "LLM-A*", self.filepath)
        return result

    @staticmethod
    def _euclidean_distance(p1, p2):
        return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

    def _update_queue(self):
        queue = []
        for _, s in self.OPEN:
            heapq.heappush(queue, (self.f_value(s), s))
        self.OPEN = queue

    def _update_target(self):
        """Update the current target in the path."""
        self.i += 1
        if self.i < len(self.target_list):
            self.s_target = self.target_list[self.i]

    def get_neighbor(self, s):
        """Find neighbors of state s that are not in obstacles."""
        return [(s[0] + u[0], s[1] + u[1]) for u in self.u_set]

    def cost(self, s_start, s_goal):
        """Calculate cost for the motion from s_start to s_goal."""
        return math.inf if self.is_collision(s_start, s_goal) else math.hypot(s_goal[0] - s_start[0], s_goal[1] - s_start[1])

    def is_collision(self, s_start, s_end):
        """Check if the line segment (s_start, s_end) collides with any barriers."""
        line1 = [s_start, s_end]
        return any(is_lines_collision(line1, [[h[1], h[0]], [h[2], h[0]]]) for h in self.horizontal_barriers) or \
                any(is_lines_collision(line1, [[v[0], v[1]], [v[0], v[2]]]) for v in self.vertical_barriers) or \
                any(is_lines_collision(line1, [[x, self.range_y[0]], [x, self.range_y[1]]]) for x in self.range_x) or \
                any(is_lines_collision(line1, [[self.range_x[0], y], [self.range_x[1], y]]) for y in self.range_y)

    def f_value(self, s):
        """Compute the f-value for state s."""
        return self.g[s] + self.heuristic(s)

    def extract_path(self, PARENT):
        """Extract the path based on the PARENT set."""
        path = [self.s_goal]
        while path[-1] != self.s_start:
            path.append(PARENT[path[-1]])
        return path[::-1]

    def heuristic(self, s):
        """Calculate heuristic value."""
        return math.hypot(self.s_goal[0] - s[0], self.s_goal[1] - s[1]) + math.hypot(self.s_target[0] - s[0], self.s_target[1] - s[1])

