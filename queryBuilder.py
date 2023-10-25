from models.condition import Condition
from models.queryConditionGroup import QueryConditionGroup

import logging
from typing import List, Dict, Optional

logging.basicConfig(level=logging.INFO)

ELEM_MATCH_KEYS = ['apns']


class QueryBuilder:

    def __init__(self):
        self.operator_mapping = {
            "==": lambda k, v: {k: v},
            "!=": lambda k, v: {k: {"$ne": v}},
            ">": lambda k, v: {k: {"$gt": v}},
            ">=": lambda k, v: {k: {"$gte": v}},
            "<": lambda k, v: {k: {"$lt": v}},
            "<=": lambda k, v: {k: {"$lte": v}},
        }

    def process_condition(self, condition: Condition) -> dict:
        query = self.operator_mapping.get(condition.operator)
        if query:
            return query(condition.key, condition.value)
        else:
            logging.error(f"Unsupported operator: {condition.operator}")
            raise ValueError(f"Unsupported operator: {condition.operator}")

    def build_query(self, group: QueryConditionGroup, recursive_elem_match_cache: Optional[Dict[str, List[Dict]]] = None) -> dict:
        if recursive_elem_match_cache is None:
            recursive_elem_match_cache = {}

        if not group.conditions:
            logging.warning("QueryConditionGroup has no conditions.")
            return {}

        queries = []
        for idx, condition_or_group in enumerate(group.conditions):
            if isinstance(condition_or_group, Condition):
                condition_query = self.process_condition(condition_or_group)
                for key in ELEM_MATCH_KEYS:
                    if key in condition_or_group.key:
                        if key not in recursive_elem_match_cache:
                            recursive_elem_match_cache[key] = []
                        sub_key = condition_or_group.key.split('.', 1)[1]
                        condition_query = {sub_key: condition_query[condition_or_group.key]}
                        recursive_elem_match_cache[key].append(condition_query)
                        break
                else:
                    queries.append(condition_query)
            elif isinstance(condition_or_group, QueryConditionGroup):
                sub_query = self.build_query(condition_or_group, {})
                queries.append(sub_query)

        if recursive_elem_match_cache:
            for key, value in recursive_elem_match_cache.items():
                # If there is more than one elemMatch query for a key, we need to wrap them in an $or or $and
                mongo_operator = f"${group.operator.lower()}"
                if len(value) > 1:
                    queries.append({key: {"$elemMatch": {mongo_operator: value}}})
                else:
                    queries.append({key: {"$elemMatch": value[0]}})

        if len(queries) == 1:
            return queries[0]

        if group.operator == "AND":
            return {"$and": queries}
        elif group.operator == "OR":
            return {"$or": queries}
        else:
            logging.error(f"Invalid operator in QueryConditionGroup: {group.operator}")
            raise ValueError(f"Invalid operator in QueryConditionGroup: {group.operator}")
