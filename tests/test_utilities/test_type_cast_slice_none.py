"""
TestTypeCastSliceNone subclasses 'UtilitiesTest' and pins that 'slice'
is no cast target: a slice passes unchanged, while 'None', an index and
a list of components are refused, so an overloaded '__getitem__' refuses
'x[None]' as a list does and answers a real slice. The cast used to
accept 'None' because 'slice(None)' is a valid slice, so an overloaded
'__getitem__' answered 'x[None]' with everything.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.dispatch import overload
from worktoy.mcls import BaseObject
from worktoy.utilities import typeCast
from worktoy.waitaminute.dispatch import DispatchException
from worktoy.waitaminute.dispatch import TypeCastException

from . import UtilitiesTest


class Playlist(BaseObject):
  """Playlist overloads subscripts on 'int' and 'slice'."""

  songs = ['a', 'b', 'c']

  @overload(int)
  def __getitem__(self, index: int) -> str:
    return self.songs[index]

  @overload(slice)
  def __getitem__(self, index: slice) -> list:
    return self.songs[index]


class Tolerant(Playlist):
  """Tolerant declares what 'None' means for it."""

  @overload(type(None))
  def __getitem__(self, index: None) -> str:
    return 'none'


class TestTypeCastSliceNone(UtilitiesTest):
  """
  TestTypeCastSliceNone provides tests for 'None' and the slice cast.
  """

  def test_none_refused(self) -> None:
    """A lone 'None' is refused."""
    with self.assertRaises(TypeCastException):
      typeCast(slice, None)

  def test_components_refused(self) -> None:
    """A list or tuple of components and a lone index are refused, since
    nothing but a slice is a slice."""
    for value in ([None, 3], (1, None), 2):
      with self.subTest(value=value):
        with self.assertRaises(TypeCastException):
          typeCast(slice, value)

  def test_slice_unchanged(self) -> None:
    """A slice, 'slice(None)' included, passes as it is."""
    full = slice(None)
    self.assertIs(typeCast(slice, full), full)

  def test_subscript_refused(self) -> None:
    """An overloaded '__getitem__' refuses 'x[None]' as a list does,
    while every other subscript still answers."""
    playlist = Playlist()
    with self.assertRaises(DispatchException):
      _ = playlist[None]
    self.assertEqual(playlist[1], 'b')
    self.assertEqual(playlist[1:], ['b', 'c'])

  def test_declared_none_answers(self) -> None:
    """A class declaring '@overload(type(None))' still answers it."""
    self.assertEqual(Tolerant()[None], 'none')
