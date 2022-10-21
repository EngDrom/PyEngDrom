
import time
import numpy as np

class Animation:
    def __init__(self, project, path):
        self.animations = []
        with open(path, 'r') as file:
            text = file.read()
            animations = text.split("--- animation ---")

            for animation in animations:
                lines = animation.split("\n")
                data = "\n".join(lines[1:])

                if lines[0].startswith("atlas.animation"):
                    self.animations.append(AtlasAnimation(project, data))
    def update(self, media):
        if not hasattr(self, "time"): self.time = time.time()
        delta_t = time.time() - self.time
        self.time += delta_t
        for animation in self.animations:
            animation.update(media, delta_t)

class AtlasAnimation:
    def __init__(self, project, string):
        lines = string.split("\n")

        self.modes = {  }

        for line in lines:
            mode, data = line.split(": ")
            _data = data.split(" ")

            self.modes[mode] = (self.make_interval_array(_data[:-1]), int(_data[-1]))
        self.current_mode = "media dx"
        self.current_time = 0
        self.last_pos = np.array([0.0, 0.0, 0.0])
        self.xmode = 0
    def make_interval_array(self, data):
        array = []
        for i in data:
            if "-" in i:
                a, b, *jump = i.split("-")
                jump = 1 if len(jump) != 1 else int(jump[0])
                
                array.extend(range(int(a), int(b) + 1, jump))
            else:
                array.append(int(i))
        return array

    def update(self, media, delta_t):
        pos = media.get_position()
        delta_p = pos - self.last_pos
        self.last_pos = pos

        mode = [ "media" ]
        if delta_p[0] != 0:
            mode.append("dx")
            self.xmode = 0 if delta_p[0] > 0 else 1
        if delta_p[1] != 0:
            mode.append("dy")
        
        _mode = " ".join(mode) # TODO find all possible modes and take best
        if _mode in self.modes and _mode != self.current_mode:
            self.current_mode = _mode
            self.current_time = - delta_t * 1000

        self.current_time += delta_t * 1000
        data, sleep = self.modes[self.current_mode]
        count = (int(self.current_time) // sleep) % len(data)
        
        media.make_atlas_tcoord_matrix(data[count], self.xmode)
