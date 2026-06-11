"""
TestKeyBind tests the 'KeyBind' example: a regular class hosting 'KeeBox'
descriptors typed by a 'KeeNum' and a 'KeeFlags' enumeration.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from .examples import KeyBind, KeyboardModifier, KeyboardKeyNum

from . import KeeTest

if TYPE_CHECKING:  # pragma: no cover
  pass


class TestKeyBind(KeeTest):
  """
  TestKeyBind tests the traditional 'KeeBox' pattern through the
  'KeyBind' example: construction through every overload, rendering,
  and above all that the enum-typed attributes remain freely mutable
  while the enumerations themselves stay frozen.
  """

  def test_construction(self) -> None:
    """
    The docstring examples hold: each overload produces the promised
    rendering, and the flexible constructor accepts its two arguments
    in either order.
    """
    kb1 = KeyBind(KeyboardModifier.SHIFT, KeyboardKeyNum.A)
    self.assertEqual(str(kb1), 'SHIFT+A')
    self.assertIs(kb1.mod, KeyboardModifier.SHIFT)
    self.assertIs(kb1.key, KeyboardKeyNum.A)

    flipped = KeyBind(KeyboardKeyNum.A, KeyboardModifier.SHIFT)
    self.assertIs(flipped.mod, KeyboardModifier.SHIFT)
    self.assertIs(flipped.key, KeyboardKeyNum.A)

    kb2 = KeyBind(KeyboardKeyNum.B)
    self.assertEqual(str(kb2), 'B')
    self.assertIs(kb2.mod, KeyboardModifier.NULL)

    kb3 = KeyBind('CTRL+C')
    self.assertEqual(str(kb3), 'CTRL+C')
    self.assertIs(kb3.mod, KeyboardModifier.CTRL)
    self.assertIs(kb3.key, KeyboardKeyNum.C)

  def test_attributes_are_mutable(self) -> None:
    """
    The 'KeeBox' attributes accept new values after construction:
    members directly, names as strings, and several flag names as a
    tuple. Only the resolved member is ever stored.
    """
    kb = KeyBind(KeyboardModifier.SHIFT, KeyboardKeyNum.A)

    kb.mod = KeyboardModifier.CTRL
    kb.key = KeyboardKeyNum.D
    self.assertIs(kb.mod, KeyboardModifier.CTRL)
    self.assertIs(kb.key, KeyboardKeyNum.D)

    kb.mod = 'alt'
    kb.key = 'E'
    self.assertIs(kb.mod, KeyboardModifier.ALT)
    self.assertIs(kb.key, KeyboardKeyNum.E)

    kb.mod = ('ctrl', 'shift')
    self.assertIs(kb.mod, KeyboardModifier.CTRL_SHIFT)
    self.assertEqual(str(kb), 'CTRL_SHIFT+E')

  def test_enums_stay_frozen(self) -> None:
    """
    Mutating the 'KeyBind' attributes never touches the enumerations:
    the members keep their identities and the classes their members.
    """
    kb = KeyBind('CTRL+C')
    kb.mod = 'shift'
    kb.key = 'A'
    self.assertEqual(len(KeyboardModifier), 16)
    self.assertEqual(len(KeyboardKeyNum), 26)
    self.assertIs(KeyboardModifier('ctrl'), KeyboardModifier.CTRL)
    self.assertIs(KeyboardKeyNum('C'), KeyboardKeyNum.C)

  def test_default_construction(self) -> None:
    """
    The empty constructor leaves the modifier at the falsy 'NULL'
    member, so a 'KeyBind' renders without the separator once a key is
    set.
    """
    kb = KeyBind()
    kb.key = 'Q'
    self.assertIs(kb.mod, KeyboardModifier.NULL)
    self.assertEqual(str(kb), 'Q')

  def test_repr(self) -> None:
    """
    The representation mirrors the flexible constructor: key and
    modifier when one is held, the key alone otherwise.
    """
    kb = KeyBind(KeyboardModifier.META, KeyboardKeyNum.F)
    self.assertEqual(repr(kb), 'KeyBind(F, META)')
    self.assertEqual(repr(KeyBind(KeyboardKeyNum.G)), 'KeyBind(G)')
