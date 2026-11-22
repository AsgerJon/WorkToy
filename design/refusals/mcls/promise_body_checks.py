"""
RefusedBodyChecks holds the refusals that belong with
'design.promises.mcls.promise_body_checks'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.mcls import BaseObject
from worktoy.waitaminute.meta import QuestionableSyntax, DelException
from worktoy.waitaminute.meta import SlotsRefused, ReservedName


class RefusedBodyChecks(TestCase):
  """
  Each of the following is refused, and the exception named is the one raised
  as of 1.2.3. A mistake Python would let pass in a class body fails at its
  line in a worktoy class: a known misspelling of a dunder, as '__setname__'
  for '__set_name__', raises 'QuestionableSyntax' naming both; '__del__',
  most often meant as '__delete__', raises 'DelException' unless the class is
  declared with 'trustMeBro=True', which each class declaring '__del__'
  repeats; '__slots__', which cannot work since a worktoy instance always
  keeps a '__dict__', raises 'SlotsRefused'; and rebinding a name Python
  reserves for the class, as '__qualname__', raises 'ReservedName'. Source:
  the docstrings of 'NamespaceHook', 'ReservedNames' and these exceptions.
  """

  def test_misspelled_dunder(self) -> None:
    with self.assertRaises(Exception) as refused:
      class Placed(BaseObject):
        def __setname__(self, owner: type, name: str) -> None:
          pass
    self.assertIsInstance(refused.exception, QuestionableSyntax)

  def test_finalizer_1(self) -> None:
    with self.assertRaises(Exception) as refused:
      class Handle(BaseObject):
        def __del__(self) -> None:
          pass
    self.assertIsInstance(refused.exception, DelException)

  def test_finalizer_2(self) -> None:
    class Trusted(BaseObject, trustMeBro=True):
      def __del__(self) -> None:
        pass

    with self.assertRaises(Exception) as refused:
      class Untrusted(Trusted):
        def __del__(self) -> None:
          pass
    self.assertIsInstance(refused.exception, DelException)

  def test_slots(self) -> None:
    with self.assertRaises(Exception) as refused:
      class Packed(BaseObject):
        __slots__ = ('x',)
    self.assertIsInstance(refused.exception, SlotsRefused)

  def test_reserved(self) -> None:
    with self.assertRaises(Exception) as refused:
      class Renamed(BaseObject):
        __qualname__ = 'Other'
    self.assertIsInstance(refused.exception, ReservedName)
