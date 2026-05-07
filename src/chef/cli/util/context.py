from typing import Callable


class Context:
    verbose: bool
    crash: Callable[[], None]

    def __init__(self, on_crash: Callable[[], None]):
        self.crash = on_crash
