


class Env:
    def __init__(self, x_range, y_range, obs_circle, obs_rectangle):
        self.x_range = (x_range[0], x_range[1])
        self.y_range = (y_range[0], y_range[1])
        self.obs_boundary = [
            [x_range[0], y_range[0], 1, y_range[1]],
            [x_range[0], y_range[1], x_range[1], 1],
            [x_range[0], y_range[0], x_range[1], 1],
            [x_range[1], y_range[0], 1, y_range[1]+1]
        ]
        self.obs_circle = obs_circle
        self.obs_rectangle = obs_rectangle

    def obs_boundary(self):
        return self.obs_boundary

    def obs_rectangle(self):
        return self.obs_rectangle

    def obs_circle(self):
        return self.obs_circle
