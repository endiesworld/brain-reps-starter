"""
Day 2 Challenge: Valid Parentheses

Write a function that takes a string s containing just these characters:

( ) { } [ ]

Return True if the input string is valid, otherwise return False.

A string is valid if:

Every opening bracket has a matching closing bracket of the same type.

Brackets close in the correct order.

Every closing bracket has a corresponding earlier opening bracket.

Example

is_valid("()")           # True
is_valid("()[]{}")       # True
is_valid("(]")           # False
is_valid("([)]")         # False
is_valid("{[]}")         # True
is_valid("]")            # False
is_valid("")             # True

Constraints

0 <= len(s) <= 10^4

s contains only ()[]{}

"""

def is_valid(s):
    stack = ["(", "{", "["]
    store = {")" : "(", "]": "[", "}": "{"}
    empty_stack = []
    if len(s) < 1 :
        return True 
    
    for data in s:
        if data in stack:
            empty_stack.append(data)
        else:
          if len(empty_stack) > 0 and store.get(data) == empty_stack[-1]:
              empty_stack.pop()
          else:
            return False 
        
    if len(empty_stack) > 0:
        return False 
    
    return True