from enum import Enum

class MatchType(Enum):
    CORRECT = 0
    HUN_CORRECT = 1
    WORD_CORRECT = 2
    BOTH_FALSE = 3
    BOTH_FALSE_DIFF = 4

