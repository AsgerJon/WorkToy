"""
TestThisNotifiers subclasses 'DescTest' and pins that a class body may
expand on the notifiers of a descriptor it inherits by decorating it
through 'THIS', naming the base that holds the descriptor:
'THIS[Parent].x.onGet' in the body of 'Child' decorates 'x' as 'Child'
will hold it. 'THIS[Parent].x' is a deferred reference to the descriptor
'x' that 'Parent' holds. Reading it takes a clone of 'Parent.x' at once,
recorded on 'Parent', and the same clone again for every further
reference to 'x' in the body, so the roles stack. The role decorators of
the reference, 'preGet', 'onGet', 'preSet', 'onSet', 'preDelete',
'onDelete' and 'setName', apply to that clone and hand the function back
as the descriptor's own decorators do; any other name, 'SET' on a
'Field', reaches the clone itself. 'Parent' takes an '__init_subclass__'
that places the recorded clones on the subclass as it is created, names
them there and forgets them, so a sibling defined later takes no clone,
and 'Parent.x' is never touched. The clone derives the storage name of
the base's descriptor, so an instance holds one slot for the field. The
mechanism needs no worktoy metaclass: a parent built by 'type' that owns
a box serves the same way. A name 'Parent' does not hold is refused at
the line with 'DanglingAlias', a role the descriptor lacks is a plain
'AttributeError'.

A decorator may hold a subscript only from Python 3.9 on (PEP 614), so
this module writes the decoration as a call after the 'def',
'f = THIS[Parent].x.onGet(f)', which every supported version runs; the
'@THIS[Parent].x.onGet' form lives in '_this_bound_helpers.py', imported
here on 3.9 and later alone.

Decorating 'Parent.x' directly from a subclass body registers on the
parent's descriptor, which is what that line says; 'THIS' is the way to
say the child's. A descriptor of the class's own body is decorated
directly, '@y.onGet', since the class does not exist yet to be named.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

import pickle
import sys
from unittest import skipIf

from worktoy.core.sentinels import THIS, Sentinel
from worktoy.desc import AttriBox, Field
from worktoy.dispatch import isFlex
from worktoy.mcls import BaseObject
from worktoy.waitaminute import TypeException
from worktoy.waitaminute.desc import ReadOnlyError, DanglingAlias
from worktoy.waitaminute.desc import NamelessCallback

from . import DescTest

if sys.version_info >= (3, 9):
  from ._this_bound_helpers import makeBound


class Parent(BaseObject):
  """Parent holds the descriptors the children expand on."""

  x = AttriBox[int](1)
  v = Field()

  @v.GET
  def _getV(self) -> int:
    return 42

  @x.onGet
  def _onGetParent(self, value: int) -> None:
    self.parentSaw = value


class Child(Parent):
  """Child adds notifiers to the inherited descriptors through THIS."""

  def _onGetX(self, value: int) -> None:
    self.lastRead = value

  _onGetX = THIS[Parent].x.onGet(_onGetX)

  def _preSetX(self, value: int) -> None:
    self.lastWrite = value

  _preSetX = THIS[Parent].x.preSet(_preSetX)

  def _setV(self, value: int) -> None:
    self.vSet = value

  _setV = THIS[Parent].v.SET(_setV)


class Sibling(Parent):
  """Sibling is defined after Child and names nothing through THIS."""


class PlainParent:
  """PlainParent is built by 'type' and has no worktoy base."""

  z = AttriBox[int](3)


class PlainChild(PlainParent):
  """PlainChild expands on an inherited box under a plain metaclass."""

  def _onGetZ(self, value: int) -> None:
    self.zSeen = value

  _onGetZ = THIS[PlainParent].z.onGet(_onGetZ)


class TestThisNotifiers(DescTest):
  """
  TestThisNotifiers provides tests for decorating inherited descriptors
  through THIS.
  """

  @staticmethod
  def _makeLocalParent() -> type:
    """A parent of its own for the tests that read a reference outside
    a class body, which records a clone on the parent named."""

    class Local(BaseObject):
      x = AttriBox[int](7)

    return Local

  def test_parent_untouched(self) -> None:
    """The parent reads, writes and refuses exactly as before, and keeps
    no record of the clones its children took."""
    parent = Parent()
    self.assertEqual(parent.x, 1)
    self.assertEqual(parent.parentSaw, 1)
    self.assertFalse(hasattr(parent, 'lastRead'))
    self.assertEqual(parent.v, 42)
    with self.assertRaises(ReadOnlyError):
      parent.v = 1
    self.assertEqual(Parent.__dict__['x']._getOnGetKeys(), ('_onGetParent',))
    self.assertEqual(Parent.__dict__['x']._getPreSetKeys(), ())
    self.assertEqual(Parent.__dict__['v']._getSetterKeys(), ())
    self.assertNotIn('__new_descriptors__', Parent.__dict__)

  def test_child_notified(self) -> None:
    """The child's callbacks fire beside the inherited ones, on read and
    on write, and the 'Field' takes the setter."""
    child = Child()
    self.assertEqual(child.x, 1)
    self.assertEqual(child.lastRead, 1)
    self.assertEqual(child.parentSaw, 1)
    child.x = 5
    self.assertEqual(child.lastWrite, 5)
    self.assertEqual(child.x, 5)
    child.v = 3
    self.assertEqual(child.vSet, 3)
    self.assertEqual(child.v, 42)

  def test_child_holds_its_own_clone(self) -> None:
    """The child holds a clone under the field name, carrying the parent's
    keys and its own, placed and named as the class was created, and the
    functions sit under their names as the decorators returned them."""
    self.assertIsNot(Child.__dict__['x'], Parent.__dict__['x'])
    self.assertIsInstance(Child.__dict__['x'], AttriBox)
    self.assertEqual(Child.__dict__['x']._getOnGetKeys(), ('_onGetParent', '_onGetX'))
    self.assertEqual(Child.__dict__['x']._getPreSetKeys(), ('_preSetX',))
    self.assertIs(Child.__dict__['x'].getFieldOwner(), Child)
    self.assertEqual(Child.__dict__['x'].getFieldName(), 'x')
    self.assertIsInstance(Child.__dict__['v'], Field)
    self.assertIsNot(Child.__dict__['v'], Parent.__dict__['v'])
    self.assertEqual(Child.__dict__['v']._getSetterKeys(), ('_setV',))
    self.assertTrue(isFlex(Child.__dict__['_onGetX']))
    self.assertTrue(isFlex(Child.__dict__['_preSetX']))
    self.assertTrue(callable(Child.__dict__['_setV']))

  def test_sibling_takes_no_clone(self) -> None:
    """A sibling defined after the decorating child inherits the parent's
    descriptors as they are."""
    self.assertNotIn('x', Sibling.__dict__)
    self.assertNotIn('v', Sibling.__dict__)
    sibling = Sibling()
    self.assertEqual(sibling.x, 1)
    self.assertEqual(sibling.parentSaw, 1)
    self.assertFalse(hasattr(sibling, 'lastRead'))

  def test_clone_shares_storage(self) -> None:
    """The clone derives the parent's storage name, so an instance holds
    one slot for the field."""
    child = Child()
    child.x = 9
    keys = [k for k in vars(child) if k.endswith('_field_object__')]
    self.assertEqual(keys, ['__x__attribox_field_object__'])
    self.assertEqual(child.x, 9)

  def test_plain_metaclass(self) -> None:
    """The mechanism needs no worktoy metaclass and no 'Object' base: the
    clone is placed on the subclass as it is created, and the first read
    through it is notified."""
    self.assertIn('z', PlainChild.__dict__)
    self.assertIsNot(PlainChild.__dict__['z'], PlainParent.__dict__['z'])
    self.assertEqual(PlainChild.__dict__['z']._getOnGetKeys(), ('_onGetZ',))
    self.assertEqual(PlainParent.__dict__['z']._getOnGetKeys(), ())
    self.assertNotIn('__new_descriptors__', PlainParent.__dict__)
    plain = PlainChild()
    self.assertEqual(plain.z, 3)
    self.assertEqual(plain.zSeen, 3)

  def test_roles_stack(self) -> None:
    """Two references to one descriptor stacked on one function give it
    both roles on the child's one clone, the base untouched."""

    class Stacked(Parent):
      def _watchX(self, value: int) -> None:
        self.watched = value

      _watchX = THIS[Parent].x.onGet(_watchX)
      _watchX = THIS[Parent].x.preSet(_watchX)

    self.assertEqual(Stacked.__dict__['x']._getOnGetKeys(), ('_onGetParent', '_watchX'))
    self.assertEqual(Stacked.__dict__['x']._getPreSetKeys(), ('_watchX',))
    self.assertEqual(Parent.__dict__['x']._getPreSetKeys(), ())
    self.assertTrue(isFlex(Stacked.__dict__['_watchX']))
    stacked = Stacked()
    self.assertEqual(stacked.x, 1)
    self.assertEqual(stacked.watched, 1)
    stacked.x = 4
    self.assertEqual(stacked.watched, 4)

  def test_dangling_refused_at_the_line(self) -> None:
    """A name the parent does not hold is refused by the reference itself,
    so a class body fails at that line."""
    Local = self._makeLocalParent()
    with self.assertRaises(DanglingAlias) as context:
      _ = THIS[Local].nothing
    self.assertIn('nothing', str(context.exception))
    with self.assertRaises(DanglingAlias) as context:
      class Bad(Local):
        def _onGetNothing(self, value: int) -> None:
          pass

        _onGetNothing = THIS[Local].nothing.onGet(_onGetNothing)
    self.assertIn('nothing', str(context.exception))

  def test_missing_role_is_attribute_error(self) -> None:
    """A role the descriptor lacks is a plain 'AttributeError': a name
    that is no role at all, and 'GET' on a box."""
    Local = self._makeLocalParent()
    with self.assertRaises(AttributeError) as context:
      _ = THIS[Local].x.onFrobnicate
    self.assertIn('onFrobnicate', str(context.exception))
    with self.assertRaises(AttributeError) as context:
      _ = THIS[Local].x.GET
    self.assertIn('GET', str(context.exception))

  def test_decorator_hands_the_function_back(self) -> None:
    """A role decorator returns what the descriptor's own decorator
    returns, the callback wrapped by 'flexCall', and leaves the function
    itself without a mark; a nameless callback is refused at the line."""
    Local = self._makeLocalParent()

    class Holder(Local):
      def _hook(self, value: int) -> None:
        pass

      wrapped = THIS[Local].x.onGet(_hook)
      assert isFlex(wrapped)
      assert wrapped.__wrapped__ is _hook
      assert vars(_hook) == {}
      _hook = wrapped
      del wrapped

    self.assertEqual(Holder.__dict__['x']._getOnGetKeys(), ('_hook',))
    with self.assertRaises(NamelessCallback):
      THIS[Local].x.onGet(lambda self, value: None)

  @skipIf(sys.version_info < (3, 9), 'a decorator holds a subscript only from 3.9 on')
  def test_bound_reference(self) -> None:
    """The decorator form works as the call form does."""
    Bound = makeBound(Parent)
    bound = Bound()
    self.assertEqual(bound.x, 1)
    self.assertEqual(bound.boundSaw, 1)
    self.assertEqual(bound.parentSaw, 1)
    self.assertIsNot(Bound.__dict__['x'], Parent.__dict__['x'])
    self.assertEqual(Bound.__dict__['x']._getOnGetKeys(), ('_onGetParent', '_onGetBound'))

  def test_subscript_takes_a_class(self) -> None:
    """THIS is subscripted with a class and nothing else."""
    with self.assertRaises(TypeException):
      _ = THIS[5]

  def test_this_itself_unchanged(self) -> None:
    """THIS stays the sentinel class: a 'Sentinel', picklable by
    reference, answering no attribute of its own."""
    self.assertTrue(issubclass(THIS, Sentinel))
    self.assertIs(pickle.loads(pickle.dumps(THIS)), THIS)
    self.assertEqual(THIS.__name__, 'THIS')
    self.assertFalse(hasattr(THIS, '__no_such_dunder__'))
