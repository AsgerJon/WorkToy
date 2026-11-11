"""
PromiseComplex promises 'ComplexMixin' and the test bank 'ComplexTest'
from 'worktoy.work_test'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

import unittest
from unittest import TestCase

from worktoy.work_test import BaseTest, ComplexMixin, ComplexTest


class PromiseComplex(TestCase):
  """
  'ComplexMixin' gives a class the arithmetic of 'complex' from its two
  parts 'REAL' and 'IMAG', built from nothing, one number, a 'complex',
  a string 'complex' parses, or two parts: the operators with
  instances, numbers and 'complex', 'abs', 'conjugate', equality and
  hash as 'complex' has them, and iteration over the two parts.
  'ComplexTest' is a bank of tests for that arithmetic: a test class
  lists it before 'BaseTest', or any other test case, with its
  implementations in 'targets', and every test runs against
  each; a class without targets skips every test, and a class listing
  the bank without a test case raises 'TypeError'. Source: the
  docstrings of 'ComplexMixin' and 'ComplexTest'.
  """

  def test_arithmetic(self) -> None:
    class Simple(ComplexMixin):
      pass

    z = Simple(1, 2)
    self.assertEqual(complex(z + Simple(3, 4)), 4 + 6j)
    self.assertEqual(complex(z * 2), 2 + 4j)
    self.assertEqual(complex(z.conjugate()), 1 - 2j)
    self.assertEqual(z, 1 + 2j)
    self.assertEqual(hash(z), hash(1 + 2j))
    self.assertEqual(abs(Simple(3, 4)), 5.0)
    self.assertEqual(list(z), [1.0, 2.0])
    for made in (Simple(1 + 2j), Simple('1+2j'), Simple(1, 2)):
      with self.subTest(made=made):
        self.assertEqual(complex(made), 1 + 2j)
    self.assertEqual(complex(Simple()), 0j)

  def test_bank_with_any_test_case(self) -> None:
    class Simple(ComplexMixin):
      pass

    class TestPlain(ComplexTest, unittest.TestCase):
      targets = (Simple,)

    result = unittest.TestResult()
    unittest.TestLoader().loadTestsFromTestCase(TestPlain).run(result)
    self.assertTrue(result.wasSuccessful())

  def test_bank(self) -> None:
    class Simple(ComplexMixin):
      pass

    class TestSimple(ComplexTest, BaseTest):
      targets = (Simple,)

    class TestNothing(ComplexTest, BaseTest):
      pass

    result = unittest.TestResult()
    unittest.TestLoader().loadTestsFromTestCase(TestSimple).run(result)
    self.assertTrue(result.wasSuccessful())
    self.assertGreater(result.testsRun, 0)
    self.assertEqual(len(result.skipped), 0)
    result = unittest.TestResult()
    unittest.TestLoader().loadTestsFromTestCase(TestNothing).run(result)
    self.assertEqual(len(result.skipped), result.testsRun)

  def test_bank_needs_a_test_case(self) -> None:
    class Simple(ComplexMixin):
      pass

    with self.assertRaises(TypeError):
      class TestBare(ComplexTest):
        targets = (Simple,)
