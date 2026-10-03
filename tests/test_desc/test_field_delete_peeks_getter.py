"""
TestFieldDeletePeeksGetter subclasses 'DescTest' and pins what deleting a
'Field' reads from its getter. 'Object.__delete__' reads the old value
before deleting, only to report it, and a 'Field' answers that read
through its getter: what the getter returns is the old value
'ProtectedError' reports, and a getter answering 'DELETED', as one does
once a deleter stored it, makes a second 'del' raise 'MissingVariable',
as a read does. A getter that raises stops nothing: the deleters run, and
no old value is reported. For 1.1 the getter did not run on 'del' at all,
so a second 'del' ran the deleters again and 'ProtectedError' reported no
old value, and before that a getter that raised stopped the deleters.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.core.sentinels import DELETED
from worktoy.desc import Field
from worktoy.mcls import BaseObject
from worktoy.waitaminute import MissingVariable
from worktoy.waitaminute.desc import ProtectedError

from . import DescTest


class Lazy(BaseObject):
  """Lazy has a getter that raises and counts its calls, a getter that
  answers, and a getter that raises without any deleter."""

  __get_count__ = 0
  __deleted__ = 0

  x = Field()
  y = Field()
  z = Field()

  @x.GET
  def _getX(self) -> int:
    self.__get_count__ += 1
    raise ValueError('not ready')

  @x.DELETE
  def _delX(self) -> None:
    self.__deleted__ += 1

  @y.GET
  def _getY(self) -> int:
    self.__get_count__ += 1
    return 7

  @z.GET
  def _getZ(self) -> int:
    self.__get_count__ += 1
    raise ValueError('not ready either')


class Draft(BaseObject):
  """Draft has a deleter storing 'DELETED', which its getter answers."""

  __body__ = None
  __deleted__ = 0

  body = Field()

  @body.GET
  def _getBody(self) -> str:
    if self.__body__ is None:
      raise ValueError('not loaded yet')
    return self.__body__

  @body.SET
  def _setBody(self, value: str) -> None:
    self.__body__ = value

  @body.DELETE
  def _delBody(self) -> None:
    self.__deleted__ += 1
    self.__body__ = DELETED


class Counter(BaseObject):
  """Counter has a deleter resetting the value instead of marking it
  deleted."""

  __n__ = 5
  __deleted__ = 0

  n = Field()

  @n.GET
  def _getN(self) -> int:
    return self.__n__

  @n.DELETE
  def _delN(self) -> None:
    self.__deleted__ += 1
    self.__n__ = 0


class TestFieldDeletePeeksGetter(DescTest):
  """
  TestFieldDeletePeeksGetter provides tests for what deleting a 'Field'
  reads from its getter.
  """

  def test_getters_run_on_read(self) -> None:
    """The getters run on a read, as before."""
    lazy = Lazy()
    with self.assertRaises(ValueError):
      _ = lazy.x
    self.assertEqual(lazy.y, 7)
    self.assertEqual(lazy.__get_count__, 2)

  def test_deleter_runs_despite_raising_getter(self) -> None:
    """The deleter runs though the getter raises, which runs once."""
    lazy = Lazy()
    del lazy.x
    self.assertEqual(lazy.__deleted__, 1)
    self.assertEqual(lazy.__get_count__, 1)

  def test_protected_reports_old_value(self) -> None:
    """Without a deleter, 'ProtectedError' reports the value the getter
    returned, which ran once."""
    lazy = Lazy()
    with self.assertRaises(ProtectedError) as context:
      del lazy.y
    self.assertEqual(context.exception.oldVal, 7)
    self.assertEqual(lazy.__get_count__, 1)

  def test_raising_getter_reports_no_old_value(self) -> None:
    """Without a deleter and with a getter that raises, 'ProtectedError'
    reports no old value, and the getter's exception goes nowhere."""
    lazy = Lazy()
    with self.assertRaises(ProtectedError) as context:
      del lazy.z
    self.assertIsNone(context.exception.oldVal)
    self.assertEqual(lazy.__get_count__, 1)

  def test_second_delete_noticed(self) -> None:
    """A getter answering 'DELETED' after the first 'del' makes the second
    raise 'MissingVariable', so the deleter runs once."""
    draft = Draft()
    draft.body = 'text'
    del draft.body
    self.assertIs(draft.__body__, DELETED)
    with self.assertRaises(MissingVariable):
      del draft.body
    self.assertEqual(draft.__deleted__, 1)
    with self.assertRaises(MissingVariable):
      _ = draft.body

  def test_delete_before_load(self) -> None:
    """A getter raising for a value not loaded yet does not stop the
    deleter."""
    draft = Draft()
    del draft.body
    self.assertEqual(draft.__deleted__, 1)
    self.assertIs(draft.__body__, DELETED)

  def test_resetting_deleter_runs_again(self) -> None:
    """A deleter resetting the value, so that the getter answers again,
    runs on every 'del'."""
    counter = Counter()
    del counter.n
    del counter.n
    self.assertEqual(counter.__deleted__, 2)
    self.assertEqual(counter.n, 0)
