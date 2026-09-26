"""
TestCustomKeeMetaBase subclasses 'KeeTest' from the 'tests.test_keenum'
package and pins that 'base' and 'mroNum' behave the same under a custom
subclass of 'KeeMeta' as under 'KeeMeta' itself. The root class a custom
metaclass builds through 'keeNum' carries another name, 'FontMetaNum'
for 'FontMeta', so telling the root apart by the name 'KeeNum' fails for
it, and wrongly succeeds for a user enumeration that happens to be named
'KeeNum'. The root is the class built by 'keeNum', whatever its name.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy import keenum
from worktoy.keenum import KeeNum, Kee, KeeMeta

from . import KeeTest


class Plain(KeeNum):
  """Plain is a direct child of the 'KeeNum' root."""

  X = Kee[int](1)


class PlainChild(Plain):
  """PlainChild extends 'Plain'."""

  Y = Kee[int](2)


class FontMeta(KeeMeta):
  """FontMeta is a custom metaclass for enumerations."""


class FontNum(FontMeta.keeNum):
  """FontNum is a direct child of the root built by 'FontMeta'."""

  ARIAL = Kee[int](1)


class MoreFont(FontNum):
  """MoreFont extends 'FontNum'."""

  TIMES = Kee[int](2)


class TestCustomKeeMetaBase(KeeTest):
  """
  TestCustomKeeMetaBase provides tests for 'base' and 'mroNum' on
  enumerations built by a custom subclass of 'KeeMeta'.
  """

  def test_custom_root(self) -> None:
    """
    The root built by 'FontMeta.keeNum' is its own base and has an empty
    'mroNum', exactly as 'KeeNum' does.
    """
    for root in (KeeNum, FontMeta.keeNum):
      with self.subTest(root=root.__name__):
        self.assertIs(root.base, root)
        self.assertEqual(root.mroNum, ())

  def test_same_shape_as_kee_num(self) -> None:
    """
    A direct child of either root is its own base, and a grandchild
    names the child as its base and as its whole 'mroNum'.
    """
    chains = ((Plain, PlainChild), (FontNum, MoreFont))
    for child, grandchild in chains:
      with self.subTest(child=child.__name__):
        self.assertIs(child.base, child)
        self.assertEqual(child.mroNum, ())
        self.assertIs(grandchild.base, child)
        self.assertEqual(grandchild.mroNum, (child,))

  def test_enumeration_named_kee_num(self) -> None:
    """
    A user enumeration that happens to be named 'KeeNum' is an ordinary
    enumeration: it is a direct child of the root, and a subclass of it
    names it as its base.
    """

    class KeeNum(keenum.KeeNum):
      X = Kee[int](1)

    class Child(KeeNum):
      Y = Kee[int](2)

    self.assertIs(KeeNum.base, KeeNum)
    self.assertIs(Child.base, KeeNum)
    self.assertEqual(Child.mroNum, (KeeNum,))
