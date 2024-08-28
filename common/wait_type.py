from enum import Enum


class WaitType(Enum):

    PRESENCE = "presence"
    CLICKABLE = "clickable"
    VISIBILITY = "visibility"
    INVISIBILITY = "invisibility"
