"""
TestObjectGuards tests the guards 'Object' keeps on the private name, on
the deleted-value sentinel, and on the context stack.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.core import Object
from worktoy.core.sentinels import DELETED
from worktoy.desc import Field
from worktoy.waitaminute import MissingVariable, TypeException
from worktoy.waitaminute.desc import WithoutException
from . import CoreTest


class ContextLiar(Object):
  """
  ContextLiar reports a context it does not have.

  'hasContext' belongs to the documented public context API, so a
  subclass is free to override it, and nothing obliges that override to
  agree with the chain it is meant to summarise. This class is that
  disagreement in its simplest form: it claims a context unconditionally
  while the chain is left absent. The guards in 'getContextInstance' and
  'getContextOwner' are written for exactly this, which is why ordinary
  use never reaches them.
  """

  def hasContext(self) -> bool:
    return True


class TestObjectGuards(CoreTest):
  """
  TestObjectGuards tests the guards 'Object' keeps on the private name,
  on the deleted-value sentinel, and on the context stack.

  These are the paths a descriptor reaches only when it never went
  through a class body, or when a subclass contradicts the invariant a
  guard relies on, which is why the ordinary descriptor tests never
  arrive at them. A descriptor built by hand has neither a field name
  nor a cached private name, and that is exactly the state the guards
  are written for.
  """

  def test_private_name_without_field_name(self) -> None:
    """
    Testing that asking for the private name before '__set_name__' has
    run reports the missing field name rather than failing inside the
    string substitution that builds the name.
    """
    descriptor = Field()
    with self.assertRaises(MissingVariable) as context:
      _ = descriptor.getPrivateName()
    e = context.exception
    self.assertIs(e.instance, descriptor)
    self.assertEqual(e.varName, '__field_name__')
    self.assertIn(str, e.expectedTypes)

  def test_private_name_rejects_non_string_cache(self) -> None:
    """
    Testing that a cached private name of the wrong type is refused
    rather than handed back, since every caller goes on to use it as an
    attribute name.
    """
    descriptor = Field()
    descriptor.__field_name__ = 'bar'
    descriptor.__private_name__ = 69
    with self.assertRaises(TypeException) as context:
      _ = descriptor.getPrivateName()
    e = context.exception
    self.assertEqual(e.varName, '__private_name__')
    self.assertEqual(e.actualObject, 69)
    self.assertIn(str, e.expectedTypes)

  def test_private_name_caches(self) -> None:
    """
    Testing that the private name is derived once and then reused, which
    is what keeps it off the hot path of every later access.
    """
    descriptor = Field()
    descriptor.__field_name__ = 'fooBar'
    first = descriptor.getPrivateName()
    self.assertEqual(descriptor.__private_name__, first)
    self.assertEqual(first, descriptor.getPrivateName())
    self.assertEqual(first, '__foo_bar__')

  def test_deleted_guard_without_field_name(self) -> None:
    """
    Testing that the deleted-value guard reports the missing field name
    when it has none to report the deletion against.
    """
    descriptor = Field()
    with self.assertRaises(MissingVariable) as context:
      _ = descriptor._deletedGuard(descriptor, DELETED)
    e = context.exception
    self.assertEqual(e.varName, '__field_name__')
    self.assertIn(str, e.expectedTypes)

  def test_deleted_guard_names_the_field(self) -> None:
    """
    Testing that a deleted value is reported against the attribute the
    caller actually asked for, so the message points at the read rather
    than at the machinery behind it.
    """
    descriptor = Field()
    descriptor.__field_name__ = 'bar'
    with self.assertRaises(MissingVariable) as context:
      _ = descriptor._deletedGuard(descriptor, DELETED)
    e = context.exception
    self.assertIs(e.instance, descriptor)
    self.assertEqual(e.varName, 'bar')

  def test_context_guards_reject_absent_chain(self) -> None:
    """
    Testing that both context accessors refuse an absent chain when
    'hasContext' claims otherwise, instead of subscripting 'None'.

    The chain is cleared explicitly because 'Object.__init__' installs
    an empty list on the instance, which shadows the class-level default
    and would reach the accessors as an 'IndexError' rather than as the
    absence the guards are looking for.
    """
    liar = ContextLiar()
    setattr(liar, '__call_chain__', None)
    self.assertTrue(liar.hasContext())
    self.assertIsNone(liar.__call_chain__)
    for name in ('getContextInstance', 'getContextOwner'):
      with self.assertRaises(MissingVariable) as context:
        _ = getattr(liar, name)()
      e = context.exception
      self.assertIs(e.instance, liar)
      self.assertEqual(e.varName, '__call_chain__')
      self.assertIn(tuple, e.expectedTypes)

  def test_context_accessors_without_context(self) -> None:
    """
    Testing that an honest 'Object' with no context raises
    'WithoutException' from both accessors, which is the path the guards
    above sit behind.
    """
    obj = Object()
    self.assertFalse(obj.hasContext())
    for name in ('getContextInstance', 'getContextOwner'):
      with self.assertRaises(WithoutException):
        _ = getattr(obj, name)()

  def test_deleted_guard_passes_other_values(self) -> None:
    """
    Testing that anything other than the sentinel travels through
    untouched, including the falsy values a truth test would swallow.
    """
    descriptor = Field()
    descriptor.__field_name__ = 'bar'
    for value in (69, 0, '', None, [], False):
      self.assertIs(descriptor._deletedGuard(descriptor, value), value)
