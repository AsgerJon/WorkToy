"""
TestDefaultUniqueness subclasses 'DescTest' from the 'tests.test_desc'
package and pins the per-instance uniqueness of mutable 'AttriBox'
defaults. A mutable default such as 'AttriBox[list]([1, 2, 3])' must give
every instance its own object; the captured class-body literal acts as a
template, never as one object shared across all instances.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.desc import AttriBox
from worktoy.mcls import BaseObject
from . import DescTest


class TestDefaultUniqueness(DescTest):
  """
  TestDefaultUniqueness pins the per-instance uniqueness of mutable
  'AttriBox' defaults, mirroring the guarantee 'EZData' already makes for
  its fields. Two fresh instances must not share a mutable default object,
  so mutating one is never observable on another.
  """

  def test_list_default_unique_per_instance(self) -> None:
    """A list default declared as 'AttriBox[list]([...])' is its own
    object on every instance."""

    class Bag(BaseObject):
      items = AttriBox[list]([1, 2, 3])

    a, b = Bag(), Bag()
    self.assertIsNot(a.items, b.items)
    self.assertEqual(a.items, [1, 2, 3])
    self.assertEqual(b.items, [1, 2, 3])

  def test_dict_default_unique_per_instance(self) -> None:
    """A dict default is its own object on every instance."""

    class Bag(BaseObject):
      mapping = AttriBox[dict]({'k': 'v'})

    a, b = Bag(), Bag()
    self.assertIsNot(a.mapping, b.mapping)
    self.assertEqual(a.mapping, {'k': 'v'})
    self.assertEqual(b.mapping, {'k': 'v'})

  def test_set_default_unique_per_instance(self) -> None:
    """A set default is its own object on every instance."""

    class Bag(BaseObject):
      tags = AttriBox[set]({1, 2, 3})

    a, b = Bag(), Bag()
    self.assertIsNot(a.tags, b.tags)
    self.assertEqual(a.tags, {1, 2, 3})
    self.assertEqual(b.tags, {1, 2, 3})

  def test_mutation_does_not_leak_between_instances(self) -> None:
    """Mutating the default-derived list on one instance must not be
    observable on another instance of the same class."""

    class Bag(BaseObject):
      items = AttriBox[list]([1, 2, 3])

    first, second = Bag(), Bag()
    first.items.append(99)
    self.assertEqual(first.items, [1, 2, 3, 99])
    self.assertEqual(second.items, [1, 2, 3])

  def test_empty_container_default_unique(self) -> None:
    """The no-argument container form keeps its existing per-instance
    freshness."""

    class Bag(BaseObject):
      items = AttriBox[list]()

    a, b = Bag(), Bag()
    self.assertIsNot(a.items, b.items)
    self.assertEqual(a.items, [])
    self.assertEqual(b.items, [])

  def test_splatted_container_default_unique(self) -> None:
    """The multi-argument container form ('AttriBox[list](1, 2, 3)')
    likewise builds a fresh object per instance."""

    class Bag(BaseObject):
      items = AttriBox[list](1, 2, 3)

    a, b = Bag(), Bag()
    self.assertIsNot(a.items, b.items)
    self.assertEqual(a.items, [1, 2, 3])
    self.assertEqual(b.items, [1, 2, 3])

  def test_prebuilt_object_default_unique(self) -> None:
    """An arbitrary pre-built object passed as the default is deep-copied
    per instance, so no two instances share the captured object."""

    class Ancestor(BaseObject):
      pass

    seed = Ancestor()

    class Holder(BaseObject):
      held = AttriBox[Ancestor](seed)

    a, b = Holder(), Holder()
    self.assertIsInstance(a.held, Ancestor)
    self.assertIsNot(a.held, seed)
    self.assertIsNot(a.held, b.held)

  def test_nested_mutable_default_is_independent(self) -> None:
    """The copy is deep, so a mutable object nested inside the default is
    independent per instance too, not merely the top-level container."""

    class Bag(BaseObject):
      items = AttriBox[list]([[1], [2]])

    a, b = Bag(), Bag()
    self.assertIsNot(a.items[0], b.items[0])
    a.items[0].append(99)
    self.assertEqual(b.items, [[1], [2]])

  def test_uncopyable_default_is_shared_without_raising(self) -> None:
    """A value that refuses to be copied is stored unchanged rather than
    raising: receiving a value of the exact field type must never error.
    Such a value is shared, the only alternative to raising."""

    class Uncopyable:
      def __deepcopy__(self, memo: dict) -> None:
        raise TypeError('this value cannot be copied')

    seed = Uncopyable()

    class Keep(BaseObject):
      value = AttriBox[Uncopyable](seed)

    a, b = Keep(), Keep()
    self.assertIs(a.value, seed)
    self.assertIs(b.value, seed)
