"""
TestGenericClassKeywords subclasses 'CoreTest' and pins that a class
deriving from a worktoy metaclass takes class keywords when its only base
with an '__init_subclass__' of its own is 'typing.Generic'. That one
hands every keyword on to 'object.__init_subclass__', which refuses them,
but 'MetaType' counted it as accepting keywords, so
'class Holder(Generic[T], metaclass=BaseMeta, trustMeBro=True)' raised
'TypeError'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import Generic, TypeVar

from worktoy.mcls import BaseMeta

from . import CoreTest

T = TypeVar('T')


class TestGenericClassKeywords(CoreTest):
  """
  TestGenericClassKeywords provides tests for class keywords on a class
  based on 'typing.Generic'.
  """

  def test_generic_takes_keywords(self) -> None:
    """A generic class of a worktoy metaclass takes a class keyword, which
    its namespace reads."""

    class Holder(Generic[T], metaclass=BaseMeta, trustMeBro=True):
      def __del__(self) -> None:
        pass  # pragma: no cover

    self.assertIn('__del__', Holder.__dict__)
    self.assertEqual(Holder.__keyword_arguments__, {'trustMeBro': True})

  def test_own_init_subclass_receives_keywords(self) -> None:
    """A base with an '__init_subclass__' of its own still receives the
    keywords."""
    received = []

    class Tagged(Generic[T], metaclass=BaseMeta):
      def __init_subclass__(cls, **kwargs) -> None:
        received.append(kwargs)

    class Sub(Tagged[int], tag='hello'):
      pass

    self.assertEqual(received, [{'tag': 'hello'}])
