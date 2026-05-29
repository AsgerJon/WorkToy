"""
TestQuickDesc provides tests for the 'QuickDesc' descriptor class
from 'worktoy.utilities'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from . import UtilitiesTest
from worktoy.utilities import QuickDesc
from worktoy.waitaminute import MissingVariable

if TYPE_CHECKING:  # pragma: no cover
  # @formatter:off
  from typing import Any, Optional

  class QuickDesc:  # noqa
    __private_key__: Optional[str]
    __field_name__: Optional[str]
    __field_owner__: Optional[type]
    def __init__(self, key: str) -> None: print(key)
    def __get__(self, instance: Any, owner: type) -> Any: ...
    def __set__(self, instance: Any, value: Any) -> None: ...
    def __delete__(self, instance: Any) -> None: ...
    def __set_name__(self, owner: type, name: str) -> None: ...
  # @formatter:on


#  ____________________________________________________________________
#  Module-level fixture
#  ¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨

class _Demo:
  """Fixture exercising QuickDesc as it is used inside worktoy:
  a private slot at class scope, with a public descriptor proxying
  access to it."""
  __value__ = None
  value = QuickDesc('__value__')


class TestQuickDesc(UtilitiesTest):
  """Tests for QuickDesc - the minimal-boilerplate descriptor used
  internally by worktoy."""

  #  ================================================================
  #  |
  #  |                         CONSTRUCTION
  #  ================================================================

  #  ________________________________________________________________
  #  Good construction
  #  ¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨

  def test_init_records_private_key(self) -> None:
    qd = QuickDesc('__some_key__')
    self.assertEqual(qd.__private_key__, '__some_key__')

  def test_init_leaves_field_name_and_owner_unset(self) -> None:
    """A loose QuickDesc, never bound to a class attribute, has
    no field name or owner. Those slots are populated by
    __set_name__ at class-creation time, not by __init__."""
    qd = QuickDesc('__some_key__')
    self.assertIsNone(qd.__field_name__)
    self.assertIsNone(qd.__field_owner__)

  #  ================================================================
  #  |
  #  |                          PYTHON API
  #  ================================================================

  #  ________________________________________________________________
  #  __set_name__ - good binding
  #  ¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨

  def test_set_name_records_field_name(self) -> None:
    """Class creation triggers __set_name__, which records the
    attribute name on the descriptor."""
    self.assertEqual(_Demo.value.__field_name__, 'value')

  def test_set_name_records_field_owner(self) -> None:
    self.assertIs(_Demo.value.__field_owner__, _Demo)

  #  ________________________________________________________________
  #  __set_name__ - name collision
  #  ¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨

  def test_set_name_rejects_collision(self) -> None:
    """A descriptor bound to the same name as its private key would
    recurse onto itself when accessed via getattr; class creation
    must fail before the class object escapes.

    Please note the ambiguity in the error type. The 'worktoy' library
    supports Python 3.7. In this version, the recently implemented
    '__set_name__' introduced in 3.6, would raise a 'RuntimeError' if
    any exception occurred during the execution of a '__set_name__'. The
    code under testing does indeed raise 'ValueError', which is what
    propagates in Python 3.8 and later. But in 3.7, this propagates as a
    'RuntimeError'.
    """
    with self.assertRaises((ValueError, RuntimeError)):
      class _Bad:  # noqa
        foo = QuickDesc('foo')

  #  ________________________________________________________________
  #  __get__ - class-level access
  #  ¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨

  def test_get_on_class_returns_descriptor_itself(self) -> None:
    """When 'instance' is None (class-level access), __get__ returns
    self rather than triggering a value lookup. This is what makes
    introspection like '_Demo.value.__field_name__' possible."""
    self.assertIsInstance(_Demo.value, QuickDesc)

  #  ________________________________________________________________
  #  __get__ - instance access
  #  ¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨

  def test_get_on_instance_returns_stored_value(self) -> None:
    """__get__ proxies to instance.<private_key> via getattr."""
    inst = _Demo()
    inst.__value__ = 'hello'
    self.assertEqual(inst.value, 'hello')

  def test_get_on_instance_falls_back_to_class_default(self) -> None:
    """Without an instance-level assignment, getattr resolves to
    the class-level default (None on _Demo)."""
    inst = _Demo()
    self.assertIsNone(inst.value)

  #  ________________________________________________________________
  #  __get__ - missing private key
  #  ¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨

  def test_get_raises_when_private_key_is_none(self) -> None:
    """If __private_key__ is unset, __get__ has no slot to proxy
    to and raises MissingVariable. Reachable when a subclass
    bypasses __init__ or when the slot is manually cleared."""
    qd = QuickDesc('__value__')
    qd.__private_key__ = None
    inst = _Demo()
    with self.assertRaises(MissingVariable):
      qd.__get__(inst, type(inst))

  #  ________________________________________________________________
  #  __set__ - read-only enforcement
  #  ¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨

  def test_set_raises_attribute_error(self) -> None:
    """Defining __set__ promotes QuickDesc to a data descriptor;
    'inst.value = x' is intercepted and raises rather than silently
    shadowing the descriptor with an instance attribute."""
    inst = _Demo()
    with self.assertRaises(AttributeError):
      inst.value = 'whoops'

  def test_set_does_not_shadow_the_descriptor(self) -> None:
    """The whole point of __set__: after a failed assignment, the
    descriptor remains the authoritative source for the attribute,
    rather than being shadowed by an instance __dict__ entry."""
    inst = _Demo()
    inst.__value__ = 'real'
    with self.assertRaises(AttributeError):
      inst.value = 'whoops'
    self.assertEqual(inst.value, 'real')

  def test_set_on_unbound_descriptor_still_raises(self) -> None:
    """A QuickDesc that has never been class-bound has
    __field_name__=None; __set__ must still raise cleanly rather
    than crashing on the missing name."""
    qd = QuickDesc('__value__')
    with self.assertRaises(AttributeError):
      qd.__set__(_Demo(), 'whoops')

  #  ________________________________________________________________
  #  __delete__ - read-only enforcement
  #  ¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨

  def test_delete_raises_attribute_error(self) -> None:
    """'del inst.value' must reach __delete__ and raise, rather
    than falling through to a no-op on the instance __dict__."""
    inst = _Demo()
    with self.assertRaises(AttributeError):
      del inst.value

  def test_delete_on_unbound_descriptor_still_raises(self) -> None:
    qd = QuickDesc('__value__')
    with self.assertRaises(AttributeError):
      qd.__delete__(_Demo())
