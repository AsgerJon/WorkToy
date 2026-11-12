"""
TestSpace is the namespace 'TestMeta' prepares for a test class. It
keeps the names 'doCleanups' and 'debug' for the library.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from ..mcls import BaseSpace
from ..waitaminute.meta import ReservedName

if TYPE_CHECKING:  # pragma: no cover, no mutate
  from typing import Any


class TestSpace(BaseSpace):
  """
  A test base built by 'TestMeta' has chosen that the bodies of its
  test classes do not bind 'doCleanups' or 'debug', two of the places
  from which 'BaseTest' reports the failed 'subTest' blocks of a test,
  each test method being the third. The place to say so is the line of
  the class body that tries: the builder is then shown that line, not
  the end of a class statement. TestSpace is the namespace 'TestMeta'
  prepares for a test class. It lets 'TestMeta' bind the two names
  before the class body runs and refuses every binding of either by
  the class body.

    class StrictTest(BaseTest, metaclass=TestMeta):
      pass

    class TestDice(StrictTest):

      def doCleanups(self) -> None:  # refused here, with 'ReservedName'
        self.table.close()

  Implementation
  --------------

  '__setitem__' raises 'ReservedName' for the keys 'doCleanups' and
  'debug' unless the keyword '_root' is true, which
  'TestMeta.__prepare__' passes and a class body cannot. Every other
  binding goes on to 'BaseSpace', hooks included.
  """

  def __setitem__(self, key: str, value: Any, **kwargs) -> None:
    """
    Every binding of the class body passes here, and 'doCleanups' and
    'debug' are the two names the class body may not bind.

    Parameters
    ----------

    key : str
      The name bound.

    value : Any
      The value bound.

    Raises
    ------

    ReservedName
      The class body binds 'doCleanups' or 'debug'.
    """
    if key in ('doCleanups', 'debug') and not kwargs.get('_root', False):
      raise ReservedName(key)
    return BaseSpace.__setitem__(self, key, value, **kwargs)
