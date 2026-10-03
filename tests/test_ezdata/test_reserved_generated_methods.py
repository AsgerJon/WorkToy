"""
TestReservedGeneratedMethods subclasses 'EZTest' from the
'tests.test_ezdata' package and pins that an EZData class body may not
define a method EZData generates after the class body is merged. Such a
definition used to be dropped without a word, so a class-body '__init__'
or '__eq__' simply never ran. Each of these names is now refused at the
offending line with 'ReservedMethodError', as '__setattr__' already was.
The helpers EZData installs before the class body, such as '__repr__',
stay open to a class-body definition, which takes their place. The
classes are built inside the tests, so a failure stays in its test.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.ezdata import EZData, EZField, EZMeta
from worktoy.waitaminute.ezdata import ReservedMethodError

from . import EZTest

_REFUSED = (
  '__init__',
  '__iter__',
  '__eq__',
  '__delattr__',
  '__hash__',
  '__lt__',
  '__le__',
  '__gt__',
  '__ge__',
  '__setattr__',
)


#  A class-body method standing in for any of the refused ones, never run.
_method = lambda *args: 'class body'


class TestReservedGeneratedMethods(EZTest):
  """
  TestReservedGeneratedMethods provides tests for the methods an EZData
  class body may not define.
  """

  def test_generated_methods_refused(self) -> None:
    """Each generated method is refused, naming the method."""
    for name in _REFUSED:
      with self.subTest(name=name):
        with self.assertRaises(ReservedMethodError) as context:
          EZMeta('Point', (EZData,), {'x': EZField[int](0), name: _method})
        self.assertEqual(context.exception.methodName, name)
        self.assertIn(name, str(context.exception))

  def test_class_statement_refused(self) -> None:
    """A class statement defining '__init__' is refused at that line."""
    with self.assertRaises(ReservedMethodError):
      class Tagged(EZData):
        x = EZField[int](0)

        __init__ = lambda self, *args, **kwargs: None

  def test_overridable_helpers_kept(self) -> None:
    """The helpers installed before the class body may still be defined,
    and the class-body definition takes their place."""

    class Named(EZData):
      x = EZField[int](0)

      def __repr__(self) -> str:
        return 'Named!'

      def __post_init__(self) -> None:
        self.x += 1

    named = Named(1)
    self.assertEqual(repr(named), 'Named!')
    self.assertEqual(named.x, 2)
