"""
TestResolveMRO tests 'resolveMRO' from 'worktoy.utilities'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

import sys

from worktoy.utilities import resolveMRO
from worktoy.waitaminute import RedundantKeyword
from . import UtilitiesTest

HERE = sys._getframe().f_code.co_filename


class TestResolveMRO(UtilitiesTest):
  """
  'resolveMRO' computes the resolution order a class with the given
  bases would have, without creating the class, so a metaclass can
  reason about the bases before building. The tests pin that the result
  agrees with the order Python gives a class of those bases, the two
  trivial inputs, the refusal of bases that admit no order, the bailout
  of the merge loop, and the warning given for a keyword that is no
  option.
  """

  @staticmethod
  def _diamond() -> tuple:
    """A, B(A), C(A) built without touching the module namespace."""
    A = type('A', (), {})
    B = type('B', (A,), {})
    C = type('C', (A,), {})
    return A, B, C

  def test_no_bases(self) -> None:
    self.assertEqual(resolveMRO(), [])

  def test_one_base(self) -> None:
    A, B, C = self._diamond()
    self.assertEqual(resolveMRO(B), [B, A, object])
    self.assertEqual(resolveMRO(object), [object])

  def test_docstring_example(self) -> None:
    A, B, C = self._diamond()
    self.assertEqual(resolveMRO(B, C), [B, C, A, object])

  def test_agrees_with_python(self) -> None:
    A, B, C = self._diamond()
    D = type('D', (B, C), {})
    E = type('E', (C,), {})
    cases = ((B, C), (C, B), (D, E), (E, B), (D, A), (B, C, A))
    for bases in cases:
      Foo = type('Foo', bases, {})
      with self.subTest(bases=[b.__name__ for b in bases]):
        self.assertEqual(resolveMRO(*bases), Foo.mro()[1:])

  def test_inconsistent_bases_refused(self) -> None:
    A, B, C = self._diamond()
    X = type('X', (B, C), {})
    Y = type('Y', (C, B), {})
    with self.assertRaises(TypeError) as context:
      resolveMRO(X, Y)
    self.assertIn('(X and Y)', str(context.exception))
    self.assertIn('consistent', str(context.exception))
    with self.assertRaises(TypeError):
      type('Z', (X, Y), {})

  def test_base_order_pinned(self) -> None:
    #  Two unrelated bases keep the order of the class statement.
    A, B, C = self._diamond()
    P = type('P', (), {})
    self.assertEqual(resolveMRO(P, A), [P, A, object])
    self.assertEqual(resolveMRO(A, P), [A, P, object])

  def test_iteration_guard(self) -> None:
    A, B, C = self._diamond()
    total = len(B.__mro__) + len(C.__mro__) + 2
    with self.assertRaises(RecursionError) as context:
      resolveMRO(B, C, _initialIterationCount=total)
    self.assertEqual(context.exception.args, ())
    self.assertEqual(
        resolveMRO(B, C, _initialIterationCount=total - 4),
        [B, C, A, object],
    )

  def test_unknown_keyword_warned(self) -> None:
    A, B, C = self._diamond()
    expected = """'worktoy.utilities.resolveMRO' received the keyword
    'strict', which it does not read, and went on without it! It reads:
    '_initialIterationCount'."""
    for bases in ((), (A,), (B, C)):
      with self.subTest(bases=len(bases)):
        with self.assertWarns(RedundantKeyword) as context:
          line = sys._getframe().f_lineno + 1
          order = resolveMRO(*bases, strict=True)
        self.assertEqual(order, resolveMRO(*bases))
        warning = context.warning
        self.assertIs(warning.receiver, resolveMRO)
        self.assertEqual(warning.keyword, 'strict')
        self.assertEqual(warning.options, ('_initialIterationCount',))
        self.assertEqual(str(warning), str.join(' ', expected.split()))
        self.assertEqual(context.filename, HERE)
        self.assertEqual(context.lineno, line)
