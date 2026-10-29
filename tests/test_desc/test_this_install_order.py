"""
TestThisInstallOrder pins where 'THIS[Parent]' installs its
'__init_subclass__' and how the hooks hand over to one another: the hook
goes on the parent named, whichever base of it took one before, and a
hook a base takes after its subclass took one is still reached, through
the subclass's hook. So the descriptors a class body records on
'Parent' land on the class being created whatever order the parents were
named in across class bodies, and a parent keeps an '__init_subclass__'
of its own. The decorations are written as calls after the 'def', the
spelling that works on Python 3.7 and 3.8 as well.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.core.sentinels import THIS
from worktoy.desc import AttriBox
from worktoy.mcls import BaseObject

from . import DescTest


class TestThisInstallOrder(DescTest):
  """
  TestThisInstallOrder provides tests for the order in which parents take
  the '__init_subclass__' of 'THIS'.
  """

  def test_child_hook_beside_base_hook(self) -> None:
    """A base that took the hook first does not stop its subclass from
    taking one of its own: 'THIS[Sub].x' in the body of a subclass of 'Sub'
    places the clone on that body's class, and leaves no record behind on
    'Sub' for a sibling defined later."""

    class Base(BaseObject):
      x = AttriBox[int](1)

    class Sub(Base):
      pass

    class FromBase(Base):
      def _onGetBase(self, value: int) -> None:
        self.baseSaw = value

      _onGetBase = THIS[Base].x.onGet(_onGetBase)

    class FromSub(Sub):
      def _onGetSub(self, value: int) -> None:
        self.subSaw = value

      _onGetSub = THIS[Sub].x.onGet(_onGetSub)

    self.assertIn('__init_subclass__', Base.__dict__)
    self.assertIn('__init_subclass__', Sub.__dict__)
    self.assertIn('x', FromSub.__dict__)
    self.assertIsNot(FromSub.__dict__['x'], Base.__dict__['x'])
    self.assertEqual(FromSub.__dict__['x']._getOnGetKeys(), ('_onGetSub',))
    self.assertIs(FromSub.__dict__['x'].getFieldOwner(), FromSub)
    self.assertNotIn('__new_descriptors__', Sub.__dict__)
    self.assertNotIn('__new_descriptors__', Base.__dict__)
    self.assertNotIn('x', Sub.__dict__)
    self.assertEqual(Base.__dict__['x']._getOnGetKeys(), ())
    fromSub = FromSub()
    self.assertEqual(fromSub.x, 1)
    self.assertEqual(fromSub.subSaw, 1)
    fromBase = FromBase()
    self.assertEqual(fromBase.x, 1)
    self.assertEqual(fromBase.baseSaw, 1)

    class Later(Sub):
      pass

    self.assertNotIn('x', Later.__dict__)

  def test_base_hook_taken_later_still_runs(self) -> None:
    """A hook a base takes after its subclass took one is reached through
    the subclass's hook, so the body of a subclass of it may name
    the base, under a plain metaclass too."""

    class Base:
      x = AttriBox[int](3)

    class Sub(Base):
      pass

    class FromSub(Sub):
      def _onGetSub(self, value: int) -> None:
        self.subSaw = value

      _onGetSub = THIS[Sub].x.onGet(_onGetSub)

    class FromBase(Base):
      def _onGetBase(self, value: int) -> None:
        self.baseSaw = value

      _onGetBase = THIS[Base].x.onGet(_onGetBase)

    class NamesBase(Sub):
      def _onGetNamesBase(self, value: int) -> None:
        self.namesBaseSaw = value

      _onGetNamesBase = THIS[Base].x.onGet(_onGetNamesBase)

    self.assertIn('x', NamesBase.__dict__)
    self.assertEqual(NamesBase.__dict__['x']._getOnGetKeys(), ('_onGetNamesBase',))
    self.assertIs(NamesBase.__dict__['x'].getFieldOwner(), NamesBase)
    self.assertNotIn('__new_descriptors__', Base.__dict__)
    self.assertNotIn('__new_descriptors__', Sub.__dict__)
    self.assertNotIn('x', Sub.__dict__)
    self.assertEqual(Base.__dict__['x']._getOnGetKeys(), ())
    namesBase = NamesBase()
    self.assertEqual(namesBase.x, 3)
    self.assertEqual(namesBase.namesBaseSaw, 3)
    fromSub = FromSub()
    self.assertEqual(fromSub.x, 3)
    self.assertEqual(fromSub.subSaw, 3)

    class Later(Base):
      pass

    self.assertNotIn('x', Later.__dict__)

  def test_own_init_subclass_kept(self) -> None:
    """A parent with an '__init_subclass__' of its own keeps it: the hook
    runs it first, with the class keywords, and places the clone after."""
    seen = []

    class Base(BaseObject):
      x = AttriBox[int](5)

      @classmethod
      def __init_subclass__(cls, **kwargs) -> None:
        seen.append((cls.__name__, kwargs.get('tag', None)))
        super().__init_subclass__(**kwargs)

    class Child(Base, tag='child'):
      def _onGetChild(self, value: int) -> None:
        self.childSaw = value

      _onGetChild = THIS[Base].x.onGet(_onGetChild)

    self.assertEqual(seen, [('Child', 'child')])
    self.assertIn('x', Child.__dict__)
    self.assertEqual(Child.__dict__['x']._getOnGetKeys(), ('_onGetChild',))
    self.assertNotIn('__new_descriptors__', Base.__dict__)
    child = Child()
    self.assertEqual(child.x, 5)
    self.assertEqual(child.childSaw, 5)

    class Plain(Base, tag='plain'):
      pass

    self.assertEqual(seen, [('Child', 'child'), ('Plain', 'plain')])
    self.assertNotIn('x', Plain.__dict__)
