import unittest

from ssg_rummy_server.sequences.pure import (
    consistent_pure_sequences,
    consistent_pure_sequences_single_suite,
    extract_pure_sequences_single_suite,
)


class TestConsistentPureSequencesSingleSuit(unittest.TestCase):
    def assertEqualIgnoringOrder(self, a, b):
        self.assertEqual(sorted(a), sorted(b))

    def assertEqualIgnoringOrderAndInternalOrder(self, a, b):
        self.assertEqualIgnoringOrder(
            [sorted(subbag) for subbag in a], [sorted(subbag) for subbag in b]
        )

    def test_independent(self):
        numbers = ["A", "2", "3", "4", "8", "9", "10"]
        self.assertEqualIgnoringOrderAndInternalOrder(
            consistent_pure_sequences_single_suite(numbers),
            [
                [],
                [["A", "2", "3"]],
                [["2", "3", "4"]],
                [["A", "2", "3", "4"]],
                [["8", "9", "10"]],
                [["A", "2", "3"], ["8", "9", "10"]],
                [["2", "3", "4"], ["8", "9", "10"]],
                [["A", "2", "3", "4"], ["8", "9", "10"]],
            ],
        )

    def test_duplicate_cards(self):
        numbers = ["A", "A", "2", "2", "3", "3"]
        self.assertEqualIgnoringOrderAndInternalOrder(
            consistent_pure_sequences_single_suite(numbers),
            [
                [],
                [["A", "2", "3"]],
                [["A", "2", "3"], ["A", "2", "3"]],
            ],
        )


class TestExtractPureSequencesSingleSuit(unittest.TestCase):
    def assertEqualIgnoringOrder(self, a, b):
        self.assertEqual(sorted(a), sorted(b))

    def test_independent(self):
        numbers = ["A", "2", "3", "4", "8", "9", "10"]
        self.assertEqualIgnoringOrder(
            extract_pure_sequences_single_suite(numbers),
            [
                ["A", "2", "3"],
                ["2", "3", "4"],
                ["A", "2", "3", "4"],
                ["8", "9", "10"],
            ],
        )


class TestExtractPureSequences(unittest.TestCase):
    def assertEqualIgnoringOrder(self, a, b):
        self.assertEqual(sorted(a), sorted(b))

    def assertEqualIgnoringOrderAndInternalOrder(self, a, b):
        self.assertEqualIgnoringOrder(
            [sorted(subbag) for subbag in a], [sorted(subbag) for subbag in b]
        )

    def test_single_suite(self):
        cards = [("A", "S"), ("2", "S"), ("3", "S"), ("4", "S")]
        self.assertEqualIgnoringOrderAndInternalOrder(
            consistent_pure_sequences(cards),
            [
                [],
                [[("A", "S"), ("2", "S"), ("3", "S")]],
                [[("A", "S"), ("2", "S"), ("3", "S"), ("4", "S")]],
                [[("2", "S"), ("3", "S"), ("4", "S")]],
            ],
        )

    def test_multiple_suites(self):
        cards = [("A", "S"), ("2", "S"), ("3", "S"), ("4", "H"), ("5", "H"), ("6", "H")]
        self.assertEqualIgnoringOrderAndInternalOrder(
            consistent_pure_sequences(cards),
            [
                [],
                [[("A", "S"), ("2", "S"), ("3", "S")]],
                [[("4", "H"), ("5", "H"), ("6", "H")]],
                [
                    [("A", "S"), ("2", "S"), ("3", "S")],
                    [("4", "H"), ("5", "H"), ("6", "H")],
                ],
            ],
        )
