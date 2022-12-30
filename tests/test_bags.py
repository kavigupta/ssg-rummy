import unittest

from ssg_rummy_server.bag_utils import consistent_subbags


class TestConsistentSubbags(unittest.TestCase):
    def assertEqualIgnoringOrder(self, a, b):
        self.assertEqual(sorted(a), sorted(b))

    def test_independent(self):
        universal = "ABCDEF"
        bags = ["ABC", "DEF"]
        self.assertEqualIgnoringOrder(
            consistent_subbags(bags, universal), [[], ["ABC"], ["DEF"], ["ABC", "DEF"]]
        )

    def test_dependent(self):
        universal = "ABCDEF"
        bags = ["ABC", "BCD"]
        self.assertEqualIgnoringOrder(
            consistent_subbags(bags, universal), [[], ["ABC"], ["BCD"]]
        )

    def test_dependent_with_duplicate(self):
        universal = "ABCCDE"
        bags = ["ABC", "CDE"]
        self.assertEqualIgnoringOrder(
            consistent_subbags(bags, universal), [[], ["ABC"], ["CDE"], ["ABC", "CDE"]]
        )

    def test_dependent_with_duplicate_and_extra(self):
        universal = "ABCCDE"
        bags = ["ABC", "CDE", "E"]
        self.assertEqualIgnoringOrder(
            consistent_subbags(bags, universal),
            [[], ["ABC"], ["E"], ["ABC", "E"], ["CDE"], ["ABC", "CDE"]],
        )

    def test_multi_subbags(self):
        universal = "ABCABCABCABC"
        bags = ["ABC"]
        self.assertEqualIgnoringOrder(
            consistent_subbags(bags, universal),
            [
                [],
                ["ABC"],
                ["ABC", "ABC"],
                ["ABC", "ABC", "ABC"],
                ["ABC", "ABC", "ABC", "ABC"],
            ],
        )
        bags = ["ABCABC"]
        self.assertEqualIgnoringOrder(
            consistent_subbags(bags, universal),
            [
                [],
                ["ABCABC"],
                ["ABCABC", "ABCABC"],
            ],
        )
