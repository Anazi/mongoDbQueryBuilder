# Condition Model
from typing import Any


class Condition:
    def __init__(self, key: str, value: Any, operator: str = None):
        self.key = key
        self.value = value
        self.operator = operator if operator else "=="
