"""This module provides tests for :module:`tools.typechecker` module."""

import unittest

from tools.typechecker import check_types


class TestTypeChecker(unittest.TestCase):
    def test_check_types_decorator(self):
        class C:
            pass

        class D:
            pass

        @check_types
        def f(x1, x2, *args):
            return 42

        c1, c2, d1 = C(), C(), D()
        self.assertEqual(f(c1, c2), 42)
        self.assertEqual(f(c1, c2, d1, 117), 42)
        with self.assertRaises(TypeError):
            f(c1, d1)


if __name__ == "__main__":
    unittest.main()
