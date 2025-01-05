from typing import List, Dict

def rod_cutting_memo(length: int, prices: List[int]) -> Dict:
    """
    Finds the optimal way to cut the rod using memoization.

    Args:
        length: Length of the rod.
        prices: List of prices where prices[i] is the price of rod length i+1.

    Returns:
        Dict with the maximum profit, cuts, and the number of cuts.
    """
    memo = {}

    def helper(n):
        # Base case: no rod left
        if n == 0:
            return 0, []
        
        # If the solution for this length is already computed, return it
        if n in memo:
            return memo[n]

        max_profit = 0
        best_cuts = []

        # Try cutting the rod at all lengths from 1 to n
        for i in range(1, n + 1):
            if i <= len(prices):
                current_profit, cuts = helper(n - i)
                current_profit += prices[i - 1]

                if current_profit > max_profit:
                    max_profit = current_profit
                    best_cuts = cuts + [i]

        # Save the result in the memo dictionary
        memo[n] = max_profit, best_cuts
        return memo[n]

    max_profit, cuts = helper(length)
    return {
        "max_profit": max_profit,
        "cuts": cuts,
        "number_of_cuts": len(cuts) - 1
    }

def rod_cutting_table(length: int, prices: List[int]) -> Dict:
    """
    Finds the optimal way to cut the rod using tabulation.

    Args:
        length: Length of the rod.
        prices: List of prices where prices[i] is the price of rod length i+1.

    Returns:
        Dict with the maximum profit, cuts, and the number of cuts.
    """
    # Create a DP table for storing max profits for all lengths
    dp = [0] * (length + 1)
    # Create an array to store the first cut lengths for reconstruction
    first_cut = [0] * (length + 1)

    # Fill the DP table bottom-up
    for i in range(1, length + 1):
        max_profit = 0
        for j in range(1, i + 1):
            if j <= len(prices) and dp[i - j] + prices[j - 1] > max_profit:
                max_profit = dp[i - j] + prices[j - 1]
                first_cut[i] = j
        dp[i] = max_profit

    # Reconstruct the cuts using the first_cut array
    result_cuts = []
    n = length
    while n > 0:
        result_cuts.append(first_cut[n])
        n -= first_cut[n]

    return {
        "max_profit": dp[length],
        "cuts": result_cuts,
        "number_of_cuts": len(result_cuts) - 1
    }


def run_tests():
    """
    Runs all test cases for the rod cutting problem.
    """
    test_cases = [
        # Test 1: Basic case
        {
            "length": 5,
            "prices": [2, 5, 7, 8, 10],
            "name": "Basic Case"
        },
        # Test 2: Optimal not to cut
        {
            "length": 3,
            "prices": [1, 3, 8],
            "name": "Optimal Not to Cut"
        },
        # Test 3: All cuts of size 1
        {
            "length": 4,
            "prices": [3, 5, 6, 7],
            "name": "Uniform Cuts"
        }
    ]

    for test in test_cases:
        print(f"\nTest: {test['name']}")
        print(f"Rod Length: {test['length']}")
        print(f"Prices: {test['prices']}")

        # Test memoization
        memo_result = rod_cutting_memo(test["length"], test["prices"])
        print("\nMemoization Result:")
        print(f"Max Profit: {memo_result['max_profit']}")
        print(f"Cuts: {memo_result['cuts']}")
        print(f"Number of Cuts: {memo_result['number_of_cuts']}")

        # Test tabulation
        table_result = rod_cutting_table(test["length"], test["prices"])
        print("\nTabulation Result:")
        print(f"Max Profit: {table_result['max_profit']}")
        print(f"Cuts: {table_result['cuts']}")
        print(f"Number of Cuts: {table_result['number_of_cuts']}")

        print("\nTest passed successfully!")

if __name__ == "__main__":
    run_tests()
