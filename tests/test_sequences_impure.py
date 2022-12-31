import unittest

from ssg_rummy_server.sequences.impure import (
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
