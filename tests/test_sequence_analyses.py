import unittest

from ssg_rummy_server.sequences.analysis import SequenceAnalysis, sequence_analyses

# three pure sequences that do not overlap each other
three_pure = [
    ("A", "H"),
    ("2", "H"),
    ("3", "H"),
    ("5", "H"),
    ("6", "H"),
    ("7", "H"),
    ("9", "H"),
    ("10", "H"),
    ("J", "H"),
]

three_pure_sequences = [
    [("A", "H"), ("2", "H"), ("3", "H")],
    [("5", "H"), ("6", "H"), ("7", "H")],
    [("9", "H"), ("10", "H"), ("J", "H")],
]


class TestSequenceAnalyses(unittest.TestCase):
    def assertAnalysesEqual(self, a, b):
        self.assertEqual(
            sorted(x.canonicalize() for x in a), sorted(x.canonicalize() for x in b)
        )

    def test_single_pure_sequence(self):
        cards = [("A", "H"), ("2", "H"), ("3", "H")]
        self.assertAnalysesEqual(
            sequence_analyses(("J", "S"), cards),
            [
                SequenceAnalysis([], [], [], [("A", "H"), ("2", "H"), ("3", "H")]),
                SequenceAnalysis([[("A", "H"), ("2", "H"), ("3", "H")]], [], [], []),
            ],
        )

    def test_independent_pure_sequences(self):
        cards = [
            ("A", "H"),
            ("2", "H"),
            ("3", "H"),
            ("8", "H"),
            ("9", "H"),
            ("10", "H"),
        ]
        self.assertAnalysesEqual(
            sequence_analyses(("J", "S"), cards),
            [
                SequenceAnalysis([], [], [], cards),
                SequenceAnalysis(
                    [[("A", "H"), ("2", "H"), ("3", "H")]],
                    [],
                    [],
                    [("8", "H"), ("9", "H"), ("10", "H")],
                ),
                SequenceAnalysis(
                    [[("8", "H"), ("9", "H"), ("10", "H")]],
                    [],
                    [],
                    [("A", "H"), ("2", "H"), ("3", "H")],
                ),
                SequenceAnalysis(
                    [
                        [("A", "H"), ("2", "H"), ("3", "H")],
                        [("8", "H"), ("9", "H"), ("10", "H")],
                    ],
                    [],
                    [],
                    [],
                ),
            ],
        )

    def test_impure_sequence(self):
        cards = three_pure + [("A", "S"), ("2", "S"), ("J", "C")]

        self.assertAnalysesEqual(
            [
                x
                for x in sequence_analyses(("J", "S"), cards)
                if x.sufficient_sequences()
            ],
            [
                SequenceAnalysis(
                    three_pure_sequences,
                    [[("A", "S"), ("2", "S"), ()]],
                    [("J", "C")],
                    [],
                ),
                SequenceAnalysis(
                    three_pure_sequences,
                    [],
                    [("J", "C")],
                    [("A", "S"), ("2", "S")],
                ),
            ],
        )

    def test_competing_impure_sequences(self):
        cards = three_pure + [("A", "S"), ("2", "S"), ("A", "C"), ("$", "$")]
        self.assertAnalysesEqual(
            [
                x
                for x in sequence_analyses(("J", "S"), cards)
                if x.sufficient_sequences()
            ],
            [
                SequenceAnalysis(
                    three_pure_sequences,
                    [[("A", "S"), ("2", "S"), ()]],
                    [("$", "$")],
                    [("A", "C")],
                ),
                SequenceAnalysis(
                    three_pure_sequences,
                    [[("A", "C"), ("A", "S"), ()]],
                    [("$", "$")],
                    [("2", "S")],
                ),
                SequenceAnalysis(
                    three_pure_sequences,
                    [],
                    [("$", "$")],
                    [("A", "C"), ("A", "S"), ("2", "S")],
                ),
            ],
        )
