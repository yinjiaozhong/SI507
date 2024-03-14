import math

def change(amount, coins):
    # base case
    if amount == 0:
        return 0
    # if coins is null or amount<0, return math.inf
    if not coins or amount < 0:
        return math.inf
    # initialize the smallest coin to infinity
    min_coins = math.inf
    # loop structure
    for coin in coins:
        # if coin is bigger than amount, skipping
        if coin > amount:
            continue
        # change the remaining amount plus the current coin count
        num_coins = 1 + change(amount - coin, coins)
        # renew min_coins
        min_coins = min(min_coins, num_coins)
    # if the min_coins is infinity, return math.inf
    if min_coins == math.inf:
        return math.inf
    # return min-coins count
    return min_coins

# test example
print(change(48, [1, 5, 10, 25, 50]))
print(change(48, [1, 7, 24, 42]))
print(change(35, [1, 3, 16, 30, 50]))
print(change(6, [4, 5, 9]))

def giveChange(amount,coins):
    # get the min_coins amount
    min_coins = change(amount, coins)
    # if we didn't change, return math.inf
    if min_coins == math.inf:
        return [math.inf,[]]
    # initialize a list to save change solution
    change_solution = []
    # remaining_amount = amount
    # loop structure until remaining amount is zero
    # order descend
    for coin in sorted(coins, reverse=True):
        # meet two conditions at the same time
        while (amount >= coin and change(amount-coin, coins) == min_coins-1):
            # adding this coin into change solution
            change_solution.append(coin)
            # renew remaining amount
            # remaining_amount -=coin
            amount -= coin
            min_coins -= 1
    # return and order change solution list
    return [len(change_solution), change_solution]

# test example
print(giveChange(48,[1, 5, 10, 25, 50]))
print(giveChange(48, [1, 7, 24, 42]))
print(giveChange(35,[1, 3, 16, 30, 50]))
print(giveChange(6, [4, 5, 9]))
