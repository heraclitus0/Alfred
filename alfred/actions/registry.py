class ActionRegistry:
    def __init__(self):
        self._actions = {}
    def register(self, name, action):
        self._actions[name] = action
    def get(self, name):
        return self._actions[name]
