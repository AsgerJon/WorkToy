"""
TestClassBool tests the '__class_bool__' method on classes derived from
the 'AbstractMetaclass' from the 'worktoy.mcls' module.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.ezdata import EZMeta
from worktoy.waitaminute.ez import EZMultipleInheritance
from .. import MCLSTest
from worktoy.mcls import AbstractMetaclass

if TYPE_CHECKING:  # pragma: no cover
  from typing import Iterator


class EmptyIterator(metaclass=AbstractMetaclass):
  """EmptyIterator is 'False' because it yields from an empty tuple. """

  @classmethod
  def __class_iter__(cls) -> Iterator:
    yield from ()


class FullIterator(metaclass=AbstractMetaclass):
  """FullIterator is 'True' because it yields from a non-empty tuple. """

  @classmethod
  def __class_iter__(cls) -> Iterator:
    yield from (69, 420, 1337)


class VintageIteratorTrue(metaclass=AbstractMetaclass):
  """Provides non-empty iterator in the old-fashioned style. """

  __iter_contents__ = None

  @classmethod
  def __class_iter__(cls) -> Iterator:
    cls.__iter_contents__ = [69, 420, 1337]
    return cls

  @classmethod
  def __class_next__(cls) -> int:
    if cls.__iter_contents__:
      return cls.__iter_contents__.pop(0)
    cls.__iter_contents__ = None
    raise StopIteration


class VintageIteratorFalse(metaclass=AbstractMetaclass):
  """Provides empty iterator in the old-fashioned style. """

  __iter_contents__ = None

  @classmethod
  def __class_iter__(cls) -> Iterator:
    cls.__iter_contents__ = []
    return cls

  @classmethod
  def __class_next__(cls) -> int:
    if cls.__iter_contents__:
      return cls.__iter_contents__.pop(0)
    cls.__iter_contents__ = None
    raise StopIteration


class ExplicitTrue(metaclass=AbstractMetaclass):
  """ExplicitTrue is 'True' because it has a __class_bool__ method that
  returns True."""

  @classmethod
  def __class_bool__(cls) -> bool:
    return True


class ExplicitFalse(metaclass=AbstractMetaclass):
  """ExplicitFalse is 'False' because it has a __class_bool__ method that
  returns False."""

  @classmethod
  def __class_bool__(cls) -> bool:
    return False


class LenFalse(metaclass=AbstractMetaclass):
  """LenFalse is 'False' because it has a __len__ method that returns 0."""

  @classmethod
  def __class_len__(cls) -> int:
    return 0


class LenTrue(metaclass=AbstractMetaclass):
  """LenTrue is 'True' because it has a __len__ method that returns a
  non-zero value."""

  @classmethod
  def __class_len__(cls) -> int:
    return 80085


class TestClassBool(MCLSTest):
  """TestClassBool tests the '__class_bool__' method on classes derived from
  the 'AbstractMetaclass' from the 'worktoy.mcls' module."""

  def test_empty_iterator(self) -> None:
    self.assertFalse(EmptyIterator)

  def test_full_iterator(self) -> None:
    self.assertTrue(FullIterator)

  def test_explicit_true(self) -> None:
    self.assertTrue(ExplicitTrue)

  def test_explicit_false(self) -> None:
    self.assertFalse(ExplicitFalse)

  def test_len_false(self) -> None:
    self.assertFalse(LenFalse)

  def test_len_true(self) -> None:
    self.assertTrue(LenTrue)

  def test_vintage_iterator_true(self) -> None:
    self.assertTrue(VintageIteratorTrue)

  def test_vintage_iterator_false(self) -> None:
    self.assertFalse(VintageIteratorFalse)

  def test_iterable(self) -> None:
    """Test that classes with __class_iter__ are iterable."""
    i = 8008135
    for i, _ in enumerate(VintageIteratorTrue):
      pass
    self.assertEqual(i, 2)  # Should iterate through 3 items (0, 1, 2)
    setattr(VintageIteratorFalse, '__iter_contents__', ['coverage', 'lol'])
    self.assertEqual(VintageIteratorFalse.__class_next__(), 'coverage')
    self.assertEqual(VintageIteratorFalse.__class_next__(), 'lol')
    with self.assertRaises(StopIteration):
      VintageIteratorFalse.__class_next__()

  def test_nuthing(self) -> None:
    """Test of nothing, nothing at all!"""

    class Foo:
      __slots__ = ('Tom', 'Dick', 'Harry')

    class Bar:
      __slots__ = ('never', 'gonna', 'give', 'you', 'up')

    with self.assertRaises(EZMultipleInheritance) as context:
      class Breh(Foo, Bar, metaclass=EZMeta):
        pass
    e = context.exception
    self.assertEqual(str(e), repr(e))

    with self.assertRaises(TypeError):
      class Yikes(Foo, Bar):
        pass
