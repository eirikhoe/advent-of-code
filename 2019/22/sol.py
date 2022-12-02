from pathlib import Path
import numpy as np
import copy
import re

data_folder = Path(__file__).parent.resolve()
import math


def primeFactors(n):

    # Print the number of two's that divide n
    while n % 2 == 0:
        print(2)
        n = n / 2

    # n must be odd at this point
    # so a skip of 2 ( i = i + 2) can be used
    for i in range(3, int(math.sqrt(n)) + 1, 2):

        # while i divides n , print i ad divide n
        while n % i == 0:
            print(i)
            n = n / i

    # Condition if n is a prime
    # number greater than 2
    if n > 2:
        print(n)


class Deck:
    """A Card class"""

    re_increment = re.compile(r"deal with increment (\d+)")
    re_new_stack = re.compile(r"deal into new stack")
    re_cut = re.compile(r"cut (-?\d+)")

    def __init__(self, n, file):
        # self.cards = np.arange(n)
        self.n_cards = n
        self.instructions = file.read_text().split("\n")
        self.complete_shuffle = [1, 0]
        self.get_shuffle()

    def deal_into_new_stack(self):
        self.complete_shuffle = [
            (-self.complete_shuffle[0]) % self.n_cards,
            (-1 - self.complete_shuffle[1]) % self.n_cards,
        ]

    def cut(self, n):
        self.complete_shuffle = [
            self.complete_shuffle[0] % self.n_cards,
            (self.complete_shuffle[1] - n) % self.n_cards,
        ]

    def deal_with_increment(self, n):
        self.complete_shuffle = [
            (n * self.complete_shuffle[0]) % self.n_cards,
            (n * self.complete_shuffle[1]) % self.n_cards,
        ]

    def get_shuffle(self):
        for instruction in self.instructions:
            if Deck.re_new_stack.match(instruction):
                self.deal_into_new_stack()
            elif Deck.re_cut.match(instruction):
                self.cut(int(Deck.re_cut.match(instruction).groups()[0]))
            elif Deck.re_increment.match(instruction):
                self.deal_with_increment(
                    int(Deck.re_increment.match(instruction).groups()[0])
                )

    def shuffle_and_get_card(self, n_shuffles, x, return_value=True):
        total_shuffle = [0, 0]
        total_shuffle[0] = pow(self.complete_shuffle[0], n_shuffles, self.n_cards)
        total_shuffle[1] = (
            self.complete_shuffle[1]
            * pow(self.complete_shuffle[0] - 1, self.n_cards - 2, self.n_cards)
        ) % self.n_cards
        total_shuffle[1] = (total_shuffle[1] * (total_shuffle[0] - 1)) % self.n_cards
        if return_value:
            return (
                ((x - total_shuffle[1]) % self.n_cards)
                * pow(total_shuffle[0], self.n_cards - 2, self.n_cards)
            ) % self.n_cards
        else:
            return (total_shuffle[0] * x + total_shuffle[1]) % self.n_cards

    def get_card(self, value):
        indices = np.arange(self.n_cards)
        return indices[self.cards == value][0]


def main():
    file = data_folder / "input.txt"
    deck = Deck(10007, file)
    n_shuffles = 1
    x = 2019
    print("Part 1")
    print(f"{deck.n_cards} cards in the deck and {n_shuffles} complete shuffle(s).")
    print(
        f"The position of card {x} is {deck.shuffle_and_get_card(n_shuffles,x,False)}."
    )
    print()
    deck = Deck(119315717514047, file)
    n_shuffles = 101741582076661
    x = 2020
    print("Part 2")
    print(f"{deck.n_cards} cards in the deck and {n_shuffles} complete shuffle(s).")
    print(f"The value of card {x} is {deck.shuffle_and_get_card(n_shuffles,x,True)}.")


if __name__ == "__main__":
    main()

