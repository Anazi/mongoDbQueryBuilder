import json

from models.condition import Condition
from models.queryConditionGroup import QueryConditionGroup
from queryBuilder import QueryBuilder

# Example usage
# Build obj for MongoDB query using QueryBuilder
query_builder = QueryBuilder()

single_condition = QueryConditionGroup(
    conditions=[Condition(key="device", value="Watch", operator="==")],
    operator="AND"
)
mongo_query_single_condition = query_builder.build_query(single_condition)
print(f"mongo_query_single_condition: {json.dumps(mongo_query_single_condition, indent=4)} \n\n ---------------------------- \n")  # This should output: {'device': 'Watch'}

input_1 = QueryConditionGroup(
    conditions=[
        QueryConditionGroup(
            conditions=[
                Condition(key="device", value="Watch", operator="!="),
                Condition(key="device", value="iPad", operator="!="),
            ],
            operator="AND"
        ),
        Condition(key="status", value="on", operator="=="),
    ],
    operator="OR"
)
mongo_query_input_1 = query_builder.build_query(input_1)
print(f"mongo_query_input_1: {json.dumps(mongo_query_input_1, indent=4)} \n\n ---------------------------- \n")
'''
This should output: {
    "$or": [
        {
            "$and": [
                {"device": {"$ne": "Watch"}},
                {"device": {"$ne": "iPad"}}
            ]
        },
        {"status": "on"}
    ]
}
'''

input_2 = QueryConditionGroup(
    conditions=[
        Condition(key="device", value="Watch", operator="!="),
        Condition(key="apns.type-mask", value=3, operator="=="),
    ],
    operator="AND"
)
mongo_query_input_2 = query_builder.build_query(input_2)
print(f"mongo_query_input_2: {json.dumps(mongo_query_input_2, indent=4)} \n\n ---------------------------- \n")
'''
This should output: {
    "$and": [
        {"device": {"$ne": "Watch"}},
        {"apns": {"$elemMatch": {"type-mask": 3}}}
    ]
}
'''

input_3 = QueryConditionGroup(
    conditions=[
        Condition(key="device", value="Watch", operator="!="),
        QueryConditionGroup(
            conditions=[
                Condition(key="apns.type-mask", value=1, operator="=="),
                Condition(key="apns.AllowedProtocolMask", value=3, operator="=="),
            ],
            operator="OR"
        )
    ],
    operator="AND"
)
mongo_query_input_3 = query_builder.build_query(input_3)
print(f"mongo_query_input_3: {json.dumps(mongo_query_input_3, indent=4)} \n --------------------------")
'''
This should output: {
    "$and": [
        {"device": {"$ne": "Watch"}},
        {
            "apns": {
                "$elemMatch": {
                    "$or": [
                        {"type-mask": 1},
                        {"AllowedProtocolMask": 3}
                    ]
                }
            }
        }
    ]
}
'''

input_4 = QueryConditionGroup(
    conditions=[
        Condition(key="device", value="Watch", operator="!="),
        QueryConditionGroup(
            conditions=[
                Condition(key="apns.type-mask", value=1, operator="=="),
                Condition(key="apns.AllowedProtocolMask", value=3, operator="=="),
            ],
            operator="OR"
        ),
        Condition(key="apns.example", value="example_value", operator="=="),
    ],
    operator="AND"
)
mongo_query_input_4 = query_builder.build_query(input_4)
print(f"mongo_query_input_4: {json.dumps(mongo_query_input_4, indent=4)} \n\n ---------------------------- \n")
'''
this should output: {
    "$and": [
        {"device": {"$ne": "Watch"}},
        {
            "apns": {
                "$elemMatch": {
                    "$or": [
                        {"type-mask": 1},
                        {"AllowedProtocolMask": 3}
                    ]
                }
            }
        },
        {
            "apns": {
                "$elemMatch": {
                    "example": "example_value"
                }
            }
        }
    ]
}
'''

# A v (B v C) v D
input_5 = QueryConditionGroup(
    conditions=[
        Condition(key="device", value="Watch", operator="!="),
        QueryConditionGroup(
            conditions=[
                Condition(key="apns.type-mask", value=1, operator="=="),
                Condition(key="apns.AllowedProtocolMask", value=3, operator="=="),
            ],
            operator="OR"
        ),
        Condition(key="apns.example", value="ex_val", operator="==")
    ],
    operator="AND"
)
mongo_query_input_5 = query_builder.build_query(input_5)
print(f"mongo_query_input_5: {json.dumps(mongo_query_input_5, indent=4)} \n\n ---------------------------- \n")
'''
This should output: mongo_query_input_5: {
    "$and": [
        {
            "device": {
                "$ne": "Watch"
            }
        },
        {
            "apns": {
                "$elemMatch": {
                    "$or": [
                        {"type-mask": 1},
                        {"AllowedProtocolMask": 3}
                    ]
                }
            }
        },
        {
            "apns": {
                "$elemMatch": {"example": "ex_val"}
            }
        }
    ]
} 
'''


input_6 = QueryConditionGroup(
    conditions=[
        Condition(key="device", value="iPhone", operator="=="),
        QueryConditionGroup(
            conditions=[
                Condition(key="apns.type-mask", value=1, operator="=="),
                Condition(key="apns.AllowedProtocolMask", value=3, operator="=="),
                Condition(key="apns.example", value="ex_val", operator="==")
            ],
            operator="AND"
        )
    ],
    operator="AND"
)
mongo_query_input_6 = query_builder.build_query(input_6)
print(f"mongo_query_input_6: {json.dumps(mongo_query_input_6, indent=4)} \n\n ---------------------------- \n")
'''
This should output: {
    "$and": [
        {"device": "iPhone"},
        {
            "apns": {
                "$elemMatch": {
                    "$or": [
                        {"type-mask": 1},
                        {"AllowedProtocolMask": 3}
                    ]
                }
            }
        }
    ]
}
'''

input_7 = QueryConditionGroup(
    conditions=[
        Condition(key="device", value="iPhone", operator="=="),
        QueryConditionGroup(
            conditions=[
                QueryConditionGroup(
                    conditions=[
                        Condition(key="apns.type-mask", value=1, operator="=="),
                        Condition(key="apns.AllowedProtocolMask", value=3, operator="=="),
                        Condition(key="apns.AllowedProtocolMaskImaginery", value=55, operator="=="),
                    ],
                    operator="AND"
                ),
                Condition(key="apns.example", value="ex_val", operator="=="),
                Condition(key="apns.NewVAl", value="newVAlcheck", operator="==")
            ],
            operator="OR"
        )
    ],
    operator="AND"
)
mongo_query_input_7 = query_builder.build_query(input_7)
print(f"mongo_query_input_7: {json.dumps(mongo_query_input_7, indent=4)} \n\n ---------------------------- \n")
