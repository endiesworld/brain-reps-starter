"""Day 01 — Two Sum
Problem: Two Sum

Given an array of integers nums and an integer target, return the indices of the two numbers such that they add up to target.

You may assume that:

each input has exactly one solution

you may not use the same element twice

You can return the answer in any order.

Example 1

Input:
nums = [2, 7, 11, 15]
target = 9

Output:
[0, 1]

Explanation:
Because nums[0] + nums[1] = 2 + 7 = 9, the answer is [0, 1].

Example 2

Input:
nums = [3, 2, 4]
target = 6

Output:
[1, 2]

Example 3

Input:
nums = [3, 3]
target = 6

Output:
[0, 1]

Constraints

2 <= nums.length <= 10^4

-10^9 <= nums[i] <= 10^9

-10^9 <= target <= 10^9

Only one valid answer exists

Implement the solution and keep it clean.
"""

def two_sum(nums, target):
    """Return indices of the two numbers such that they add up to target."""
    # TODO: implement
    # Steps
    
    # if not nums or len(nums) < 2:
    #     raise ValueError("Input list must contain at least two numbers.")
    # if len(nums) == 2:
    #     if nums[0] + nums[1] == target:
    #         return [0, 1]
    # # 1: Create a hashmap to store the originimal numbers and their current index
    
    # store = {}
    # index = 0
    # for num in nums:
    #     store[num] = index
    #     index += 1

    # # 2: sort the origininal list
    # sorted_nums = sorted(nums)
    # result = None
    # # 3: iterate and compare
    # for index, number in enumerate(sorted_nums):
    #     compare = sorted_nums[index + 1: ]
    #     for number_b in compare:
    #         if number + number_b == target :
    #             result = [number, number_b]
    #             break
    #         elif number + number_b > target:
    #             break
    #     if result:
    #         break

    # if result:
    #     final_result = [store[result[0]], store[result[1]]]
    #     return final_result
    store = {}
    for index, num in enumerate(nums):
        reminder = target - num
        if reminder in store:
            return [store[reminder], index]
        store[num] = index

    raise NotImplementedError
