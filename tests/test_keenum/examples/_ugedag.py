"""
Ugedag provides an example implementation of 'KeeNum' by enumerating
weekdays in Danish. The value type is a custom class for the purpose of
testing.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.keenum import KeeNum, Kee
from worktoy.mcls import BaseMeta, BaseSpace
from . import Dag

if TYPE_CHECKING:  # pragma: no cover
  pass


class _FreeLoader(metaclass=BaseMeta):
  """
  Non-KeeNum class added as a second baseclass.
  """


class _HitchHiker(metaclass=BaseMeta):
  """
  Non-KeeNum class added as a second baseclass.
  """
  __namespace__ = BaseSpace(BaseMeta, '_HitchHiker', (), )
  __namespace__['__member_type__'] = int


class Hverdag(KeeNum, _HitchHiker, _FreeLoader):
  MANDAG = Kee[Dag]('Mandag')
  TIRSDAG = Kee[Dag]('Tirsdag')
  ONSDAG = Kee[Dag]('Onsdag')
  TORSDAG = Kee[Dag]('Torsdag')
  FREDAG = Kee[Dag]('Fredag')


class Weekend(KeeNum, _HitchHiker, _FreeLoader):
  LORDAG = Kee[Dag]('Lørdag')
  SONDAG = Kee[Dag]('Søndag')


class Ugedag(Hverdag, Weekend):
  """
  Ugedag provides an example implementation of 'KeeNum' by enumerating
  weekdays in Danish. The value type is a custom class for the purpose of
  testing.
  """
