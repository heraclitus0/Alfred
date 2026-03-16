class BaseAction:
    name = "base"
    def run(self, *args, **kwargs):
        raise NotImplementedError
