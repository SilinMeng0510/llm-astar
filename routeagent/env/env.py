from shapely.geometry import LineString, Point
import matplotlib.pyplot as plt

from ..utils.utils import parse, parse_search

class Environment:
  def __init__(self, start, end, object, map=(100, 100)):
    self.MAP = map
    self.end, self.start, self.current = end, start, start
    self.search_history, self.path = [], [self.start]
    self.index = 0

    self.obstacles = []
    for i in range(0, len(object), 3):
      self.obstacles.append(Point(object[i], object[i + 1]).buffer(object[i + 2]))

  def step(self, action):
    if action.startswith("> action:"):
      point = parse(action)
      point = (point[0], point[1])
      line = LineString([self.current, point])
      self.current = point
      for obstacle in self.obstacles:
        if line.intersects(obstacle):
          return f"Failed: Collision.\n"
        
      self.path.append(point)
      if point == self.end:
        return f"Success: You have reached the end.\n"
      return f"No collision. You are now at [{self.current[0]}, {self.current[1]}].\n"
    elif action.startswith("> search:"):
      if action in self.search_history:
        return "Failed: You have already taken this action.\n"
      self.search_history.append(action)
      
      self.index += 1
      points = parse_search(action)
      line = LineString(points)
      for obstacle in self.obstacles:
        if line.intersects(obstacle):
          return f"Collision between [{points[0][0]}, {points[0][1]}] and [{points[1][0]}, {points[1][1]}].\n"
      return f"No collision between [{points[0][0]}, {points[0][1]}] and [{points[1][0]}, {points[1][1]}].\n"
    else:
      return "Ok.\n"
