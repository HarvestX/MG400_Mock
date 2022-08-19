"""task manager."""
import collections


class TaskManager:
    """TaskManager"""

    def __init__(self) -> None:
        self.__que = collections.deque("")

    def stack(self, command: str):
        """stack"""
        self.__que.append(command)

    def unstack(self):
        """unstack"""
        return self.__que.pop()
