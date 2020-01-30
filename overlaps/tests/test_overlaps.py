import unittest

from overlaps.overlaps.overlap import has_overlaps


class TestOverlap(unittest.TestCase):
    def test_error_not_a_tuple(self):
        with self.assertRaises(ValueError):
            has_overlaps('test', (1, 2))

    def test_error_none_input(self):
        with self.assertRaises(ValueError):
            has_overlaps(None, 'test')

    def test_error_not_integer_in_a_tuple(self):
        with self.assertRaises(TypeError):
            has_overlaps(('1', 2), (1, 2))

    def test_no_overlap_ordered_positive_lines(self):
        self.assertFalse(has_overlaps((1, 5), (6, 8)))

    def test_no_overlap_unordered_positive_lines(self):
        self.assertFalse(has_overlaps((6, 8), (1, 5)))

    def test_no_overlap_ordered_negative_lines(self):
        self.assertFalse(has_overlaps((-5, -8), (-4, -1)))

    def test_no_overlap_unordered_negative_lines(self):
        self.assertFalse(has_overlaps((-4, -1), (-5, -8)))

    def test_no_overlap_ordered_mixed_lines(self):
        self.assertFalse(has_overlaps((-6, -2), (-1, 4)))

    def test_no_overlap_unordered_mixed_lines(self):
        self.assertTrue(has_overlaps((-1, -4), (-6, -2)))

    def test_overlap_ordered_positive_lines(self):
        self.assertTrue(has_overlaps((1, 3), (2, 8)))

    def test_overlap_unordered_positive_lines(self):
        self.assertTrue(has_overlaps((2, 8), (1, 3)))

    def test_overlap_ordered_negative_lines(self):
        self.assertTrue(has_overlaps((-4, -1), (-3, -8)))

    def test_overlap_unordered_negative_lines(self):
        self.assertTrue(has_overlaps((-3, -8), (-4, -1)))

    def test_overlap_positive_ordered_lines_edge_case(self):
        self.assertTrue(has_overlaps((1, 4), (4, 8)))

    def test_overlap_positive_unordered_lines_edge_case(self):
        self.assertTrue(has_overlaps((4, 8), (1, 4)))

    def test_overlap_negative_ordered_lines_edge_case(self):
        self.assertTrue(has_overlaps((-4, -1), (-2, 2)))

    def test_overlap_negative_unordered_lines_edge_case(self):
        self.assertTrue(has_overlaps((-2, 2), (-4, -1)))

    def test_overlap_ordered_mixed_lines(self):
        self.assertTrue(has_overlaps((-4, -1), (-2, 2)))

    def test_overlap_unordered_mixed_lines(self):
        self.assertTrue(has_overlaps((-2, 2), (-4, -1)))

    def test_overlap_special_case(self):
        self.assertTrue(has_overlaps((0, 0), (0, 0)))


if __name__ == "__main__":
    unittest.main()
