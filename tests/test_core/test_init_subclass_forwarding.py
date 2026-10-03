"""
TestInitSubclassForwarding subclasses 'CoreTest' and pins what reaches the
'__init_subclass__' of a base of a worktoy class from the class statement.
The keywords worktoy itself reads, such as 'trustMeBro', stay with the
namespace and never enter the '__init_subclass__' chain. Every other
keyword goes down the chain, to a base ahead of 'Object' or after it
alike, whether the base names the keyword or takes it through '**kwargs'.
What a base passes on that no base takes reaches 'object.__init_subclass__',
which refuses it, so a base forwarding a keyword it does not know raises as
it would in a plain class. 'Object' itself defines no '__init_subclass__':
it used to take every keyword and pass on only the ones a base named, so a
base taking '**kwargs' received nothing.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.mcls import BaseObject

from . import CoreTest


class Tagged:
  """Tagged gives each subclass a tag from the class statement, records
  what else it received and passes that on, as the Python docs show."""

  tag = None
  received = None

  def __init_subclass__(cls, tag=None, **kwargs) -> None:
    super().__init_subclass__(**kwargs)
    cls.tag = tag
    cls.received = dict(kwargs)


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


class TestInitSubclassForwarding(CoreTest):
  """
  TestInitSubclassForwarding provides tests for the class keywords that
  reach the '__init_subclass__' of the bases of a worktoy class.
  """

  def test_named_keyword_arrives(self) -> None:
    """A base after 'Object' receives the keyword its '__init_subclass__'
    names."""

    class Widget(BaseObject, Tagged, tag='hello'):
      pass

    self.assertEqual(Widget.tag, 'hello')
    self.assertEqual(Widget.received, {})

  def test_worktoy_keyword_stays_out(self) -> None:
    """A keyword worktoy reads, 'trustMeBro' for its hook and
    '_strictMRO' for the namespace itself, never enters the chain, so the
    base sees its own keyword alone, while the namespace records all."""

    class Widget(BaseObject, Tagged, tag='hello', trustMeBro=True,
                 _strictMRO=True):
      pass

    self.assertEqual(Widget.tag, 'hello')
    self.assertEqual(Widget.received, {})
    self.assertEqual(Widget.__keyword_arguments__,
                     {'tag': 'hello', 'trustMeBro': True, '_strictMRO': True})

  def test_keyword_only_parameter(self) -> None:
    """A keyword the base declares as keyword-only arrives as well."""

    class Widget(BaseObject, Levelled, level=3):
      pass

    self.assertEqual(Widget.level, 3)

  def test_base_before_object(self) -> None:
    """A base ahead of 'Object' receives the same: its keyword, and not
    the ones worktoy reads."""

    class Gadget(Tagged, BaseObject, tag='hello', trustMeBro=True):
      pass

    self.assertEqual(Gadget.tag, 'hello')
    self.assertEqual(Gadget.received, {})

  def test_catch_all_receives_keyword(self) -> None:
    """A base taking any keyword through '**kwargs' receives the keyword
    no other reader took, after 'Object' as ahead of it."""

    class Widget(BaseObject, Watcher, flavour='vanilla'):
      pass

    class Gadget(Watcher, BaseObject, flavour='vanilla'):
      pass

    self.assertEqual(Widget.received, {'flavour': 'vanilla'})
    self.assertEqual(Gadget.received, {'flavour': 'vanilla'})
    self.assertEqual(Widget.__keyword_arguments__, {'flavour': 'vanilla'})

  def test_forwarded_keyword_refused_by_object(self) -> None:
    """A keyword a base passes on that no base takes reaches 'object',
    which refuses it, whichever side of 'Object' the base is on."""
    with self.assertRaises(TypeError) as context:
      class Widget(BaseObject, Tagged, flavour='vanilla'):
        pass
    self.assertIn('takes no keyword arguments', str(context.exception))
    with self.assertRaises(TypeError) as context:
      class Gadget(Tagged, BaseObject, flavour='vanilla'):
        pass
    self.assertIn('takes no keyword arguments', str(context.exception))

  def test_subclass_without_keyword(self) -> None:
    """A subclass stating no keyword leaves the base at its default."""

    class Widget(BaseObject, Tagged, tag='hello'):
      pass

    class Sub(Widget):
      pass

    self.assertIsNone(Sub.tag)
    self.assertEqual(Widget.tag, 'hello')
