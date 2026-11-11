"""
PromiseBodyChecks promises the checks the namespace of a worktoy class
runs on its body, from 'worktoy.mcls'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.mcls import BaseObject
from worktoy.waitaminute.meta import QuestionableSyntax, DelException
from worktoy.waitaminute.meta import SlotsRefused, ReservedName


class PromiseBodyChecks(TestCase):
  """
  A mistake Python would let pass in a class body fails at its line in a
  worktoy class: a known misspelling of a dunder, as '__setname__' for
  '__set_name__', raises 'QuestionableSyntax' naming both; '__del__',
  most often meant as '__delete__', raises 'DelException' unless the
  class is declared with 'trustMeBro=True', which each class declaring
  '__del__' repeats; '__slots__', which cannot
  work since a worktoy instance always keeps a '__dict__', raises
  'SlotsRefused'; and rebinding a name Python reserves for the class, as
  '__qualname__', raises 'ReservedName'. All are 'SyntaxError's. Source:
  the docstrings of 'NamespaceHook', 'ReservedNames' and these
  exceptions.
  """

  def test_misspelled_dunder(self) -> None:
    with self.assertRaises(QuestionableSyntax) as context:
      class Placed(BaseObject):
        def __setname__(self, owner: type, name: str) -> None:
          pass
    e = context.exception
    self.assertIsInstance(e, SyntaxError)
    self.assertEqual(e.derpName, '__setname__')
    self.assertEqual(e.realName, '__set_name__')

  def test_finalizer(self) -> None:
    with self.assertRaises(DelException) as context:
      class Handle(BaseObject):
        def __del__(self) -> None:
          pass
    self.assertEqual(context.exception.name, 'Handle')

    class Trusted(BaseObject, trustMeBro=True):
      def __del__(self) -> None:
        pass

    self.assertTrue(callable(Trusted.__del__))
    with self.assertRaises(DelException):
      class Untrusted(Trusted):
        def __del__(self) -> None:
          pass

  def test_slots(self) -> None:
    with self.assertRaises(SlotsRefused) as context:
      class Packed(BaseObject):
        __slots__ = ('x',)
    self.assertEqual(context.exception.className, 'Packed')

  def test_reserved(self) -> None:
    with self.assertRaises(ReservedName) as context:
      class Renamed(BaseObject):
        __qualname__ = 'Other'
    self.assertEqual(context.exception.resName, '__qualname__')
