from enum import Enum


class State(Enum):
    MENU = 0
    USERS_LIST = 2
    ADD_DESIRE = 3
    ADD_TAGS = 4
    CHOOSE_TAG = 4.5
    VIEW = 5


State.ALL = tuple(State)
