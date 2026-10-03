"""
TestKeeFlagsMiss subclasses 'KeeTest' and pins that every miss on a
'KeeFlags' class raises 'KeeResolveError', by name, by index, by value,
among several identifiers and through a 'KeeBox', as every miss on a
'KeeNum' does, so one 'except' clause covers both enumerations. A name
miss used to raise 'KeyError' and a value miss 'ValueError', so a
fallback catching 'KeeResolveError' around a lookup caught an index miss
alone and let the other two escape.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.keenum import KeeFlags, KeeFlag, KeeBox
from worktoy.mcls import BaseObject
from worktoy.waitaminute.keenum import KeeResolveError

from . import KeeTest

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any


class Perm(KeeFlags):
  """
  Perm holds the three permission flags of a file.
  """

  READ = KeeFlag()
  WRITE = KeeFlag()
  EXEC = KeeFlag()


class Entry(BaseObject):
  """
  Entry holds the permission of a file, read from a config value.
  """

  perm = KeeBox[Perm]('read')


def permFromConfig(entry: Any) -> Perm:
  """
  Reads a permission from a config entry, falling back to NULL for
  anything the enumeration does not know.
  """
  try:
    return Perm[entry]
  except KeeResolveError:
    return Perm.NULL


class TestKeeFlagsMiss(KeeTest):
  """
  TestKeeFlagsMiss provides tests for the exception a miss on a flags
  class raises.
  """

  def test_name_miss(self) -> None:
    """An unknown name raises 'KeeResolveError' naming the class and the
    name, from a subscript and from a call alike."""
    with self.assertRaises(KeeResolveError) as context:
      _ = Perm['delete']
    self.assertIs(context.exception.keeNum, Perm)
    self.assertEqual(context.exception.identifier, 'delete')
    with self.assertRaises(KeeResolveError):
      Perm('delete')

  def test_index_miss(self) -> None:
    """An index past the members raises 'KeeResolveError'."""
    with self.assertRaises(KeeResolveError) as context:
      _ = Perm[99]
    self.assertEqual(context.exception.identifier, 99)

  def test_value_miss(self) -> None:
    """A value of no member raises 'KeeResolveError'."""
    with self.assertRaises(KeeResolveError) as context:
      Perm(3.5)
    self.assertIs(context.exception.keeNum, Perm)
    self.assertEqual(context.exception.identifier, 3.5)

  def test_miss_among_several(self) -> None:
    """A miss among several identifiers raises 'KeeResolveError' for the
    one that missed."""
    with self.assertRaises(KeeResolveError) as context:
      _ = Perm['read', 'delete']
    self.assertEqual(context.exception.identifier, 'delete')

  def test_box_miss(self) -> None:
    """A 'KeeBox' assigned a name of no member raises 'KeeResolveError'."""
    entry = Entry()
    self.assertIs(entry.perm, Perm.READ)
    with self.assertRaises(KeeResolveError):
      entry.perm = 'delete'
    self.assertIs(entry.perm, Perm.READ)

  def test_membership(self) -> None:
    """A miss of any kind reads as absent."""
    for identifier in ('delete', 99, 3.5, ('read', 'delete')):
      with self.subTest(identifier=identifier):
        self.assertNotIn(identifier, Perm)
    self.assertIn('read', Perm)
    self.assertIn(1, Perm)

  def test_one_except_clause(self) -> None:
    """A fallback catching 'KeeResolveError' covers every miss."""
    self.assertIs(permFromConfig('read'), Perm.READ)
    for entry in ('delete', 99, 3.5):
      with self.subTest(entry=entry):
        self.assertIs(permFromConfig(entry), Perm.NULL)
