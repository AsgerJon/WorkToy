"""
TestAbstractNamespaceItems tests the reads, bindings and deletions of
'AbstractNamespace' from 'worktoy.mcls'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.mcls import BaseMeta, BaseSpace, BaseObject
from worktoy.waitaminute.meta import HookException, ClaimedName
from . import MclsTest, LoggingHook, ClaimingHook, ClaimedSpace
from . import ClaimedMeta, Roster


class TestAbstractNamespaceItems(MclsTest):
  """
  Every read, binding and deletion of a class body passes the hooks of
  its namespace: a hook may refuse a read, claim a binding so the
  namespace never stores it, or claim a deletion. A claimed name still
  reads as bound through the shadow record, and a deletion of a claimed
  name fails as the class is created. The tests pin each route on a
  'ClaimedSpace' driven by hand.
  """

  def setUp(self) -> None:
    MclsTest.setUp(self)
    LoggingHook.log.clear()
    ClaimingHook.taken.clear()
    ClaimingHook.dropped.clear()
    self.space = ClaimedSpace(ClaimedMeta, 'A', ())

  def test_binding_stored_and_shadowed(self) -> None:
    self.space['x'] = 1
    self.assertEqual(dict.__getitem__(self.space, 'x'), 1)
    self.assertEqual(self.space.getShadowSpace(), {'x': 1})
    self.assertIn(('set', 'x'), LoggingHook.log)
    self.space['x'] = 2
    self.assertEqual(self.space['x'], 2)
    self.assertEqual(self.space.getShadowSpace()['x'], 2)

  def test_claimed_binding_not_stored(self) -> None:
    self.space['y'] = b'claimed'
    self.assertFalse(dict.__contains__(self.space, 'y'))
    self.assertEqual(self.space['y'], b'claimed')
    self.assertEqual(ClaimingHook.taken, [('y', b'claimed')])
    self.assertEqual(self.space.getShadowSpace(), {'y': b'claimed'})
    self.assertNotIn('y', self.space.compile())

  def test_claim_ends_the_round(self) -> None:
    hooks = [*self.space.getHooks()]
    self.assertIs(hooks[3], ClaimedSpace.__dict__['claimingHook'])
    self.assertTrue(hooks[3].setItemPhase('z', b'1'))
    self.assertFalse(hooks[3].setItemPhase('z', 1))
    self.assertFalse(hooks[4].setItemPhase('z', b'1'))

  def test_miss_raises_after_the_hooks(self) -> None:
    with self.assertRaises(KeyError) as context:
      _ = self.space['nothing']
    self.assertEqual(context.exception.args, ('nothing',))
    record = [entry for entry in LoggingHook.log if entry[0] == 'get'][0]
    self.assertEqual(record[1], 'nothing')
    self.assertIsInstance(record[2], KeyError)

  def test_bound_key_error_is_a_value(self) -> None:
    own = KeyError('bound by the body')
    self.space['err'] = own
    self.assertIs(self.space['err'], own)

  def test_refused_read_wrapped(self) -> None:
    with self.assertRaises(HookException) as context:
      _ = self.space['forbidden']
    exception = context.exception
    self.assertIsInstance(exception.initialException, ValueError)
    self.assertIs(exception.namespaceObject, self.space)
    self.assertEqual(exception.itemKey, 'forbidden')
    self.assertIsInstance(exception.errorValue, KeyError)
    self.assertIs(exception.hookFunction,
                  ClaimedSpace.__dict__['refusingHook'])
    self.assertIn('forbidden', str(exception))
    self.space['forbidden'] = 3
    with self.assertRaises(HookException) as context:
      _ = self.space['forbidden']
    self.assertEqual(context.exception.errorValue, 3)
    self.assertIsInstance(context.exception.initialException, ValueError)
    self.assertEqual(context.exception.itemKey, 'forbidden')
    self.assertIn("Value: '3'", str(context.exception))

  def test_unknown_deletion_refused(self) -> None:
    with self.assertRaises(KeyError) as context:
      del self.space['nothing']
    self.assertEqual(context.exception.args, ('nothing',))

  def test_plain_deletion(self) -> None:
    self.space['x'] = 1
    del self.space['x']
    self.assertFalse(dict.__contains__(self.space, 'x'))
    self.assertEqual(self.space.getShadowSpace(), {})
    self.assertIn(('del', 'x'), LoggingHook.log)
    self.assertEqual(self.space.getClaimedDeletions(), ())
    with self.assertRaises(KeyError) as context:
      _ = self.space['x']
    self.assertEqual(context.exception.args, ('x',))

  def test_deletion_written_past_the_hooks(self) -> None:
    dict.__setitem__(self.space, 'raw', 1)
    self.assertFalse(self.space._isClaimed('raw'))
    del self.space['raw']
    self.assertFalse(dict.__contains__(self.space, 'raw'))
    self.assertEqual(self.space.getClaimedDeletions(), ())

  def test_claimed_deletion(self) -> None:
    self.space['d'] = bytearray(b'1')
    del self.space['d']
    self.assertEqual(ClaimingHook.dropped, ['d'])
    self.assertEqual(dict.__getitem__(self.space, 'd'), bytearray(b'1'))
    self.assertEqual(self.space.getClaimedDeletions(), ())

  def test_deletion_of_claimed_name_fails_at_compile(self) -> None:
    self.space['y'] = b'claimed'
    del self.space['y']
    self.assertEqual(self.space.getClaimedDeletions(), ('y',))
    self.assertEqual(self.space.getShadowSpace(), {})
    with self.assertRaises(ClaimedName) as context:
      self.space.compile()
    self.assertEqual(context.exception.className, 'A')
    self.assertEqual(context.exception.keyName, 'y')
    self.assertIn("The class body of 'A' deletes 'y'",
                  str(context.exception))

  def test_deletion_of_rebound_claimed_name(self) -> None:
    self.space['w'] = 1
    self.space['w'] = b'2'
    self.assertEqual(dict.__getitem__(self.space, 'w'), 1)
    self.assertEqual(self.space['w'], 1)
    self.assertTrue(self.space._isClaimed('w'))
    del self.space['w']
    self.assertFalse(dict.__contains__(self.space, 'w'))
    self.assertEqual(self.space.getClaimedDeletions(), ('w',))

  def test_is_claimed(self) -> None:
    self.assertFalse(self.space._isClaimed('never'))
    self.space['a'] = 1
    self.assertFalse(self.space._isClaimed('a'))
    self.space['b'] = b'1'
    self.assertTrue(self.space._isClaimed('b'))
    self.space['a'] = b'2'
    self.assertTrue(self.space._isClaimed('a'))

  def test_in_a_class_statement(self) -> None:
    with self.assertRaises(ClaimedName) as context:
      class A(metaclass=ClaimedMeta):
        x = b'claimed'
        del x
    self.assertEqual(context.exception.className, 'A')
    self.assertEqual(context.exception.keyName, 'x')
    self.assertIn("deletes 'x'", str(context.exception))

    class B(metaclass=ClaimedMeta):
      x = b'claimed'
      y = x.decode()
      z = 1
      del z

    self.assertEqual(B.y, 'claimed')
    self.assertFalse(hasattr(B, 'x'))
    self.assertFalse(hasattr(B, 'z'))

  def test_deep_get_item(self) -> None:
    space = BaseSpace(BaseMeta, 'A', (Roster,))
    space['own'] = 1
    self.assertEqual(space.deepGetItem('own'), 1)
    self.assertEqual(space.deepGetItem('members'), [Roster.members])
    self.assertEqual(space.deepGetItem('__class_iter__')[-1],
                     BaseObject.__dict__['__class_iter__'])
    with self.assertRaises(KeyError) as context:
      space.deepGetItem('absent')
    self.assertEqual(context.exception.args, ('absent',))

  def test_random_bindings(self) -> None:
    self.randomWord.size = 6
    self.randomInteger.size = 6
    words = self.randomWord.row
    numbers = self.randomInteger.row
    for word, number in zip(words, numbers):
      self.space[word] = number
    for word, number in zip(words, numbers):
      with self.subTest(word=word):
        self.assertEqual(self.space[word], number)
        del self.space[word]
        self.assertNotIn(word, self.space.getShadowSpace())
