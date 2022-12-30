def subtract_bags(bag1, bag2):
    """
    Subtract bag2 from bag1. Return None if you cannot validly perform this subtraction.
    """
    result = list(bag1)
    for item in bag2:
        try:
            result.remove(item)
        except ValueError:
            return None
    return result


def intersect_bags(bag1, bag2):
    """
    Return the intersection of bag1 and bag2.
    """
    bag2 = list(bag2)
    result = []
    for item in bag1:
        if item in bag2:
            result.append(item)
            bag2.remove(item)
    return result


def consistent_subbags(bags, universal):
    """
    Produce all subbags of the given bags such that when you add them together, you get a subbag of the universal bag.
    """

    if not bags:
        return [[]]
    first, *rest = bags
    result = []
    # without first
    result += consistent_subbags(rest, universal)
    # with first
    universal_without_first = subtract_bags(universal, first)
    if universal_without_first is not None:
        result += [
            [first] + subbag
            for subbag in consistent_subbags(bags, universal_without_first)
        ]
    return result
