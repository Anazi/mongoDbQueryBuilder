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


# AND/OR for elemMatch together
# ONLY OR is working, so AND need to add it
"""
Abu Jalloh11:25 PM
db.myCollection.find({
  myArray: {
    $elemMatch: {
      $or: [
        {
          fieldA: valueA, // Condition A
          fieldB: valueB  // Condition B
        },
        {
          fieldC: valueC  // Condition C
        }
      ]
    }
  }
})
Abu Jalloh11:31 PM
To construct a query with both AND and OR conditions in MongoDB, you'll typically use the $or operator at the top level of your query and $and operators within each condition set. Here's how you can do it:

Suppose you have a collection of employees with an array of projects they worked on, and you want to find employees where at least one project matches (Web Development AND 2023 Release) or (AI Research).

python
Copy code
db.employees.find({
  $or: [
    {
      "projects": {
        $elemMat
db.employees.find({
  $or: [
    {
      "projects": {
        $elemMatch: {
          $and: [
            { "name": "Web Development" },  // Condition A
            { "name": "2023 Release" }     // Condition B
          ]
        }
      }
    },
    {
      "projects": {
        $elemMatch: {
          "name": "AI Research"  // Condition C
        }
      }
    }
  ]
})
spw-mihd-nui
"""