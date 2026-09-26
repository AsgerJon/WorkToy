"""
TestPlainMethodCalls subclasses 'SpaceHookTest' from the
'tests.test_mcls.test_hooks' package and pins that an ordinary method in
the body of a 'BaseObject' subclass is called exactly as Python calls a
method of a plain class. The namespace keeps the function as it was
written, so a keyword argument may supply a positional parameter, an
extra positional argument raises 'TypeError' rather than disappearing,
and an attribute set on the function stays on it.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.mcls import BaseObject

from . import SpaceHookTest

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any


def _identity(self: Any, x: Any) -> Any:
  """The '_identity' function returns its argument. The tests bind it in
  a class body, where it becomes an ordinary method."""
  return x


class TestPlainMethodCalls(SpaceHookTest):
  """
  TestPlainMethodCalls provides tests for calling ordinary methods on
  instances of 'BaseObject' subclasses.
  """

  @staticmethod
  def _buildSubject() -> type:
    """The '_buildSubject' method builds a fresh 'BaseObject' subclass
    holding one method of each shape the tests call."""

    class Subject(BaseObject):
      def one(self, x: Any) -> Any:
        return x

      def two(self, x: Any, y: Any) -> tuple:
        return x, y

      def withDefault(self, x: Any, y: Any = 10) -> tuple:
        return x, y

    return Subject

  def test_keyword_supplies_positional(self) -> None:
    """A positional parameter receives its value by keyword."""
    subject = self._buildSubject()()
    self.assertEqual(subject.one(x=1), 1)

  def test_keyword_supplies_every_parameter(self) -> None:
    """Every parameter receives its value by keyword."""
    subject = self._buildSubject()()
    self.assertEqual(subject.two(x=1, y=2), (1, 2))

  def test_positional_then_keyword(self) -> None:
    """The first parameter receives its value by position and the second
    by keyword."""
    subject = self._buildSubject()()
    self.assertEqual(subject.two(1, y=2), (1, 2))

  def test_keyword_leaves_default(self) -> None:
    """A keyword for the required parameter leaves the defaulted one at
    its default."""
    subject = self._buildSubject()()
    self.assertEqual(subject.withDefault(x=1), (1, 10))

  def test_keyword_through_class(self) -> None:
    """Called through the class with the instance passed explicitly, the
    method still takes a keyword for its positional parameter."""
    cls = self._buildSubject()
    subject = cls()
    self.assertEqual(cls.one(subject, x=1), 1)

  def test_extra_positional_raises(self) -> None:
    """A positional argument beyond those the method declares raises
    'TypeError' instead of being dropped."""
    subject = self._buildSubject()()
    with self.assertRaises(TypeError):
      subject.one(1, 2)
    with self.assertRaises(TypeError):
      subject.withDefault(1, 2, 3)

  def test_function_kept_as_written(self) -> None:
    """The class keeps the function bound in its body, not a wrapper
    around it."""

    class Subject(BaseObject):
      method = _identity

    self.assertIs(Subject.__dict__['method'], _identity)
    self.assertEqual(Subject().method(69), 69)

  def test_function_attribute_kept(self) -> None:
    """An attribute set on a function in the class body is still there
    when the function is read back through the class or an instance."""

    class Subject(BaseObject):
      def tagged(self) -> str:
        return 'tagged'

      tagged.tag = 'kept'

    self.assertEqual(Subject.tagged.tag, 'kept')
    self.assertEqual(Subject().tagged.tag, 'kept')
    self.assertEqual(Subject().tagged(), 'tagged')

  def test_exact_positional_call(self) -> None:
    """A call supplying each parameter by position returns as written."""
    subject = self._buildSubject()()
    self.assertEqual(subject.two(1, 2), (1, 2))
    self.assertEqual(subject.withDefault(1), (1, 10))
    self.assertEqual(subject.withDefault(1, 2), (1, 2))

  def test_missing_argument_raises(self) -> None:
    """A call leaving a required parameter without a value raises
    'TypeError'."""
    subject = self._buildSubject()()
    with self.assertRaises(TypeError):
      subject.one()
    with self.assertRaises(TypeError):
      subject.two(y=2)

  def test_unknown_keyword_raises(self) -> None:
    """A keyword the method does not declare raises 'TypeError'."""
    subject = self._buildSubject()()
    with self.assertRaises(TypeError):
      subject.one(1, z=2)
