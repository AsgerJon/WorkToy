"""
TestBaseObjectArguments pins that a 'BaseObject' subclass defining
neither '__init__' nor '__new__' refuses constructor arguments, as a
plain Python class does. It used to accept them through 'Object.__init__'
and drop them without a word. A subclass with an initializer of its own,
inherited or overloaded, or with a '__new__' of its own, is unaffected,
and arguments handed on to 'super().__init__' are still recorded.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.desc import AttriBox
from worktoy.dispatch import overload
from worktoy.mcls import BaseObject

from .. import MCLSTest


class Point(BaseObject):
  """Point declares fields and no initializer."""

  x = AttriBox[int](0)
  y = AttriBox[int](0)


class Forwarding(BaseObject):
  """Forwarding hands every argument on to 'BaseObject.__init__'."""

  def __init__(self, *args, **kwargs) -> None:
    BaseObject.__init__(self, *args, **kwargs)


class Inheriting(Forwarding):
  """Inheriting takes the initializer of its base."""


class Overloaded(BaseObject):
  """Overloaded has an overloaded initializer."""

  x = AttriBox[int](0)

  @overload(int)
  def __init__(self, x: int) -> None:
    self.x = x

  @overload()
  def __init__(self) -> None:
    pass


class Allocated(BaseObject):
  """Allocated takes its arguments in '__new__'."""

  def __new__(cls, *args, **kwargs) -> Allocated:
    self = object.__new__(cls)
    self.received = args
    return self


class TestBaseObjectArguments(MCLSTest):
  """
  TestBaseObjectArguments provides tests for the constructor arguments of
  'BaseObject' subclasses.
  """

  def test_positional_refused(self) -> None:
    """Positional arguments to a class without an initializer raise
    the 'TypeError' Python raises for a plain class."""
    with self.assertRaises(TypeError) as context:
      Point(3, 4)
    self.assertEqual(str(context.exception), 'Point() takes no arguments')

  def test_keyword_refused(self) -> None:
    """Keyword arguments are refused the same way."""
    with self.assertRaises(TypeError) as context:
      Point(x=3)
    self.assertEqual(str(context.exception), 'Point() takes no arguments')

  def test_base_object_refused(self) -> None:
    """'BaseObject' itself takes no arguments."""
    with self.assertRaises(TypeError) as context:
      BaseObject(1)
    expected = 'BaseObject() takes no arguments'
    self.assertEqual(str(context.exception), expected)

  def test_no_arguments(self) -> None:
    """A class without an initializer still constructs without
    arguments, its fields at their defaults."""
    point = Point()
    self.assertEqual((point.x, point.y), (0, 0))

  def test_forwarding_records(self) -> None:
    """Arguments handed on to 'BaseObject.__init__' by an initializer of
    the subclass are recorded as before."""
    forwarding = Forwarding(1, 2, key='value')
    self.assertEqual(forwarding.getPosArgs(), (1, 2))
    self.assertEqual(forwarding.getKeyArgs(), {'key': 'value'})

  def test_inherited_initializer(self) -> None:
    """An initializer inherited from a base below 'BaseObject' counts as
    the subclass's own."""
    self.assertEqual(Inheriting(1).getPosArgs(), (1,))

  def test_overloaded_initializer(self) -> None:
    """An overloaded initializer receives its arguments."""
    self.assertEqual(Overloaded(7).x, 7)
    self.assertEqual(Overloaded().x, 0)

  def test_own_new(self) -> None:
    """A class taking its arguments in '__new__' receives them, as a
    plain class overriding '__new__' alone does."""
    self.assertEqual(Allocated(1, 2).received, (1, 2))
