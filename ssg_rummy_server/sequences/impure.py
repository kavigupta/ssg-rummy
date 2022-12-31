from collections import defaultdict
import itertools

from ..bag_utils import intersect_bags
from .utils import card_sequences, card_multi_suite_sequences


def extract_impure_sequences(cards):
    """
    Extract all impure sequences from a list of cards, placing a wildcard `()` rather than using a joker
        for each.
    """
    # maps each impure sequence to the number of wildcards it contains, a list for now of all possibilities for code
    # legibility
    impure_sequences = defaultdict(list)
    # single cards paired with wildcards
    for card in set(cards):
        impure_sequences[(card,)] += [2]
    # sequence with some wildcards
    for sequence in [*card_sequences(), *card_multi_suite_sequences()]:
        sequence_with_our_cards = intersect_bags(sequence, cards)
        if len(sequence_with_our_cards) < 2:
            continue
        for r in range(2, len(sequence_with_our_cards) + 1):
            for subset in itertools.combinations(sequence_with_our_cards, r):
                impure_sequences[subset] += [len(sequence) - len(subset)]

    impure_sequences = [tuple(x) + ((),) * min(y) for x, y in impure_sequences.items()]

    return impure_sequences
