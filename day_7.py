from enum import Enum
from functools import cached_property
from typing import List, Tuple

from src import Day


class Card(Enum):
    rank: int

    def __new__(cls, value: str, rank: int):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.rank = rank
        return obj

    def __lt__(self, other: "Card"):
        return self.value < other.value

    def __gt__(self, other: "Card"):
        return self.value > other.value

    def __eq__(self, other: "Card"):
        return self.value == other.value

    def __str__(self) -> str:
        return self.value

    def __hash__(self):
        return hash(self.value)

    ACE = ("A", 12)
    KING = ("K", 11)
    QUEEN = ("Q", 10)
    JACK = ("J", 9)
    TEN = ("T", 8)
    NINE = ("9", 7)
    EIGHT = ("8", 6)
    SEVEN = ("7", 5)
    SIX = ("6", 4)
    FIVE = ("5", 3)
    FOUR = ("4", 2)
    THREE = ("3", 1)
    TWO = ("2", 0)
    JOKER = ("*", -1)


class Rank(Enum):
    def __lt__(self, other):
        return self.value < other.value

    def __gt__(self, other):
        return self.value > other.value

    def __eq__(self, other):
        return self.value == other.value

    HIGH_CARD = 0
    ONE_PAIR = 1
    TWO_PAIR = 2
    THREE_OF_A_KIND = 3
    FULL_HOUSE = 6
    FOUR_OF_A_KIND = 7
    FIVE_OF_A_KIND = 8


class Hand:
    def __init__(self, cards: List[Card]):
        """
        Initialize a Hand object with a list of cards.

        Args:
            cards (List[Cards]): A list of Cards objects
                representing the cards in the hand.
        """
        self.cards = cards

    def __repr__(self) -> str:
        """
        Return a string representation of the hand.

        Returns:
            str: A string representation of the hand.
        """
        return "".join(map(str, self.cards))

    def __lt__(self, other):
        """
        Compare two hands based on their ranks.

        Args:
            other (Hand): The other hand to compare with.

        Returns:
            bool: True if this hand is less than the other hand,
                False otherwise.
        """
        if self.rank == other.rank:
            for card, other_card in zip(self.cards, other.cards):
                if card.rank == other_card.rank:
                    continue
                else:
                    return card.rank < other_card.rank
            return False
        else:
            return self.rank < other.rank

    def _rank(self, cards: List[Card]) -> Rank:
        """
        Determine the rank of a hand based on its cards.

        Args:
            cards (List[Cards]): A list of Cards objects representing
                the cards in the hand.

        Returns:
            HandRank: The rank of the hand.
        """
        cs = set(cards)
        match len(cs):
            case 1:
                return Rank.FIVE_OF_A_KIND
            case 2:
                if any([cards.count(card) == 4 for card in cs]):
                    return Rank.FOUR_OF_A_KIND
                else:
                    return Rank.FULL_HOUSE
            case 3:
                if any([cards.count(card) == 3 for card in cs]):
                    return Rank.THREE_OF_A_KIND
                else:
                    return Rank.TWO_PAIR
            case 4:
                return Rank.ONE_PAIR
            case _:
                return Rank.HIGH_CARD

    @cached_property
    def rank(self) -> Rank:
        """
        Get the rank of the hand.

        Returns:
            HandRank: The rank of the hand.
        """
        return self._rank(self.cards)


class JokerHand(Hand):
    @cached_property
    def rank(self) -> Rank:
        jokers = [card for card in self.cards if card == Card.JOKER]
        nonjokers = [card for card in self.cards if card != Card.JOKER]

        if len(jokers) == 0:
            return self._rank(nonjokers)
        elif len(jokers) == len(self.cards):
            return Rank.FIVE_OF_A_KIND
        else:
            ranks = []
            for card in set(nonjokers):
                cards = nonjokers + [card] * len(jokers)
                ranks.append(self._rank(cards))
            return max(ranks)


class Day7(Day):
    @property
    def data(self) -> List[Tuple[Hand, int]]:
        output = []
        for line in self.raw_data:
            hand, bid = line.split()
            output.append((Hand([Card(card) for card in hand]), int(bid)))

        return output

    def part_1(self) -> int:
        total_winnings = 0
        for i, (_, bid) in enumerate(sorted(self.data)):
            total_winnings += bid * (i + 1)
        return total_winnings

    def part_2(self) -> int:
        new_data = []
        for hand, bid in sorted(self.data):
            new_hand = []
            for card in hand.cards:
                new_hand.append(card if card != Card.JACK else Card.JOKER)
            new_data.append((JokerHand(new_hand), bid))

        total_winnings = 0
        for i, (_, bid) in enumerate(sorted(new_data)):
            total_winnings += bid * (i + 1)

        return total_winnings


if __name__ == "__main__":
    d = Day7("./input/day_7.txt")
    print(d.part_1())
    print(d.part_2())
