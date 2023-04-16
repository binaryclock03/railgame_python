class GameObject():
    visible = True

    def __init__(self):
        pass

    def draw(self):
        if self.visible:
            self._draw()

    def _draw(self, surface):
        pass