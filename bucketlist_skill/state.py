from enum import Enum


class State(Enum):
    MENU = 0
    OTHERS_LIST = 1
    USERS_LIST = 2
    ADD = 3


State.ALL = tuple(State)
