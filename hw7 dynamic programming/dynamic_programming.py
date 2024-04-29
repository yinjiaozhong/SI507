import math

def change(amount, coins):
    """
    Returns the minimum number of coins required to make up the given amount of money.
    If there is no possible solution, returns math.inf.
    """
    dp = [math.inf] * (amount + 1)
    dp[0] = 0

    for i in range(1, amount + 1):
        for coin in coins:
            if i - coin >= 0:
                dp[i] = min(dp[i], dp[i - coin] + 1)

    return dp[amount]

def giveChange(amount, coins):
    """
    Returns a list whose first member is the minimum number of coins required
    and whose second member is a list of the coins in the optimal solution.
    """
    dp = [[math.inf, []] for _ in range(amount + 1)]
    dp[0] = [0, []]

    for i in range(1, amount + 1):
        for coin in coins:
            if i - coin >= 0:
                if dp[i - coin][0] + 1 < dp[i][0]:
                    dp[i] = [dp[i - coin][0] + 1, dp[i - coin][1] + [coin]]

    return dp[amount]

if __name__ == "__main__":
    # Example usage:
    print(change(48, [1, 5, 10, 25, 50]))  # Output: 6
    print(giveChange(48, [1, 5, 10, 25, 50]))  # Output: [6, [25, 10, 10, 1, 1, 1]]
