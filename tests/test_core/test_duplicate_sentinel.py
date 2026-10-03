"""
TestDuplicateSentinel subclasses 'CoreTest' and pins that a class
statement declaring a sentinel at a name a sentinel already holds is
refused with 'DuplicateSentinel'. A sentinel defines one concept for the
whole process, so two modules each declaring a 'PENDING' do not get a
sentinel each. The second class statement used to receive the first
sentinel without a word, docstring and module included, so a message of
the mailer passed the identity check of the ledger.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

import sys
import types

from worktoy.core import sentinels
from worktoy.core.sentinels import Sentinel, SentinelMeta
from worktoy.waitaminute.meta import DuplicateSentinel

from . import CoreTest

LEDGER = '''
from worktoy.core.sentinels import Sentinel


class PENDING(Sentinel):
  """A ledger entry booked but not yet posted."""


def post(entry):
  return 'posted' if entry is PENDING else 'left alone'
'''

MAILER = '''
from worktoy.core.sentinels import Sentinel


class PENDING(Sentinel):
  """A message queued but not yet sent."""
'''


def _loadModule(name: str, source: str) -> types.ModuleType:
  """Runs 'source' as the module 'name', as an import would."""
  module = types.ModuleType(name)
  sys.modules[name] = module
  exec(source, module.__dict__)
  return module


class TestDuplicateSentinel(CoreTest):
  """
  TestDuplicateSentinel provides tests for the refusal of a second
  sentinel at a taken name.
  """

  def tearDown(self) -> None:
    for name in ('ledger', 'mailer'):
      sys.modules.pop(name, None)
    super().tearDown()

  def test_second_module_refused(self) -> None:
    """A mailer declaring 'PENDING' after a ledger did is refused, and
    the exception names the sentinel, the module of the first and the
    module of the second."""
    ledger = _loadModule('ledger', LEDGER)
    with self.assertRaises(DuplicateSentinel) as context:
      _loadModule('mailer', MAILER)
    e = context.exception
    self.assertEqual(e.sentinelName, 'PENDING')
    self.assertIs(e.existing, ledger.PENDING)
    self.assertEqual(e.module, 'mailer')
    self.assertIn("'PENDING'", str(e))
    self.assertIn("'ledger'", str(e))
    self.assertIn("'mailer'", str(e))
    self.assertEqual(str(e), repr(e))
    self.assertIsInstance(e, TypeError)

  def test_first_sentinel_kept(self) -> None:
    """The refusal leaves the first sentinel registered and untouched,
    docstring and module included."""

    class POSTED(Sentinel):
      """A ledger entry posted."""

    with self.assertRaises(DuplicateSentinel):
      class POSTED(Sentinel):  # noqa: F811
        """Something else entirely."""

    self.assertEqual(POSTED.__doc__.strip(), 'A ledger entry posted.')
    self.assertEqual(POSTED.__module__, __name__)

  def test_library_sentinel_refused(self) -> None:
    """A 'DELETED' of one's own is refused, naming the one worktoy
    declares and where."""
    with self.assertRaises(DuplicateSentinel) as context:
      class DELETED(Sentinel):
        """Marks a row the user removed, kept for undo."""
    e = context.exception
    self.assertIs(e.existing, sentinels.DELETED)
    self.assertEqual(e.module, __name__)
    self.assertIn("'%s'" % sentinels.DELETED.__module__, str(e))
    self.assertIn("'%s'" % __name__, str(e))

  def test_distinct_names_accepted(self) -> None:
    """Two sentinels of different names are two sentinels."""

    class QUEUED(Sentinel):
      """A message queued."""

    class SENT(Sentinel):
      """A message sent."""

    self.assertIsNot(QUEUED, SENT)
    self.assertTrue(issubclass(QUEUED, Sentinel))
    self.assertTrue(issubclass(SENT, Sentinel))

  def test_without_module(self) -> None:
    """A sentinel built by hand from a namespace naming no module is
    refused the same, the message saying only that a class statement
    declares another."""
    with self.assertRaises(DuplicateSentinel) as context:
      SentinelMeta('THIS', (Sentinel,), {})
    e = context.exception
    self.assertIs(e.existing, sentinels.THIS)
    self.assertIsNone(e.module)
    self.assertIn('a class statement declares another', str(e))
