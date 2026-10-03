"""
TestKeeMetaRootInit subclasses 'KeeTest' and pins that the root a custom
'KeeMeta' builds through its 'keeNum' descriptor is prepared and
initialised by that metaclass, as any of its enumerations is. The root
used to be built by '__new__' alone, on a namespace made directly rather
than by '__prepare__', so a metaclass customising either never saw it.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.keenum import KeeMeta, KeeSpace, Kee

from . import KeeTest

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any

inits = []
prepared = []


class FontSpace(KeeSpace):
  """FontSpace is the namespace 'FontMeta' prepares."""


class FontMeta(KeeMeta):
  """FontMeta records the classes it prepares and initialises."""

  @classmethod
  def __prepare__(mcls, name: str, bases: tuple, **kwargs) -> FontSpace:
    prepared.append(name)
    return FontSpace(mcls, name, bases, **kwargs)

  def __init__(cls, *args, **kwargs) -> None:
    inits.append(cls.__name__)
    KeeMeta.__init__(cls, *args, **kwargs)


class TestKeeMetaRootInit(KeeTest):
  """
  TestKeeMetaRootInit provides tests for the root of a custom 'KeeMeta'.
  """

  def test_root_prepared_and_initialised(self) -> None:
    """The root goes through the '__prepare__' and '__init__' of the
    metaclass, and is its own base."""
    root = FontMeta.keeNum
    self.assertIn(root.__name__, prepared)
    self.assertIn(root.__name__, inits)
    self.assertIsInstance(root.__namespace__, FontSpace)
    self.assertIs(root.base, root)
    self.assertIs(FontMeta.keeNum, root)

  def test_enumeration_of_root(self) -> None:
    """An enumeration based on the root works as before."""

    class Font(FontMeta.keeNum):
      ARIAL = Kee[int](1)

    self.assertIs(Font(1), Font.ARIAL)
    self.assertIn('Font', inits)
