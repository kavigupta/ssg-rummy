import unittest

from ssg_rummy_server.sequences.impure import (
    consistent_impure_sequences,
    extract_impure_sequences,
)


class TestExtractImpureSequences(unittest.TestCase):
    def assertEqualIgnoringOrder(self, a, b):
        self.assertEqual(sorted(a), sorted(b))

    def assertEqualIgnoringOrderAndInternalOrder(self, a, b):
        self.assertEqualIgnoringOrder(
            [sorted(subbag) for subbag in a], [sorted(subbag) for subbag in b]
        )

    def test_basic_subsets(self):
        cards = [("A", "S"), ("2", "S"), ("3", "S")]
        self.assertEqualIgnoringOrderAndInternalOrder(
            extract_impure_sequences(cards),
            [
                [("A", "S"), ("2", "S"), ("3", "S")],
                [("A", "S"), ("2", "S"), ()],
                [("A", "S"), (), ("3", "S")],
                [(), ("2", "S"), ("3", "S")],
                [("A", "S"), (), ()],
                [("2", "S"), (), ()],
                [("3", "S"), (), ()],
            ],
        )

    def test_missed_subsets(self):
        cards = [("A", "S"), ("3", "S")]
        self.assertEqualIgnoringOrderAndInternalOrder(
            extract_impure_sequences(cards),
            [
                [("A", "S"), (), ("3", "S")],
                [("A", "S"), (), ()],
                [("3", "S"), (), ()],
            ],
        )

    def test_alternates(self):
        cards = [("A", "S"), ("2", "S"), ("2", "C")]
        self.assertEqualIgnoringOrderAndInternalOrder(
            extract_impure_sequences(cards),
            [
                [("A", "S"), ("2", "S"), ()],
                [("2", "S"), ("2", "C"), ()],
                [("A", "S"), (), ()],
                [("2", "S"), (), ()],
                [("2", "C"), (), ()],
            ],
        )


class TestConsistentImpureSequences(unittest.TestCase):
    def assertEqualIgnoringOrder(self, a, b):
        self.assertEqual(sorted(a), sorted(b))

    def assertEqualIgnoringOrder2(self, a, b):
        self.assertEqualIgnoringOrder(
            [sorted(subbag) for subbag in a], [sorted(subbag) for subbag in b]
        )

    def assertEqualIgnoringOrder3(self, a, b):
        self.assertEqualIgnoringOrder2(
            [[sorted(subbag) for subbag in subsubbag] for subsubbag in a],
            [[sorted(subbag) for subbag in subsubbag] for subsubbag in b],
        )

    def test_joker_limit(self):
        cards = [("A", "S"), ("2", "S"), ("3", "S")]
        self.assertEqualIgnoringOrder3(
            consistent_impure_sequences(cards, 1),
            [
                [],
                [[("A", "S"), ("2", "S"), ("3", "S")]],
                [[("A", "S"), ("2", "S"), ()]],
                [[("A", "S"), (), ("3", "S")]],
                [[(), ("2", "S"), ("3", "S")]],
            ],
        )
        self.assertEqualIgnoringOrder3(
            consistent_impure_sequences(cards, 2),
            [
                [],
                [[("A", "S"), ("2", "S"), ("3", "S")]],
                [[("A", "S"), ("2", "S"), ()]],
                [[("A", "S"), (), ("3", "S")]],
                [[(), ("2", "S"), ("3", "S")]],
                [[(), (), ("3", "S")]],
                [[(), ("2", "S"), ()]],
                [[("A", "S"), (), ()]],
            ],
        )

    def overlapping_sequences(self):
        cards = [("A", "S"), ("2", "S"), ("2", "C")]
        self.assertEqualIgnoringOrder3(
            consistent_impure_sequences(cards, 1),
            [
                [],
                [[("A", "S"), ("2", "S"), ()]],
                [[("2", "S"), ("2", "C"), ()]],
            ],
        )
        self.assertEqualIgnoringOrder3(
            consistent_impure_sequences(cards, 2),
            [
                [],
                [[("A", "S"), ("2", "S"), ()]],
                [[("2", "S"), ("2", "C"), ()]],
                [[("A", "S"), (), ()]],
                [[("2", "S"), (), ()]],
                [[("2", "C"), (), ()]],
            ],
        )

    def test_independent_sequences(self):
        cards = [("A", "S"), ("2", "S"), ("8", "H"), ("9", "H")]
        self.assertEqualIgnoringOrder3(
            consistent_impure_sequences(cards, 1),
            [
                [],
                [[("A", "S"), ("2", "S"), ()]],
                [[("8", "H"), ("9", "H"), ()]],
            ],
        )
        self.assertEqualIgnoringOrder3(
            consistent_impure_sequences(cards, 2),
            [
                [],
                [[("A", "S"), ("2", "S"), ()]],
                [[("8", "H"), ("9", "H"), ()]],
                [[("A", "S"), ("2", "S"), ()], [("8", "H"), ("9", "H"), ()]],
                [[("A", "S"), (), ()]],
                [[("2", "S"), (), ()]],
                [[("8", "H"), (), ()]],
                [[("9", "H"), (), ()]],
            ],
        )
