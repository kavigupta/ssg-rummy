from ..deck import numbers


def number_sequences():
    """
    Generate all possible sequences of numbers.
    """
    for len_seq in 3, 4, 5:
        for starting in range(len(numbers) - len_seq):
            yield numbers[starting : starting + len_seq]


def card_sequences():
    """
    Produce all possible sequences of cards, up to 5 cards.
    """
    for sequence in number_sequences():
        for suite in "SCHD":
            yield [(number, suite) for number in sequence]


def card_multi_suite_sequences():
    """
    Produce all multi-suite sequences, e.g., [('A', 'S'), ('A', 'C'), ('A', 'H'), ('A', 'D')].
        Can be 3 or 4 cards long.
    """
    for number in numbers:
        for suites in "SCHD", "SCH", "SCD", "SHD", "CHD":
            yield [(number, suite) for suite in suites]
