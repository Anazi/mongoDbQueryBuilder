# QueryConditionGroup Model
from typing import List, Union

from models.condition import Condition


class QueryConditionGroup:
    def __init__(
            self,
            conditions: List[Union[Condition, "QueryConditionGroup"]],
            operator: str = None,
    ):
        self.conditions = conditions
        self.operator = operator if operator else "AND"
