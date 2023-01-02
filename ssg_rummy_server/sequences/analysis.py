import attr
from ssg_rummy_server.bag_utils import subtract_bags
from ssg_rummy_server.jokers import separate_jokers
from ssg_rummy_server.sequences.impure import consistent_impure_sequences

from ssg_rummy_server.sequences.pure import consistent_pure_sequences

MIN_NUM_PURE_SEQUENCES = 3


@attr.s
class SequenceAnalysis:
    pure_sequences = attr.ib()
    impure_sequences = attr.ib()
    jokers = attr.ib()
    other = attr.ib()

    def canonicalize(self):
        return SequenceAnalysis(
            sorted(sorted(seq) for seq in self.pure_sequences),
            sorted(sorted(seq) for seq in self.impure_sequences),
            sorted(self.jokers),
            sorted(self.other),
        )

    def sufficient_sequences(self):
        return len(self.pure_sequences) >= MIN_NUM_PURE_SEQUENCES

def sequence_analyses(joker, cards):
    """
    Sequence analyses for a list of cards. Returns a list of SequenceAnalysis objects.
    """
    pure_sequence_sets = consistent_pure_sequences(cards)
    for pure_sequences in pure_sequence_sets:
        remaining_cards = subtract_bags(cards, [x for xs in pure_sequences for x in xs])
        assert remaining_cards is not None
        jokers, remaining_cards = separate_jokers(joker, remaining_cards)
        if len(pure_sequences) < MIN_NUM_PURE_SEQUENCES:
            yield SequenceAnalysis(pure_sequences, [], jokers, remaining_cards)
        else:
            for impure_sequences in consistent_impure_sequences(
                remaining_cards, len(jokers)
            ):
                other = subtract_bags(
                    remaining_cards, [x for xs in impure_sequences for x in xs if x != ()]
                )
                assert other is not None
                yield SequenceAnalysis(pure_sequences, impure_sequences, jokers, other)
