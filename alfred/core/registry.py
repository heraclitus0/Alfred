class ComponentRegistry:
    def __init__(self) -> None:
        self._components = {}

    def register(self, name: str, component) -> None:
        self._components[name] = component

    def get(self, name: str):
        return self._components[name]
