"""
TestTypeCastSubclass subclasses 'UtilitiesTest' and pins how 'typeCast'
casts to a subclass of a builtin it has a rule for, such as a subclass of
'int', 'str' or 'list'. A subclass that keeps the constructor of its
builtin is that builtin under another name: the value is held to the
rule of that builtin, and the result is then built as an instance of
the subclass, so the cast is as lossless as one to the builtin and keeps
the type asked for. A subclass with a constructor of its own, a '__new__'
or an '__init__' other than that of its builtin, as an 'IntEnum' or
'collections.Counter' has, states its own conversion and is trusted: its
constructor receives the value as given.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from collections import Counter
from enum import IntEnum
from typing import TYPE_CHECKING

from worktoy.utilities import typeCast
from worktoy.waitaminute.dispatch import TypeCastException

from . import UtilitiesTest

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any


class TestTypeCastSubclass(UtilitiesTest):
  """
  TestTypeCastSubclass provides tests for 'typeCast' to subclasses of the
  builtins it has rules for.
  """

  @staticmethod
  def _subclasses() -> tuple:
    """The '_subclasses' method builds one subclass of each builtin the
    tests cast to: 'int', 'float', 'str', 'bytes', 'list' and 'dict'."""

    class MyInt(int):
      pass

    class MyFloat(float):
      pass

    class MyStr(str):
      pass

    class MyBytes(bytes):
      pass

    class MyList(list):
      pass

    class MyDict(dict):
      pass

    return MyInt, MyFloat, MyStr, MyBytes, MyList, MyDict

  def test_lossy_values_refused(self) -> None:
    """A value the rule of the builtin refuses is refused for the
    subclass, naming the subclass."""
    MyInt, _, MyStr, MyBytes, MyList, MyDict = self._subclasses()
    cases = (
      (MyInt, 2.5),
      (MyStr, None),
      (MyStr, 5),
      (MyBytes, 3),
      (MyList, 'abc'),
      (MyDict, [('a', 1)]),
    )
    for target, value in cases:
      with self.subTest(target=target.__name__, value=repr(value)):
        with self.assertRaises(TypeCastException) as context:
          typeCast(target, value)
        self.assertIs(context.exception.type_, target)

  def test_cast_keeps_the_subclass(self) -> None:
    """A value the rule accepts is cast, and the result is an instance of
    the subclass."""
    MyInt, MyFloat, MyStr, MyBytes, MyList, MyDict = self._subclasses()
    cases = (
      (MyInt, 2.0, 2),
      (MyInt, '3', 3),
      (MyFloat, 2, 2.0),
      (MyStr, b'abc', 'abc'),
      (MyBytes, 'abc', b'abc'),
      (MyList, (1, 2), [1, 2]),
      (MyDict, {'a': 1}, {'a': 1}),
    )
    for target, value, expected in cases:
      with self.subTest(target=target.__name__, value=repr(value)):
        cast = typeCast(target, value)
        self.assertIs(type(cast), target)
        self.assertEqual(cast, expected)

  def test_value_of_the_builtin_becomes_the_subclass(self) -> None:
    """A value already of the builtin, but not of the subclass, is built
    into the subclass rather than returned as it is."""
    MyInt, _, MyStr, *__ = self._subclasses()
    cast = typeCast(MyStr, 'Never gonna give you up')
    self.assertIs(type(cast), MyStr)
    self.assertEqual(cast, 'Never gonna give you up')
    cast = typeCast(MyInt, True)
    self.assertIs(type(cast), MyInt)
    self.assertEqual(cast, 1)

  def test_built_without_instantiation_fallback(self) -> None:
    """Building the subclass belongs to the cast, so it happens with
    'allowInstantiation=False' as well, while the rule still refuses."""
    MyInt, *_ = self._subclasses()
    cast = typeCast(MyInt, 2.0, allowInstantiation=False)
    self.assertIs(type(cast), MyInt)
    with self.assertRaises(TypeCastException):
      typeCast(MyInt, 2.5, allowInstantiation=False)

  def test_plain_subclass_construction_checked(self) -> None:
    """A plain subclass whose metaclass makes the call refuse the cast
    value, or return something that is not an instance of it, is refused
    with 'TypeCastException', naming the subclass."""

    class Refusing(type):
      def __call__(cls, *args: Any) -> Any:
        raise ValueError('no instances')

    class Shifting(type):
      def __call__(cls, *args: Any) -> Any:
        return 42

    class NoStr(str, metaclass=Refusing):
      pass

    class OddStr(str, metaclass=Shifting):
      pass

    for target in (NoStr, OddStr):
      with self.subTest(target=target.__name__):
        with self.assertRaises(TypeCastException) as context:
          typeCast(target, b'abc')
        self.assertIs(context.exception.type_, target)

  def test_own_constructor_trusted(self) -> None:
    """A subclass with a constructor of its own receives the value as
    given, past the rule of its builtin."""

    class Upper(str):
      def __new__(cls, value: Any) -> Any:
        return str.__new__(cls, str(value).upper())

    class Level(IntEnum):
      LOW = 1
      HIGH = 2

    cast = typeCast(Upper, 5)
    self.assertIs(type(cast), Upper)
    self.assertEqual(cast, '5')
    self.assertEqual(typeCast(Upper, 'abc'), 'ABC')
    self.assertIs(typeCast(Level, 1.0), Level.LOW)
    self.assertEqual(typeCast(Counter, 'abba'), Counter(a=2, b=2))

  def test_inherited_constructor_trusted(self) -> None:
    """A constructor inherited from a class between the subclass and its
    builtin, or an '__init__' from a mixin after the builtin, counts as
    the subclass's own."""

    class Upper(str):
      def __new__(cls, value: Any) -> Any:
        return str.__new__(cls, str(value).upper())

    class Shout(Upper):
      pass

    class Tagged:
      def __init__(self, *args: Any) -> None:
        pass

    class TaggedStr(str, Tagged):
      pass

    self.assertEqual(typeCast(Shout, 5), '5')
    self.assertEqual(typeCast(TaggedStr, 5), '5')

  def test_trusted_constructor_refusing(self) -> None:
    """A trusted constructor that refuses the value, or returns something
    that is not an instance of the subclass, is refused with
    'TypeCastException', and so is any trusted constructor when
    'allowInstantiation' is false."""

    class Picky(str):
      def __new__(cls, value: Any) -> Any:
        if value != 'yes':
          raise ValueError('only yes')
        return str.__new__(cls, value)

    class Shifty(int):
      def __new__(cls, value: Any) -> Any:
        return 42.0

    self.assertEqual(typeCast(Picky, 'yes'), 'yes')
    cases = ((Picky, b'yes', {}), (Shifty, 2.0, {}),
             (Picky, 'yes', dict(allowInstantiation=False)))
    for target, value, kwargs in cases:
      with self.subTest(target=target.__name__, kwargs=kwargs):
        with self.assertRaises(TypeCastException) as context:
          typeCast(target, value, **kwargs)
        self.assertIs(context.exception.type_, target)
