"""
TestCastRule subclasses 'UtilitiesTest' and pins 'castRule', which names
the builtin whose rule 'typeCast' holds a target to. That is the target
itself for a builtin with a rule, the builtin a subclass is based on when
the subclass leaves its constructor as it is, and 'None' for a subclass
with a constructor of its own and for every other class, whose
constructor 'typeCast' trusts. 'AttriBox' asks it too, so the boxes and
the overload dispatch decide the same way.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from collections import Counter, OrderedDict
from enum import IntEnum
from pathlib import Path

from worktoy.utilities import castRule

from . import UtilitiesTest


class TestCastRule(UtilitiesTest):
  """
  TestCastRule provides tests for 'castRule'.
  """

  def test_builtins_with_a_rule(self) -> None:
    """Each builtin with a rule is its own rule."""
    builtins = (str, bytes, bytearray, bool, int, float, complex, dict,
                list, tuple, set, frozenset)
    for builtin in builtins:
      with self.subTest(target=builtin.__name__):
        self.assertIs(castRule(builtin), builtin)

  def test_plain_subclass(self) -> None:
    """A subclass leaving the constructor as it is, directly or further
    down, is held to the rule of its builtin."""

    class MyStr(str):
      pass

    class MyMyStr(MyStr):
      pass

    class MyInt(int):
      pass

    self.assertIs(castRule(MyStr), str)
    self.assertIs(castRule(MyMyStr), str)
    self.assertIs(castRule(MyInt), int)

  def test_own_constructor(self) -> None:
    """A subclass with a '__new__' or an '__init__' of its own, inherited
    or from a mixin after the builtin, has no rule."""

    #  The constructors are never called, only found, and a lambda that
    #  never runs leaves no line uncovered.
    class OwnNew(str):
      __new__ = lambda cls, value: str.__new__(cls, value)

    class Inherits(OwnNew):
      pass

    class OwnInit(list):
      __init__ = lambda self, *args: list.__init__(self, *args)

    class Tagged:
      __init__ = lambda self, *args: None

    class TaggedStr(str, Tagged):
      pass

    class Level(IntEnum):
      LOW = 1

    for target in (OwnNew, Inherits, OwnInit, TaggedStr, Level, Counter,
                   OrderedDict):
      with self.subTest(target=target.__name__):
        self.assertIsNone(castRule(target))

  def test_other_classes(self) -> None:
    """A class based on no builtin with a rule has none, nor has
    'object'."""
    for target in (Path, object, type):
      with self.subTest(target=target.__name__):
        self.assertIsNone(castRule(target))
