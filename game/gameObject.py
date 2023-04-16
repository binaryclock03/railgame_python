class GameObject():
    visible = True

    def __init__(self):
        pass

    def draw(self, surface):
        if self.visible:
            self._draw(surface)

    def _draw(self, surface):
        pass