Abstract
------
Path planning is a fundamental scientific problem in robotics and autonomous navigation, requiring the derivation of efficient routes from starting to destination points while avoiding obstacles. Traditional algorithms like A* and its variants are capable of ensuring path validity but suffer from significant computational and memory inefficiencies as the state space grows. Conversely, large language models (LLMs) excel in broader environmental analysis through contextual understanding, providing global insights into environments. However, they fall short in detailed spatial and temporal reasoning, often leading to invalid or inefficient routes. In this work, we propose **LLM-A***, an new LLM based route planning method that synergistically combines the precise pathfinding capabilities of A* with the global reasoning capability of LLMs. This hybrid approach aims to enhance pathfinding efficiency in terms of time and space complexity while maintaining the integrity of path validity, especially in large-scale scenarios. By integrating the strengths of both methodologies, **LLM-A*** addresses the computational and memory limitations of conventional algorithms without compromising on the validity required for effective pathfinding.

Directory Structure
------
    .
    └── dataset
    └── env
        └── search
    └── model
        ├── chatgpt
        └── llama3
    └── pather
        ├── astar
        └── llm_astar
    └── utils

## ⏬ Installation
```bash
pip install llm-astar
```

## 🚀 Quick Start
```python
import openai
openai.api_key = "YOUR API KEY"

from llmastar.pather import AStar, LLMAStar
query = {"start": [5, 5], "goal": [27, 15], "size": [51, 31],
        "horizontal_barriers": [[10, 0, 25], [15, 30, 50]],
        "vertical_barriers": [[25, 10, 22]],
        "range_x": [0, 51], "range_y": [0, 31]}
astar = AStar().searching(query=query, filepath='astar.png')
llm = LLMAStar(llm='gpt', prompt='standard').searching(query=query, filepath='llm.png')
```

## 📝 Citation
If you found this work helpful, please consider citing it using the following:
```
LLM-A*: Large Language Model Enhanced Incremental Heuristic Search on Path Planning
Silin Meng, Yiwei Wang, Cheng-Fu Yang, Nanyun Peng, Kai-Wei Chang
```

## 💫 Showcase
<br/>
<p align="center"> <img width="1000" src="https://github.com/SilinMeng0510/llm-astar/assets/89226819/36ff049f-4e4e-453b-9454-2d6441ad79c0">

## 🪪 License
MIT. Check `LICENSE`.

[![Downloads](https://static.pepy.tech/badge/llm-astar)](https://pepy.tech/project/llm-astar) ![PyPI - Version](https://img.shields.io/pypi/v/llm-astar)


