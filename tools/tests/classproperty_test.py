"""This module provides tests for :module:`tools.classproperty` module."""

import unittest

from tools.classproperty import classproperty


class TestClassProperty(unittest.TestCase):
    def test_classproperty_decorator(self):
        class C:
            @classproperty
            def f(cls):
                return 42

        c, d = C(), C()
        self.assertEqual(C.f, 42)
        self.assertEqual(c.f, 42)
        self.assertEqual(id(C.f), id(d.f))


if __name__ == "__main__":
    unittest.main()
