class Action():
    _action:str = "none"

    def __str__(self) -> str:
        return self._action

    def get_action(self) -> str:
        return self._action

    def update_action(self, new_action:str):
        self._action = new_action