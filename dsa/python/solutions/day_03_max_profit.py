"""
You are given a list prices where prices[i] is the price of a stock on day i.

Choose one day to buy and a different future day to sell.

Return the maximum profit you can achieve. If no profit is possible, return 0.

Function signature

Example 1
prices = [7, 1, 5, 3, 6, 4]
# Output: 5
# Buy at 1, sell at 6
Example 2
prices = [7, 6, 4, 3, 1]
# Output: 0
# No profit possible
Constraints

1 <= len(prices) <= 10^5

0 <= prices[i] <= 10^4
    
"""

def max_profit(prices):
    max_profit = 0
    buy = prices[0]
    sell = 0

    for price in prices:
        if price < buy:
            buy = price
        elif max_profit < price - buy:
            sell = price
            max_profit = price - buy
    return max_profit
