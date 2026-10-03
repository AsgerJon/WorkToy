"""
TestNoPickle subclasses 'UtilitiesTest' from the 'tests.test_utilities'
package and pins the behaviour of the 'NoPickle' mixin on small local
classes. A class mixing it in refuses to be pickled, by any protocol, and
refuses to have state restored into it by a pickle stream, raising
'PickleException' both ways. Since the 'copy' module falls back on the
same reduce protocol, the mixin copies by itself, the way that protocol
did: a new instance holding the instance dict, the slot values and the
items of a 'dict', shallow or deep, without calling '__init__' or
'__setattr__'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

import copy
import pickle
from typing import TYPE_CHECKING

from worktoy.utilities import NoPickle
from worktoy.waitaminute import PickleException

from . import UtilitiesTest

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any


class Plain(NoPickle):
  """Plain keeps its state in the instance dict and counts the calls of
  its '__init__'."""

  __init_calls__ = 0

  def __init__(self, *items: Any) -> None:
    type(self).__init_calls__ += 1
    self.items = [*items, ]


class Slotted(NoPickle):
  """Slotted keeps its state in slots, one of which may stay unset."""

  __slots__ = ('first', 'second')

  def __init__(self, first: Any) -> None:
    self.first = first


class Single(NoPickle):
  """Single declares its one slot as a bare string."""

  __slots__ = 'only'


class Mapping(NoPickle, dict):
  """Mapping is a 'dict' that also holds an attribute."""

  label = None


class Guarded(NoPickle):
  """Guarded refuses every assignment once constructed."""

  def __init__(self, value: Any) -> None:
    object.__setattr__(self, 'value', value)

  def __setattr__(self, key: str, value: Any) -> None:
    raise AttributeError(key)


class Reduced(NoPickle):
  """Reduced reopens '__reduce__', leaving the other layers to refuse."""

  def __reduce__(self) -> tuple:
    return Reduced, ()


class Stated(NoPickle):
  """Stated reopens '__getstate__', leaving the other layers to refuse."""

  def __getstate__(self) -> dict:
    return {}


class Failure(NoPickle, ValueError):
  """Failure is an exception keeping state in a slot."""

  __slots__ = ('detail',)

  def __init__(self, detail: Any) -> None:
    ValueError.__init__(self, 'failure', detail)
    self.detail = detail


class TestNoPickle(UtilitiesTest):
  """
  TestNoPickle provides tests for the 'NoPickle' mixin.
  """

  def test_pickle_refused(self) -> None:
    """Pickling raises 'PickleException' for every protocol."""
    for protocol in range(pickle.HIGHEST_PROTOCOL + 1):
      with self.subTest(protocol=protocol):
        with self.assertRaises(PickleException) as context:
          pickle.dumps(Plain(1), protocol)
        self.assertEqual(context.exception.action, 'pickled')

  def test_reduce_refused(self) -> None:
    """Each hook of the pickle protocol raises 'PickleException'."""
    plain = Plain(1)
    with self.assertRaises(PickleException):
      plain.__reduce__()
    with self.assertRaises(PickleException):
      plain.__reduce_ex__(2)
    with self.assertRaises(PickleException):
      plain.__getstate__()

  def test_layers_refuse_alone(self) -> None:
    """Each layer refuses on its own: a subclass reopening '__reduce__'
    still cannot be pickled, and one reopening '__getstate__' still
    refuses '__reduce__'."""
    self.assertEqual(Reduced().__reduce__(), (Reduced, ()))
    with self.assertRaises(PickleException):
      pickle.dumps(Reduced())
    self.assertEqual(Stated().__getstate__(), {})
    with self.assertRaises(PickleException):
      Stated().__reduce__()

  def test_unpickle_refused(self) -> None:
    """Restoring state from a pickle stream raises 'PickleException'."""
    with self.assertRaises(PickleException) as context:
      Plain(1).__setstate__({'items': []})
    self.assertEqual(context.exception.action, 'unpickled')

  def test_refusal_names_the_object(self) -> None:
    """The exception holds the object and names its type."""
    plain = Plain(1)
    with self.assertRaises(PickleException) as context:
      pickle.dumps(plain)
    self.assertIs(context.exception.obj, plain)
    self.assertIn('Plain', str(context.exception))

  def test_copy(self) -> None:
    """A shallow copy is a new instance sharing the attribute values,
    made without calling '__init__'."""
    plain = Plain(1, 2)
    calls = Plain.__init_calls__
    copied = copy.copy(plain)
    self.assertIsInstance(copied, Plain)
    self.assertIsNot(copied, plain)
    self.assertIs(copied.items, plain.items)
    self.assertEqual(Plain.__init_calls__, calls)

  def test_deepcopy(self) -> None:
    """A deep copy copies the attribute values too."""
    plain = Plain([1], 2)
    copied = copy.deepcopy(plain)
    self.assertIsNot(copied.items, plain.items)
    self.assertIsNot(copied.items[0], plain.items[0])
    self.assertEqual(copied.items, plain.items)

  def test_deepcopy_cycle(self) -> None:
    """A deep copy of an object referring to itself refers to the copy."""
    plain = Plain()
    plain.me = plain
    copied = copy.deepcopy(plain)
    self.assertIs(copied.me, copied)

  def test_copy_slots(self) -> None:
    """Slot values are copied, and an unset slot stays unset."""
    slotted = Slotted([1])
    copied = copy.copy(slotted)
    deep = copy.deepcopy(slotted)
    self.assertIs(copied.first, slotted.first)
    self.assertEqual(deep.first, [1])
    self.assertIsNot(deep.first, slotted.first)
    with self.assertRaises(AttributeError):
      _ = copied.second

  def test_copy_single_slot(self) -> None:
    """A slot declared as a bare string is copied too."""
    single = Single()
    single.only = 7
    self.assertEqual(copy.copy(single).only, 7)

  def test_copy_mapping(self) -> None:
    """The items of a 'dict' are copied along with its attributes."""
    mapping = Mapping(a=[1])
    mapping.label = 'x'
    copied = copy.copy(mapping)
    deep = copy.deepcopy(mapping)
    self.assertEqual(dict(copied), {'a': [1]})
    self.assertIs(copied['a'], mapping['a'])
    self.assertEqual(copied.label, 'x')
    self.assertIsNot(deep['a'], mapping['a'])
    self.assertEqual(deep['a'], [1])

  def test_copy_bypasses_setattr(self) -> None:
    """Copying does not go through '__setattr__', which does refuse an
    ordinary assignment."""
    guarded = Guarded(5)
    with self.assertRaises(AttributeError):
      guarded.value = 6
    self.assertEqual(copy.copy(guarded).value, 5)
    self.assertEqual(copy.deepcopy(guarded).value, 5)

  def test_copy_exception(self) -> None:
    """An exception keeps its arguments and its slot values."""
    failure = Failure('bad')
    copied = copy.copy(failure)
    self.assertIsInstance(copied, Failure)
    self.assertEqual(copied.args, ('failure', 'bad'))
    self.assertEqual(copied.detail, 'bad')
