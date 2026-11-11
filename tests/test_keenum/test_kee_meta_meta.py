"""
TestKeeMetaMeta tests 'KeeMetaMeta' from 'worktoy.keenum'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.core import MetaType
from worktoy.keenum import KeeMetaMeta, KeeMeta, KeeNum, KeeBase, Kee
from . import KeenumTest


class TestKeeMetaMeta(KeenumTest):
  """
  'KeeMetaMeta' gives every metaclass based on 'KeeMeta' a root
  enumeration of its own through 'keeNum', built on first access and
  cached. The tests pin the root of 'KeeMeta' itself, the root a
  subclass metaclass builds, the cache, the reset on subclassing and
  the peek of the getter.
  """

  def test_kee_num_is_the_cached_root(self) -> None:
    self.assertIs(type(KeeMeta), KeeMetaMeta)
    self.assertIsSubclass(KeeMetaMeta, MetaType)
    self.assertIs(KeeMeta.keeNum, KeeNum)
    self.assertIs(KeeMeta.__kee_num__, KeeNum)
    self.assertIs(type(KeeNum), KeeMeta)
    self.assertIs(KeeNum.base, KeeNum)
    self.assertEqual(KeeNum.__doc__, KeeBase.__doc__)
    self.assertEqual(KeeNum.__name__, 'KeeNum')
    self.assertIsSubclass(KeeNum, KeeBase)
    self.assertEqual(len(KeeNum), 0)

  def test_subclass_metaclass_builds_its_own_root(self) -> None:
    class TempoMeta(KeeMeta):
      pass

    self.assertIsNone(TempoMeta.__kee_num__)
    with self.assertRaises(RecursionError) as context:
      TempoMeta._getKeeNum(_recursion=True)
    self.assertEqual(context.exception.args, ())
    root = TempoMeta.keeNum
    self.assertIs(TempoMeta.keeNum, root)
    self.assertIs(TempoMeta.__kee_num__, root)
    self.assertIsNot(root, KeeNum)
    self.assertEqual(root.__name__, 'TempoMetaNum')
    self.assertIs(type(root), TempoMeta)
    self.assertIs(root.base, root)
    self.assertEqual(root.mroNum, ())
    self.assertEqual(root.__doc__, KeeBase.__doc__)
    self.assertIs(KeeMeta.keeNum, KeeNum)

    class Font(TempoMeta.keeNum):
      ARIAL = Kee[int](1)

    self.assertIs(type(Font), TempoMeta)
    self.assertIs(Font.base, Font)
    self.assertIsInstance(Font.ARIAL, root)
    self.assertEqual(str(Font), "<TempoMetaNum 'Font': 1 member>")
    self.assertEqual(str(Font.ARIAL), '<Font>.ARIAL')

    class Bold(Font):
      pass

    self.assertEqual(str(Font.ARIAL), '<TempoMetaNum>.ARIAL')

  def test_descriptor_through_the_class(self) -> None:
    self.assertIs(type(KeeMetaMeta.__dict__['keeNum']).__name__, 'Field')
    self.assertIs(KeeMetaMeta.keeNum, KeeMetaMeta.__dict__['keeNum'])

  def test_root_named_after_any_metaclass(self) -> None:
    class AbcMeta(KeeMeta):
      pass

    class ZedMeta(KeeMeta):
      pass

    self.assertEqual(AbcMeta.keeNum.__name__, 'AbcMetaNum')
    self.assertEqual(ZedMeta.keeNum.__name__, 'ZedMetaNum')
    self.assertEqual(KeeMeta.keeNum.__name__, 'KeeNum')
