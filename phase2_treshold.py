#!/usr/bin/env python3

import math
import argparse

def is_probability_acceptable(i, n, N, T):
    """
    Checks whether the probability P_D^i(n) is less than the threshold p* = 1 / C(N, 2).
    
    Parameters:
    - i: Number of iterations
    - n: Number of collisions
    - N: Number of devices
    - T: Length of perturbation

    Returns:
    - True if P_D^i(n) < p*, False otherwise.
    """
    if n <= 0 or N < 2 or i < n or T <= 0:
        raise ValueError("Invalid input: Ensure i >= n, n > 0, N >= 2, and T > 0.")

    # Compute product term ∏_{j=0}^{i - n - 1} (1 - j/T)
    product_term = 1.0
    for j in range(i - n):
        product_term *= (1 - j / T)

    P_D_in = (1 / T ** n) * product_term
    p_star = 2 / (N * (N - 1))

    print(f"P_D^{i}({n}) = {P_D_in:.5e}")
    print(f"p* = {p_star:.5e}")
    
    return P_D_in < p_star

def main():
    parser = argparse.ArgumentParser(description="Check whether P_D^i(n) < p* = 1 / C(N, 2)")
    parser.add_argument("i", type=int, help="Number of iterations")
    parser.add_argument("n", type=int, help="Number of collisions")
    parser.add_argument("N", type=int, help="Number of devices")
    parser.add_argument("T", type=int, help="Length of perturbation")

    args = parser.parse_args()

    try:
        result = is_probability_acceptable(args.i, args.n, args.N, args.T)
        print("Result:", result)
    except ValueError as e:
        print("Error:", e)

if __name__ == "__main__":
    main()
