<br/>
<p align="center"> <img width="1000" src="https://github.com/SilinMeng0510/RouteAgent/assets/89226819/7bc8d029-4707-4b42-9c0d-41a11de95814">


[![Downloads](https://static.pepy.tech/badge/termax)](https://pepy.tech/project/termax) ![PyPI - Version](https://img.shields.io/pypi/v/termax)


# Overview
Route-agent performs path planning with GPT and LLMs.

## Installation
```bash
pip install routeagent
```

## Quick Start
```python
from routeagent import RePE

query = "design a path from [10, 0] to [0, 10] that avoids crossing the area of circle centered at [5, 5] with a radius of 4."
pather = RePE()
pather.run(query)
```


