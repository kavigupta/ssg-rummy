import random

numbers = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
suites = "SCHD"


def card_deck():
    return [(number, suite) for number in numbers for suite in suites] + [
        ("$", "$")
    ] * 2


def shuffled_deck(num_decks):
    whole_deck = [x for x in card_deck() for _ in range(num_decks)]
    assert len(whole_deck) == num_decks * 54, str((len(whole_deck)))
    random.shuffle(whole_deck)
    return whole_deck
