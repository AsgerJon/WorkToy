"""
TestInitSubclassKeyword subclasses 'EZTest' and pins what an 'EZData'
class statement does with a class keyword that is none of its options.
With a base that has an '__init_subclass__' of its own, the keyword goes
down the '__init_subclass__' chain, where that base takes it or 'object'
refuses it: 'class Point(EZData, Tagged, tag='hello')', where 'Tagged'
takes 'tag', used to raise 'ClassKeywordError'. With no such base nothing
could read the keyword, and 'ClassKeywordError' refuses it at the class
statement, listing the accepted spellings, so a misspelled option still
fails loudly.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from types import new_class

from worktoy.ezdata import EZData, EZField
from worktoy.waitaminute.ezdata import ClassKeywordError

from . import EZTest


class Tagged:
  """Tagged gives each subclass a tag from the class statement and passes
  the rest on, as the Python docs show."""

  tag = None

  def __init_subclass__(cls, tag=None, **kwargs) -> None:
    super().__init_subclass__(**kwargs)
    cls.tag = tag


class Levelled:
  """Levelled declares its keyword as keyword-only."""

  level = 0

  def __init_subclass__(cls, *, level=0, **kwargs) -> None:
    super().__init_subclass__(**kwargs)
    cls.level = level


class Watcher:
  """Watcher takes any keyword through '**kwargs' and passes none on."""

  received = None

  def __init_subclass__(cls, **kwargs) -> None:
    super().__init_subclass__()
    cls.received = dict(kwargs)


class TestInitSubclassKeyword(EZTest):
  """
  TestInitSubclassKeyword provides tests for the class keywords of a
  base's own '__init_subclass__' on an 'EZData' class.
  """

  def test_named_keyword_accepted(self) -> None:
    """The keyword a base names reaches the base, and the class works as
    any 'EZData' class."""

    class Point(EZData, Tagged, tag='hello'):
      x = EZField[int](0)

    self.assertEqual(Point.tag, 'hello')
    self.assertEqual(Point(1).x, 1)
    self.assertEqual(Point(), Point(0))

  def test_with_an_option(self) -> None:
    """The keyword of the base and an option of 'EZData' go together,
    each to its reader, the option never entering the chain."""

    class Point(EZData, Tagged, tag='frozen point', frozen=True):
      x = EZField[int](0)

    self.assertEqual(Point.tag, 'frozen point')
    self.assertTrue(Point.isFrozen)
    with self.assertRaises(AttributeError):
      Point().x = 1

  def test_keyword_only_parameter(self) -> None:
    """A keyword declared as keyword-only arrives too."""

    class Point(EZData, Levelled, level=2):
      x = EZField[int](0)

    self.assertEqual(Point.level, 2)

  def test_catch_all_receives_keyword(self) -> None:
    """A base taking any keyword through '**kwargs' receives the keyword
    no option took."""

    class Point(EZData, Watcher, extra=1):
      x = EZField[int](0)

    self.assertEqual(Point.received, {'extra': 1})
    self.assertEqual(Point(2).x, 2)

  def test_misspelled_refused_without_reader(self) -> None:
    """With no base having an '__init_subclass__' of its own, a keyword
    that is no option is refused at the class statement, and the refusal
    lists the accepted spellings. The class is built through 'new_class',
    since the refusal comes before the body of a class statement would
    run."""
    body = lambda namespace: namespace.update(x=EZField[int](0))
    with self.assertRaises(ClassKeywordError) as context:
      new_class('Point', (EZData,), dict(frozn=True), body)
    self.assertEqual(context.exception.keyword, 'frozn')
    self.assertIn('frozen', context.exception.accepted)
    self.assertIn('trustMeBro', context.exception.accepted)

  def test_misspelled_refused_by_object(self) -> None:
    """With a base passing keywords on, a misspelled keyword goes down the
    chain and 'object' refuses it, as in a plain class."""
    with self.assertRaises(TypeError) as context:
      class Point(EZData, Tagged, tg='hello'):
        x = EZField[int](0)
    self.assertNotIsInstance(context.exception, ClassKeywordError)
    self.assertIn('takes no keyword arguments', str(context.exception))

  def test_base_before_ez_data(self) -> None:
    """The base may come before 'EZData' as well."""

    class Point(Tagged, EZData, tag='hello'):
      x = EZField[int](0)

    self.assertEqual(Point.tag, 'hello')
    self.assertEqual(Point(3).x, 3)
