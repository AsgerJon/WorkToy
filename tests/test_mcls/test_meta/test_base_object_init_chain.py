"""
TestBaseObjectInitChain pins that 'Object.__init__', once it has recorded
its arguments, calls the next '__init__' along the resolution order
without them. A base listed after a 'BaseObject' subclass, such as
'threading.Thread', 'logging.Handler' or a cooperative mixin, is then
initialized as in a plain class. It used to be skipped, since
'Object.__init__' called 'object.__init__' directly, and the object failed
later, at its first use. A base whose '__init__' requires arguments goes
before 'BaseObject', where it receives them as before; listed after it,
it refuses at construction with its own 'TypeError'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

import logging
import threading

from worktoy.mcls import BaseObject

from .. import MCLSTest


class Worker(BaseObject, threading.Thread):
  """Worker runs as a thread."""

  def run(self) -> None:
    self.result = 42


class Collector(BaseObject, logging.Handler):
  """Collector keeps the message of the last record it handles."""

  def emit(self, record: logging.LogRecord) -> None:
    self.last = record.getMessage()


class ReadyMixin:
  """ReadyMixin marks the instance in a cooperative initializer."""

  def __init__(self, *args, **kwargs) -> None:
    super().__init__(*args, **kwargs)
    self.ready = True


class Tool(BaseObject, ReadyMixin):
  """Tool lists the mixin after 'BaseObject'."""


class NeedsValue:
  """NeedsValue requires an argument."""

  def __init__(self, value: int) -> None:
    self.value = value


class ValueFirst(NeedsValue, BaseObject):
  """ValueFirst lists the base requiring an argument first."""


class ValueLast(BaseObject, NeedsValue):
  """ValueLast lists the base requiring an argument after 'BaseObject'."""


class TestBaseObjectInitChain(MCLSTest):
  """
  TestBaseObjectInitChain provides tests for the bases a 'BaseObject'
  subclass lists after 'BaseObject'.
  """

  def test_thread_after_base_object(self) -> None:
    """A 'threading.Thread' listed after 'BaseObject' is initialized, so
    the thread starts and runs."""
    worker = Worker()
    worker.start()
    worker.join()
    self.assertEqual(worker.result, 42)

  def test_handler_after_base_object(self) -> None:
    """A 'logging.Handler' listed after 'BaseObject' is initialized, so a
    logger can hand it a record."""
    collector = Collector()
    logger = logging.getLogger('test_base_object_init_chain')
    logger.addHandler(collector)
    try:
      logger.warning('hello')
    finally:
      logger.removeHandler(collector)
    self.assertEqual(collector.last, 'hello')

  def test_mixin_after_base_object(self) -> None:
    """A cooperative mixin listed after 'BaseObject' has its initializer
    run."""
    self.assertTrue(Tool().ready)

  def test_required_arguments_first(self) -> None:
    """A base requiring arguments listed before 'BaseObject' receives
    them."""
    self.assertEqual(ValueFirst(7).value, 7)

  def test_required_arguments_last(self) -> None:
    """A base requiring arguments listed after 'BaseObject' is called
    without them and refuses at construction with its own 'TypeError'."""
    with self.assertRaises(TypeError) as context:
      ValueLast()
    self.assertIn("'value'", str(context.exception))
