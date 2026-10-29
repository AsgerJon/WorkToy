"""
TestClassHashCache pins that the default hash of a class, made from the
names of the class, its bases and its metaclass, is computed once, at the
first hash, and kept in the class's own '__dict__' under
'__class_hash_value__'. A class renamed after it was hashed, as a factory
names the class it built, keeps its hash, so a dict or set holding it,
such as a registry filled in '__init_subclass__', still finds it. It used
to hash by its new name and be lost. A class defining '__class_hash__' is
asked at every hash, and a subclass computes its own default.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.mcls import AbstractMetaclass, BaseObject

from .. import MCLSTest

registry = {}


class Plugin(BaseObject):
  """Plugin registers every subclass, keyed by the class itself."""

  def __init_subclass__(cls, **kwargs) -> None:
    super().__init_subclass__(**kwargs)
    registry[cls] = cls.__name__


def makePlugin(name: str) -> type:
  """Returns a new subclass of 'Plugin', named after it was created."""

  class _Impl(Plugin):
    pass

  _Impl.__name__ = name
  return _Impl


class Counter(metaclass=AbstractMetaclass):
  """Counter answers every hash with the next count."""

  __hash_count__ = 0

  @classmethod
  def __class_hash__(cls) -> int:
    cls.__hash_count__ += 1
    return cls.__hash_count__


class TestClassHashCache(MCLSTest):
  """
  TestClassHashCache provides tests for the default class hash being
  computed once per class and kept for the life of the class.
  """

  def test_renamed_class_stays_registered(self) -> None:
    """A class renamed after a registry hashed it is still found there."""
    csv = makePlugin('Csv')
    self.assertIn(csv, registry)
    self.assertEqual(registry[csv], '_Impl')

  def test_kept_value_is_the_default(self) -> None:
    """The kept value is the documented default, as first computed, and a
    later rename leaves it."""

    class Plain(metaclass=AbstractMetaclass):
      pass

    expected = hash(('Plain', 'AbstractMetaclass'))
    self.assertEqual(hash(Plain), expected)
    self.assertEqual(Plain.__dict__['__class_hash_value__'], expected)
    Plain.__name__ = 'Renamed'
    self.assertEqual(hash(Plain), expected)

  def test_subclass_computes_its_own(self) -> None:
    """A subclass created after its base was hashed computes its own
    default instead of reading the base's through inheritance."""

    class Base(metaclass=AbstractMetaclass):
      pass

    self.assertEqual(hash(Base), hash(('Base', 'AbstractMetaclass')))

    class Sub(Base):
      pass

    expected = hash(('Sub', 'Base', 'AbstractMetaclass'))
    self.assertEqual(hash(Sub), expected)
    self.assertEqual(Sub.__dict__['__class_hash_value__'], expected)

  def test_class_hash_asked_every_time(self) -> None:
    """A class defining '__class_hash__' is asked at every hash, and
    nothing is kept for it."""
    first = hash(Counter)
    self.assertEqual(hash(Counter), first + 1)
    self.assertNotIn('__class_hash_value__', Counter.__dict__)
