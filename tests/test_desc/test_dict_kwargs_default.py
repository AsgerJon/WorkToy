"""
TestDictKwargsDefault pins the keyword-argument path of the deferred
'AttriBox' default for the builtin container field types. A declaration
such as 'AttriBox[dict](a=1, b=2)' builds its default through normal
construction, so the captured keyword arguments end up in the dict
instead of being silently discarded by the container-of-positional-args
special case, which applies only when no keyword arguments were
captured.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.desc import AttriBox
from worktoy.mcls import BaseObject
from . import DescTest


class TestDictKwargsDefault(DescTest):
  """
  TestDictKwargsDefault pins the content and the per-instance ownership
  of 'AttriBox' container defaults captured as keyword arguments.
  """

  def test_kwargs_default_content(self) -> None:
    """A dict default declared with keyword arguments holds exactly
    those keyword arguments."""

    class Bag(BaseObject):
      mapping = AttriBox[dict](a=1, b=2)

    bag = Bag()
    self.assertEqual(bag.mapping, {'a': 1, 'b': 2})

  def test_kwargs_default_unique_per_instance(self) -> None:
    """A kwargs-built dict default is its own object on every instance,
    so mutating one instance is never observable on another."""

    class Bag(BaseObject):
      mapping = AttriBox[dict](a=1, b=2)

    first, second = Bag(), Bag()
    self.assertIsNot(first.mapping, second.mapping)
    first.mapping['c'] = 3
    self.assertEqual(first.mapping, {'a': 1, 'b': 2, 'c': 3})
    self.assertEqual(second.mapping, {'a': 1, 'b': 2})

  def test_mixed_args_and_kwargs_default(self) -> None:
    """A dict default combining a positional seed with keyword
    arguments builds through normal construction, merging both."""

    class Bag(BaseObject):
      mapping = AttriBox[dict]([('k', 'v')], a=1)

    bag = Bag()
    self.assertEqual(bag.mapping, {'k': 'v', 'a': 1})

  def test_lone_dict_with_kwargs_default(self) -> None:
    """A lone dict argument accompanied by keyword arguments is not
    deep-copied as-is, since the copy would discard the keyword
    arguments; normal construction merges both instead."""

    class Bag(BaseObject):
      mapping = AttriBox[dict]({'k': 'v'}, a=1)

    first, second = Bag(), Bag()
    self.assertEqual(first.mapping, {'k': 'v', 'a': 1})
    self.assertIsNot(first.mapping, second.mapping)
    self.assertEqual(second.mapping, {'k': 'v', 'a': 1})
