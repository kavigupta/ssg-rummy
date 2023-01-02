from .deck import to_number


def is_joker(joker, card):
    # number joker
    if joker[0] == card[0]:
        return True
    # paplu joker
    if joker[1] == card[1] and (to_number(joker[0]) - to_number(card[0])) % 13 in {
        0,
        1,
        12,
    }:
        return True
    # $ joker
    if list(card) == ["$", "$"]:
        return True
    return False


def separate_jokers(joker, cards):
    """
    Returns (jokers, other_cards)
    """
    jokers = [card for card in cards if is_joker(joker, card)]
    other_cards = [card for card in cards if not is_joker(joker, card)]
    return jokers, other_cards
