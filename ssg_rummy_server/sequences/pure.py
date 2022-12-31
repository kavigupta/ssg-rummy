from collections import defaultdict
import itertools
from ..bag_utils import consistent_subbags
from .utils import number_sequences


def consistent_pure_sequences(cards):
    by_suite = defaultdict(list)
    for number, suite in cards:
        by_suite[suite].append((number, suite))
    return [
        [x for xs in xss for x in xs]
        for xss in itertools.product(
            *[
                consistent_pure_sequences_single_suite_on_cards(cards)
                for cards in by_suite.values()
            ]
        )
    ]


def consistent_pure_sequences_single_suite_on_cards(cards):
    numbers, suites = zip(*cards)
    [suite] = set(suites)
    return [
        [[(number, suite) for number in sequence] for sequence in sequences]
        for sequences in consistent_pure_sequences_single_suite(numbers)
    ]


def consistent_pure_sequences_single_suite(numbers_to_extract):
    """
    Extracts all possible sets of consistent pure sequences from a list of card numbers.

    E.g., ["A", "2", "3", "4", "8", "9", "10"] gives the following outputs
        []
        [["A", "2", "3"]]
        [["2", "3", "4"]]
        [["A", "2", "3", "4"]]
        [["8", "9", "10"]]
        [["A", "2", "3"], ["8", "9", "10"]]
        [["2", "3", "4"], ["8", "9", "10"]]
        [["A", "2", "3", "4"], ["8", "9", "10"]]
    """

    sequences = extract_pure_sequences_single_suite(numbers_to_extract)
    return consistent_subbags(sequences, numbers_to_extract)


def extract_pure_sequences_single_suite(numbers_to_extract):
    """
    Extracts all possible sets of pure sequences from a list of card numbers.

    Only up to 5 cards, as 6 card sequences can be represented as 3 card sequences.

    E.g., ["A", "2", "3", "4", "8", "9", "10"] gives the following outputs
        ["A", "2", "3"]
        ["2", "3", "4"]
        ["A", "2", "3", "4"]
        ["8", "9", "10"]
    """
    # get the pure sequences
    pure_sequences = []
    # triplis
    for card in set(numbers_to_extract):
        if numbers_to_extract.count(card) >= 3:
            pure_sequences.append([card] * 3)
    # sequences of length len_seq
    for sequence in number_sequences():
        if set(sequence) - set(numbers_to_extract) == set():
            pure_sequences.append(sequence)
    return pure_sequences
