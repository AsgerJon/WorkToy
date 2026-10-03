"""
TestNoPickleClasses subclasses 'UtilitiesTest' from the
'tests.test_utilities' package and pins that the objects of every class
'worktoy' defines refuse the pickle protocol, while 'copy.copy' and
'copy.deepcopy' keep working on them. An enumeration member and a box are
each its own copy. Classes themselves are pickled by
name alone, which rebuilds nothing, and the sentinels are never
instantiated, so neither is covered.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

import copy
import pickle
from typing import TypeVar

from worktoy import core, desc, dispatch, ezdata, keenum, lorem_ipsum
from worktoy import mcls, utilities, work_test
from worktoy.core import Object, ContextInstance, ContextOwner
from worktoy.core.sentinels import ARGS, Sentinel
from worktoy.desc import AttriBox, FixBox, FastBox, Field, Alias
from worktoy.desc import BaseDescriptor, SymbolicName
from worktoy.dispatch import TypeSig, Dispatcher, CallMeMaybe, Permuter
from worktoy.dispatch import PermuterMethod, overload
from worktoy.ezdata import EZData, EZField, EZStore
from worktoy.keenum import KeeNum, Kee, KeeFlags, KeeFlag, KeeBox
from worktoy.lorem_ipsum import Sentence, StochasticWord, GaussianLengths
from worktoy.mcls import BaseObject, BaseMeta
from worktoy.mcls.space_hooks import NamespaceHook, SpaceDesc
from worktoy.mcls.space_hooks import ReservedNames
from worktoy.utilities import NoPickle, QuickDesc, Directory, ValidSlice
from worktoy.utilities import ExceptionInfo
from worktoy.utilities.combinatorics import Arrangement, Arrangements
from worktoy.waitaminute import PickleException
from worktoy.waitaminute.control_flow import ControlSpace, MetaFlow
from worktoy.work_test import BaseTest, SubTest, ComplexMixin
from worktoy.work_test.samplers import IntSampler

from . import UtilitiesTest

T = TypeVar('T')


class Day(KeeNum):
  """Day provides the enumeration members below."""

  MON = Kee[str]('mon')
  TUE = Kee[str]('tue')


class Perm(KeeFlags):
  """Perm provides the flags members below."""

  READ = KeeFlag()
  WRITE = KeeFlag()


class Point(EZData):
  """Point is a plain EZData class."""

  x = EZField[int](0)


class Frozen(EZData, frozen=True):
  """Frozen is a frozen EZData class."""

  x = EZField[int](0)


class Holder(BaseObject):
  """Holder is a 'BaseObject' with a box and an overloaded method."""

  items = AttriBox[list]()

  @overload(int)
  def twice(self, value: int) -> int:
    return value * 2


class Complex(ComplexMixin):
  """Complex mixes 'ComplexMixin' into a plain class."""


def _function(*args) -> tuple:
  """A plain function for the callable wrappers."""
  return args


def _instances() -> dict:
  """One instance of every class with instances, by label."""
  holder = Holder()
  holder.items.append(1)
  return {
    'Object'         : Object(),
    'BaseObject'     : holder,
    'ContextInstance': ContextInstance(),
    'ContextOwner'   : ContextOwner(),
    'ARGS'           : ARGS[int],
    'AttriBox'       : AttriBox[int](1),
    'FixBox'         : FixBox[int](1),
    'FastBox'        : FastBox[int](1),
    'Field'          : Field(),
    'Alias'          : Alias('items'),
    'BaseDescriptor' : BaseDescriptor(),
    'SymbolicName'   : SymbolicName('a', 'b'),
    '_RootAlias'     : AttriBox[T],
    'TypeSig'        : TypeSig(int),
    'Dispatcher'     : Dispatcher(),
    'CallMeMaybe'    : CallMeMaybe(_function),
    'Permuter'       : Permuter(_function),
    'PermuterMethod' : PermuterMethod(_function),
    'overload'       : overload.fallback(_function),
    'EZData'         : Point(1),
    'EZData frozen'  : Frozen(1),
    'EZField'        : EZField[int](1),
    'EZStore'        : EZStore('x'),
    'Kee'            : Kee[int](1),
    'KeeFlag'        : KeeFlag(),
    'KeeBox'         : KeeBox[Day]('mon'),
    'Sentence'       : Sentence(20),
    'StochasticWord' : StochasticWord(),
    'GaussianLengths': GaussianLengths(40, 15, 12, 70),
    'BaseSpace'      : BaseMeta.__prepare__('Foo', ()),
    'ControlSpace'   : ControlSpace(MetaFlow, 'Foo', ()),
    'NamespaceHook'  : NamespaceHook(),
    'SpaceDesc'      : SpaceDesc(),
    'ReservedNames'  : ReservedNames(),
    'QuickDesc'      : QuickDesc('__x__'),
    'Directory'      : Directory(),
    'ExceptionInfo'  : ExceptionInfo(ValueError),
    'Arrangement'    : Arrangement(('a', 'b'), (1, 0)),
    'Arrangements'   : Arrangements('a', 'b'),
    'BaseTest'       : BaseTest(),
    'SubTest'        : SubTest(),
    'ComplexMixin'   : Complex(1, 2),
    'IntSampler'     : IntSampler(),
  }


_MEMBERS = {'KeeNum member': Day.MON, 'KeeFlags member': Perm.READ}

#  The boxes belong to the class they are declared on, and copy to
#  themselves; see 'AttriBox.__deepcopy__'.
_BOXES = ('AttriBox', 'FixBox', 'Kee', 'KeeBox')

_PACKAGES = (
  utilities, utilities.combinatorics, core, dispatch, desc, mcls,
  mcls.space_hooks, lorem_ipsum, keenum, ezdata, work_test,
  work_test.samplers,
)


class TestNoPickleClasses(UtilitiesTest):
  """
  TestNoPickleClasses provides tests for the refusal to pickle the objects
  of every class of 'worktoy', and for copying them.
  """

  def test_pickle_refused(self) -> None:
    """Every object raises 'PickleException' when pickled."""
    for label, obj in {**_instances(), **_MEMBERS}.items():
      with self.subTest(label=label):
        with self.assertRaises(PickleException):
          pickle.dumps(obj)

  def test_unpickle_refused(self) -> None:
    """Every object refuses state restored from a pickle stream."""
    for label, obj in {**_instances(), **_MEMBERS}.items():
      with self.subTest(label=label):
        with self.assertRaises(PickleException):
          obj.__setstate__({})

  def test_copy(self) -> None:
    """A shallow copy is a new object of the same type, the boxes
    aside."""
    for label, obj in _instances().items():
      if label in _BOXES:
        continue
      with self.subTest(label=label):
        copied = copy.copy(obj)
        self.assertIs(type(copied), type(obj))
        self.assertIsNot(copied, obj)

  def test_deepcopy(self) -> None:
    """A deep copy is a new object of the same type, the boxes aside."""
    for label, obj in _instances().items():
      if label in _BOXES:
        continue
      with self.subTest(label=label):
        copied = copy.deepcopy(obj)
        self.assertIs(type(copied), type(obj))
        self.assertIsNot(copied, obj)

  def test_boxes_copy_to_themselves(self) -> None:
    """A box is its own copy, shallow and deep."""
    instances = _instances()
    for label in _BOXES:
      with self.subTest(label=label):
        box = instances[label]
        self.assertIs(copy.copy(box), box)
        self.assertIs(copy.deepcopy(box), box)

  def test_copied_state(self) -> None:
    """Copies keep the state that makes the object what it is."""
    holder = _instances()['BaseObject']
    self.assertEqual(copy.copy(holder).items, [1])
    self.assertIsNot(copy.deepcopy(holder).items, holder.items)
    self.assertEqual(copy.copy(Frozen(3)), Frozen(3))
    self.assertEqual(copy.deepcopy(Frozen(3)).x, 3)
    self.assertEqual(copy.copy(TypeSig(int, str)), TypeSig(int, str))
    self.assertEqual(copy.copy(SymbolicName('a', 'b')).snake, 'a_b')
    self.assertEqual(copy.copy(holder).twice(2), 4)
    self.assertEqual(copy.copy(CallMeMaybe(_function))(1), (1,))

  def test_members_copy_to_themselves(self) -> None:
    """An enumeration member is its own copy, shallow and deep."""
    for label, member in _MEMBERS.items():
      with self.subTest(label=label):
        self.assertIs(copy.copy(member), member)
        self.assertIs(copy.deepcopy(member), member)

  def test_every_exported_class_refuses(self) -> None:
    """Every class the packages export, apart from metaclasses, the
    sentinels and the uninstantiable 'ValidSlice', mixes in 'NoPickle'."""
    for package in _PACKAGES:
      for name in package.__all__:
        obj = getattr(package, name)
        if not isinstance(obj, type):
          continue
        if issubclass(obj, (type, Sentinel)) or obj is ValidSlice:
          continue
        with self.subTest(name=name):
          self.assertIsSubclass(obj, NoPickle)
