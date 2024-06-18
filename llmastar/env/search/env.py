class Env:
    def __init__(self, x_range, y_range, horizontal_barriers, vertical_barriers):
        self.x_range = x_range  # size of background
        self.y_range = y_range
        self.horizontal_barriers = horizontal_barriers
        self.vertical_barriers = vertical_barriers
        self.motions = [(-1, 0), (-1, 1), (0, 1), (1, 1),
                        (1, 0), (1, -1), (0, -1), (-1, -1)]
        self.obs = self.obs_map()

    def update_obs(self, obs):
        self.obs = obs

    def obs_map(self):
        """
        Initialize obstacles' positions
        :return: map of obstacles
        """

        x = self.x_range
        y = self.y_range
        obs = set()

        for i in range(x):
            obs.add((i, 0))
        for i in range(x):
            obs.add((i, y - 1))

        for i in range(y):
            obs.add((0, i))
        for i in range(y):
            obs.add((x - 1, i))
            
        for barrier in self.horizontal_barriers:
            for i in range(barrier[1], barrier[2]):
                obs.add((i, barrier[0]))
        for barrier in self.vertical_barriers:
            for i in range(barrier[1], barrier[2]):
                obs.add((barrier[0], i))
        
        # for i in range(10, 21):
        #     obs.add((i, 15))
        # for i in range(15):
        #     obs.add((20, i))

        # for i in range(15, 30):
        #     obs.add((30, i))
        # for i in range(16):
        #     obs.add((40, i))

        return obs
