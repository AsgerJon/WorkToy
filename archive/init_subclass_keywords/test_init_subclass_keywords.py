"""
TestInitSubclassKeywords subclasses 'UtilitiesTest' and pins
'initSubclassKeywords', which names the class keywords that the
'__init_subclass__' methods of the given classes declare by name. A
declared keyword is a named parameter after the class parameter, by
position or keyword only; a '**kwargs' catch-all declares none, since it
promises to pass anything on, which 'object.__init_subclass__' then
refuses.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.utilities import initSubclassKeywords

from . import UtilitiesTest


class Tagged:
  """Tagged declares 'tag' as a named parameter."""

  def __init_subclass__(cls, tag=None, **kwargs) -> None:
    super().__init_subclass__(**kwargs)
    cls.tag = tag


class Levelled:
  """Levelled declares 'level' as a keyword-only parameter."""

  def __init_subclass__(cls, *, level=0, **kwargs) -> None:
    super().__init_subclass__(**kwargs)
    cls.level = level


class Swallower:
  """Swallower takes any keyword and declares none."""

  def __init_subclass__(cls, **kwargs) -> None:
    super().__init_subclass__()


class Silent:
  """Silent defines no '__init_subclass__' of its own."""


class Inheriting(Tagged):
  """Inheriting inherits the '__init_subclass__' of 'Tagged' and defines
  none of its own."""


class TestInitSubclassKeywords(UtilitiesTest):
  """
  TestInitSubclassKeywords provides tests for 'initSubclassKeywords'.
  """

  def test_named_parameter(self) -> None:
    """A parameter named after the class parameter is a declared
    keyword."""
    self.assertEqual(initSubclassKeywords(Tagged), ('tag',))

  def test_keyword_only_parameter(self) -> None:
    """A keyword-only parameter is a declared keyword as well."""
    self.assertEqual(initSubclassKeywords(Levelled), ('level',))

  def test_catch_all_declares_nothing(self) -> None:
    """A '**kwargs' catch-all declares no keyword."""
    self.assertEqual(initSubclassKeywords(Swallower), ())

  def test_without_init_subclass(self) -> None:
    """A class without an '__init_subclass__' of its own declares
    nothing, whether it inherits one or not, and neither does
    'object'."""
    self.assertEqual(initSubclassKeywords(Silent), ())
    self.assertEqual(initSubclassKeywords(Inheriting), ())
    self.assertEqual(initSubclassKeywords(object), ())

  def test_several_classes(self) -> None:
    """The keywords of several classes come in the order of the classes,
    each name once."""
    names = initSubclassKeywords(Tagged, Silent, Levelled, Tagged, object)
    self.assertEqual(names, ('tag', 'level'))

  def test_no_classes(self) -> None:
    """No classes declare no keywords."""
    self.assertEqual(initSubclassKeywords(), ())
