"""
TestDefaultValueUniqueness subclasses 'EZTest' from the
'tests.test_ezdata' package and provides tests for the uniqueness of
default values in 'EZData' dataclasses.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.ezdata import EZData, EZField
from . import EZTest

if TYPE_CHECKING:  # pragma: no cover
  pass


class TestDefaultValueUniqueness(EZTest):
  """
  TestDefaultValueUniqueness subclasses 'EZTest' from the
  'tests.test_ezdata' package and provides tests for the uniqueness of
  default values in 'EZData' dataclasses. The expected behavior is
  that every fresh instance receives its own copy of a mutable
  default; in particular, mutating one instance must not be
  observable on any other instance of the same class.
  """

  def test_list_default_is_unique_per_instance(self) -> None:
    """
    Two fresh instances of an 'EZData' subclass with a list-typed
    field declared as 'EZField[list]([...])' must each receive
    their own list object. The field's declared default acts as a
    template, not as a shared instance.
    """

    class WithList(EZData):
      xs = EZField[list]([1, 2, 3])

    a = WithList()
    b = WithList()
    self.assertIsNot(a.xs, b.xs)
    self.assertEqual(a.xs, [1, 2, 3])
    self.assertEqual(b.xs, [1, 2, 3])

  def test_list_factory_default_is_unique_per_instance(self) -> None:
    """
    Two fresh instances of an 'EZData' subclass with a list-typed
    field declared as 'EZField[list]()' must each receive their
    own empty list. The no-argument form is the natural spelling
    for a list-valued default and must not share state across
    instances.
    """

    class WithFactoryList(EZData):
      xs = EZField[list]()

    a = WithFactoryList()
    b = WithFactoryList()
    self.assertIsNot(a.xs, b.xs)
    self.assertEqual(a.xs, [])
    self.assertEqual(b.xs, [])

  def test_dict_default_is_unique_per_instance(self) -> None:
    """
    Two fresh instances of an 'EZData' subclass with a dict-typed
    field must each receive their own dict, regardless of whether
    the default was given as a literal or constructed by the
    field's no-argument form.
    """

    class WithDict(EZData):
      data = EZField[dict]({'key': 'value'})

    a = WithDict()
    b = WithDict()
    self.assertIsNot(a.data, b.data)
    self.assertEqual(a.data, {'key': 'value'})
    self.assertEqual(b.data, {'key': 'value'})

  def test_mutation_does_not_leak_between_instances(self) -> None:
    """
    Mutating the default-derived value on one instance must not
    change the value seen by any other instance of the same
    class. This is the functional consequence of per-instance
    default uniqueness and the most likely real-world symptom
    of the shared-default bug.
    """

    class WithItems(EZData):
      items = EZField[list]([1, 2, 3])

    first = WithItems()
    second = WithItems()
    first.items.append(99)
    self.assertEqual(first.items, [1, 2, 3, 99])
    self.assertEqual(second.items, [1, 2, 3])
