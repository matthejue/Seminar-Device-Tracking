#!/usr/bin/env python3

import math
import sys

def is_probability_acceptable(i, n, N, T, verbose=True):
    """
    Checks whether the probability P^N_T(i, n) is less than the threshold p* = 1 / C(N, 2).
    """
    if n < 0 or N < 2 or T <= 0:
        raise ValueError("Invalid input: Ensure n >= 0, N >= 2, and T > 0.")

    if i < n:
        return False

    if n == 0:
        # P^N_T(0) = ∏_{j=0}^{i-1} (1 - j/T)
        product_term = 1.0
        for j in range(i):
            product_term *= (1 - j / T)
        P = product_term
    else:
        product_term = 1.0
        for j in range(i - n):
            product_term *= (1 - j / T)
        P = (1 / T ** n) * product_term

    p_star = 2 / (N * (N - 1))

    if verbose:
        print(f"P^N_T({i}, {n}) = {P:.5e}")
        print(f"p*           = {p_star:.5e}")
        print(f"P^N_T({i}, {n}) < p* ? → {P < p_star}\n")

    return P < p_star

def find_minimum_n(i, N, T, n_max=100, verbose=False):
    """
    Finds the smallest n* such that is_probability_acceptable(i, n, N, T) returns True.
    """
    for n in range(0, n_max + 1):  # Now starts from 0
        try:
            if is_probability_acceptable(i, n, N, T, verbose=verbose):
                return n
        except ValueError:
            continue
    return None

def generate_n_star_table(N, T, i_start=1, i_max=300, n_max=100):
    """
    Generates a table of i-ranges where the minimum n* value is constant.
    Stops when n* = 0 or i reaches i_max.
    """
    found_first = False
    i = i_start
    current_n_star = None
    range_start = None

    print(f"{'i-range':<15} | {'n*[i]':>6}")
    print("-" * 25)

    while i <= i_max:
        n_star = find_minimum_n(i, N, T, n_max=n_max, verbose=False)

        if n_star is None:
            i += 1
            continue

        if not found_first:
            current_n_star = n_star
            range_start = i
            found_first = True

        elif n_star != current_n_star:
            print(f"{str(range_start) + '–' + str(i - 1):<15} | {current_n_star:>6}")
            range_start = i
            current_n_star = n_star

        if n_star == 0:
            print(f"{i:<15} | {0:>6}")
            break

        i += 1

    if found_first and current_n_star != 0 and i > range_start:
        print(f"{str(range_start) + '–' + str(i - 1):<15} | {current_n_star:>6}")

    print("-" * 25)

def main():
    args = sys.argv[1:]

    if len(args) == 4:
        # Single test mode: i n N T
        i, n, N, T = map(int, args)

        print("\n--- Parameter Assignment ---")
        print(f"i  (iterations)         = {i}")
        print(f"n  (collisions)         = {n}")
        print(f"N  (number of devices)  = {N}")
        print(f"T  (perturbation length)= {T}")
        print("-----------------------------\n")

        try:
            is_probability_acceptable(i, n, N, T, verbose=True)
        except ValueError as e:
            print("Error:", e)

    elif len(args) == 2:
        # Table generation mode: N T
        N, T = map(int, args)

        print("\n--- Parameter Assignment ---")
        print(f"N  (number of devices)  = {N}")
        print(f"T  (perturbation length)= {T}")
        print("-----------------------------")

        generate_n_star_table(N, T)

    else:
        print("Usage:")
        print("  ./phase2_treshold.py i n N T       → check if P^N_T(i, n) < p*")
        print("  ./phase2_treshold.py N T           → generate n* table")

if __name__ == "__main__":
    main()
