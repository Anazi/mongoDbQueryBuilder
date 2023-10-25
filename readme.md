
# MongoDB Query Builder

A Python-based query builder to generate MongoDB queries based on structured input.

## Features

1. **Simple Text Search**: Supports simple queries with just a text box.
2. **Advanced Search Form**: Allows complex queries by filling out a form for each condition.
3. **Logical Operators**: Enables usage of logical operators like "AND", "OR".
4. **Nested Queries**: Facilitates complex nested queries.


## Usage Examples

---

### Simple Text Search

#### Input

```python
simple_search = QueryConditionGroup(
    conditions=[Condition(key="name", value="John", operator="==")],
    operator="AND"
)
```

#### Output MongoDB Query

```json
{
    "name": "John"
}
```

---

### Advanced Search Form

#### Input

```python
advanced_search = QueryConditionGroup(
    conditions=[
        Condition(key="name", value="John", operator="=="),
        Condition(key="age", value=30, operator=">=")
    ],
    operator="AND"
)
```

#### Output MongoDB Query

```json
{
    "$and": [
        {"name": "John"},
        {"age": {"$gte": 30}}
    ]
}
```

---

### Logical Operators

#### Input

```python
logical_operators = QueryConditionGroup(
    conditions=[
        Condition(key="name", value="John", operator="=="),
        QueryConditionGroup(
            conditions=[
                Condition(key="age", value=30, operator=">="),
                Condition(key="age", value=40, operator="<")
            ],
            operator="OR"
        )
    ],
    operator="AND"
)
```

#### Output MongoDB Query

```json
{
    "$and": [
        {"name": "John"},
        {
            "$or": [
                {"age": {"$gte": 30}},
                {"age": {"$lt": 40}}
            ]
        }
    ]
}
```

---

### Nested Queries

#### Input

```python
nested_query = QueryConditionGroup(
    conditions=[
        Condition(key="name", value="John", operator="=="),
        QueryConditionGroup(
            conditions=[
                Condition(key="age", value=30, operator=">="),
                QueryConditionGroup(
                    conditions=[
                        Condition(key="city", value="NY", operator="=="),
                        Condition(key="city", value="SF", operator=="==")
                    ],
                    operator="OR"
                )
            ],
            operator="AND"
        )
    ],
    operator="AND"
)
```

#### Output MongoDB Query

```json
{
    "$and": [
        {"name": "John"},
        {
            "$and": [
                {"age": {"$gte": 30}},
                {
                    "$or": [
                        {"city": "NY"},
                        {"city": "SF"}
                    ]
                }
            ]
        }
    ]
}
```

---
