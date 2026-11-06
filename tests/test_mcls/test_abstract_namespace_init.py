"""
TestAbstractNamespaceInit tests the construction and the text of
'AbstractNamespace' from 'worktoy.mcls'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.mcls import AbstractNamespace, BaseMeta, BaseSpace, BaseObject
from worktoy.utilities import resolveMRO
from . import MclsTest, LoggingHook, LoggedSpace, LoggedMeta, Roster


class TestAbstractNamespaceInit(MclsTest):
  """
  A namespace learns the metaclass, name, bases and keywords of the
  class it serves before the body runs, computes the resolution order
  of the bases, and runs every hook's 'preparePhase'. The tests pin what
  it keeps, the order and the lookup order with and without a
  consistent resolution order, and the two texts.
  """

  def test_keeps_what_it_is_given(self) -> None:
    space = BaseSpace(BaseMeta, 'A', (Roster,), tag=1)
    self.assertIs(space.getMetaclass(), BaseMeta)
    self.assertEqual(space.getClassName(), 'A')
    self.assertEqual(space.getBases(), (Roster,))
    self.assertIsInstance(space.getBases(), tuple)
    self.assertEqual(space.getKwargs(), {'tag': 1})
    space.getKwargs()['tag'] = 2
    self.assertEqual(space.getKwargs(), {'tag': 1})
    self.assertEqual(BaseSpace(BaseMeta, 'A', ()).getKwargs(), {})
    self.assertEqual(space.getShadowSpace(), {})
    self.assertEqual(space.getClaimedDeletions(), ())
    self.assertEqual(dict(space), {})

  def test_resolution_order(self) -> None:
    space = BaseSpace(BaseMeta, 'A', (Roster,))
    self.assertEqual(space.getMRO(), resolveMRO(Roster))
    self.assertEqual(space.getMRO(), [*Roster.__mro__])
    order = space._getLookupOrder()
    self.assertEqual(order, space.getMRO())
    self.assertIsNot(order, space.getMRO())
    self.assertEqual(BaseSpace(BaseMeta, 'A', ()).getMRO(), [])

  def test_inconsistent_order_refused(self) -> None:
    class A:
      pass

    class B(A):
      pass

    with self.assertRaises(TypeError) as context:
      BaseSpace(BaseMeta, 'X', (A, B))
    self.assertIn('cannot form a consistent mro', str(context.exception))
    loose = BaseSpace(BaseMeta, 'X', (A, B), _strictMRO=False)
    self.assertIsNone(loose.getMRO())
    self.assertEqual(loose._getLookupOrder(), [A, object, B])
    strict = BaseSpace(BaseMeta, 'X', (B, A), _strictMRO=True)
    self.assertEqual(strict.getMRO(), [B, A, object])

  def test_prepare_phase_runs(self) -> None:
    LoggingHook.log.clear()
    LoggedSpace(LoggedMeta, 'A', ())
    self.assertEqual(LoggingHook.log, [('prepare', 'A')])

  def test_str(self) -> None:
    space = BaseSpace(BaseMeta, 'A', (Roster, BaseObject))
    text = str(space)
    self.assertIn("type: 'BaseSpace'", text)
    self.assertIn("metaclass: 'BaseMeta'", text)
    self.assertIn('bases: (Roster, BaseObject)', text)
    self.assertIn("class: 'A'", text)
    self.assertEqual(str(BaseObject.__namespace__),
                     str(BaseObject.getNamespace()))

  def test_repr(self) -> None:
    plain = BaseSpace(BaseMeta, 'A', (Roster,))
    self.assertEqual(repr(plain), "BaseSpace(BaseMeta, 'A', (Roster))")
    bare = AbstractNamespace(BaseMeta, 'A', ())
    self.assertEqual(repr(bare), "AbstractNamespace(BaseMeta, 'A', ())")
    keyed = BaseSpace(BaseMeta, 'A', (Roster,), tag=1, flag=True)
    self.assertEqual(repr(keyed),
                     "BaseSpace(BaseMeta, 'A', (Roster), tag=1, flag=True)")

  def test_random_names(self) -> None:
    self.randomWord.size = 6
    for word in self.randomWord.row:
      space = BaseSpace(BaseMeta, word, ())
      with self.subTest(word=word):
        self.assertEqual(space.getClassName(), word)
        self.assertEqual(repr(space), "BaseSpace(BaseMeta, '%s', ())" % word)
