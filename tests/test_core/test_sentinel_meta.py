"""
TestSentinelMeta tests 'SentinelMeta' from 'worktoy.core.sentinels'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.core import MetaType
from worktoy.core.sentinels import Sentinel, SentinelMeta, DELETED, OWNER
from worktoy.core.sentinels import THIS, DESC, METACALL, ARGS
from worktoy.waitaminute.meta import IllegalInstantiation, DuplicateSentinel
from . import CoreTest, FamilyMeta


class TestSentinelMeta(CoreTest):
  """
  A sentinel is a class that is its own marker: unique for the whole
  process, compared by identity, impossible to instantiate, and readable
  in a traceback. 'SentinelMeta' builds them and keeps the one registry
  every family shares. The tests pin the registry, the refusal of a
  second class statement at a taken name leaving no trace, the refusal
  of instantiation, equality and hash, the text, and a family of a
  project sharing the registry.
  """

  def test_registry_holds_library_sentinels(self) -> None:
    registered = SentinelMeta._getRegisteredSentinels()
    for sentinel in (Sentinel, DELETED, OWNER, THIS, DESC, METACALL, ARGS):
      with self.subTest(sentinel=sentinel.__name__):
        self.assertIn(sentinel, registered)
        self.assertIs(SentinelMeta._getNamedSentinel(sentinel.__name__),
                      sentinel)

  def test_found_by_name_value(self) -> None:
    name = str.join('', ('DELE', 'TED'))
    self.assertIs(SentinelMeta._getNamedSentinel(name), DELETED)

  def test_unknown_name(self) -> None:
    with self.assertRaises(KeyError) as context:
      SentinelMeta._getNamedSentinel('CORE_NOWHERE')
    self.assertEqual(context.exception.args, ('CORE_NOWHERE',))

  def test_new_sentinel_registered(self) -> None:
    before = len(SentinelMeta._getRegisteredSentinels())

    class CORE_PENDING(Sentinel):
      """A sentinel of the tests."""

    self.assertEqual(len(SentinelMeta._getRegisteredSentinels()), before + 1)
    self.assertIs(SentinelMeta._getNamedSentinel('CORE_PENDING'),
                  CORE_PENDING)
    self.assertIsInstance(CORE_PENDING, SentinelMeta)
    self.assertIsInstance(CORE_PENDING, MetaType)
    self.assertIsSubclass(CORE_PENDING, Sentinel)

  def test_duplicate_name_refused_without_trace(self) -> None:
    before = [*SentinelMeta._getRegisteredSentinels()]
    with self.assertRaises(DuplicateSentinel) as context:
      class DELETED(Sentinel):
        pass
    self.assertEqual(context.exception.sentinelName, 'DELETED')
    self.assertIs(context.exception.existing, globals()['DELETED'])
    self.assertEqual(context.exception.module, __name__)
    self.assertIn("'DELETED'", str(context.exception))
    self.assertIn("the class statement in '%s'" % __name__,
                  str(context.exception))
    self.assertEqual(context.exception.module, __name__)
    self.assertIsInstance(context.exception, TypeError)
    self.assertEqual(SentinelMeta._getRegisteredSentinels(), before)

  def test_not_instantiable(self) -> None:
    for sentinel in (Sentinel, DELETED, OWNER, THIS, DESC, METACALL):
      with self.subTest(sentinel=sentinel.__name__):
        with self.assertRaises(IllegalInstantiation) as context:
          sentinel()
        self.assertIs(context.exception.cls, sentinel)
        self.assertIsInstance(context.exception, TypeError)
        self.assertIn("'%s'" % sentinel.__name__, str(context.exception))
    with self.assertRaises(IllegalInstantiation) as context:
      DELETED(1, key=2)
    self.assertIs(context.exception.cls, DELETED)
    self.assertIn("'DELETED'", str(context.exception))

  def test_identity_and_hash(self) -> None:
    self.assertEqual(DELETED, DELETED)
    self.assertNotEqual(DELETED, OWNER)
    self.assertIs(DELETED, DELETED)
    expected = hash((SentinelMeta.__module__, 'SentinelMeta',
                     DELETED.__module__, 'DELETED'))
    self.assertEqual(hash(DELETED), expected)
    self.assertEqual(hash(DELETED), hash(DELETED))
    self.assertEqual(len({DELETED, OWNER, DELETED}), 2)
    self.assertNotEqual(hash(DELETED), hash(OWNER))

  def test_text(self) -> None:
    self.assertEqual(str(DELETED), "<Sentinel: 'DELETED'>")
    self.assertEqual(repr(DELETED), "<Sentinel: 'DELETED'>")
    self.assertEqual(str(Sentinel), "<Sentinel: 'Sentinel'>")

  def test_prepare_is_plain_dict(self) -> None:
    space = SentinelMeta.__prepare__('CORE_X', ())
    self.assertIs(type(space), dict)
    self.assertEqual(space, {})

  def test_class_keyword_absorbed(self) -> None:
    class CORE_KEYED(Sentinel, flavour='mint'):
      pass

    self.assertIn(CORE_KEYED, SentinelMeta._getRegisteredSentinels())

  def test_family_shares_registry(self) -> None:
    CORE_FAMILY = FamilyMeta('CORE_FAMILY', (), {'__module__': __name__})
    self.assertIsInstance(CORE_FAMILY, FamilyMeta)
    self.assertIsInstance(CORE_FAMILY, SentinelMeta)
    self.assertIn(CORE_FAMILY, SentinelMeta._getRegisteredSentinels())
    self.assertNotIn('__registered_sentinels__', vars(FamilyMeta))
    self.assertEqual(CORE_FAMILY.describe(), 'family member CORE_FAMILY')
    self.assertEqual(str(CORE_FAMILY), "<Sentinel: 'CORE_FAMILY'>")
    with self.assertRaises(IllegalInstantiation) as context:
      CORE_FAMILY()
    self.assertIs(context.exception.cls, CORE_FAMILY)
    self.assertIn("'CORE_FAMILY'", str(context.exception))
    with self.assertRaises(DuplicateSentinel) as context:
      class CORE_FAMILY(Sentinel):
        pass
    self.assertEqual(context.exception.sentinelName, 'CORE_FAMILY')
    self.assertIs(context.exception.existing, CORE_FAMILY)
    self.assertEqual(context.exception.module, __name__)
    self.assertIn("'CORE_FAMILY'", str(context.exception))
    with self.assertRaises(DuplicateSentinel) as context:
      FamilyMeta('DELETED', (), {})
    self.assertIs(context.exception.existing, DELETED)
    self.assertIsNone(context.exception.module)
    self.assertEqual(context.exception.sentinelName, 'DELETED')
    self.assertIn('a class statement', str(context.exception))
