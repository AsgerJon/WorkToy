"""The dataclass cohort: the same small dataclasses declared with
'dataclasses' and with 'worktoy.ezdata', each as its documentation
shows it: a point of two floats, mutable and frozen, an account that
checks itself in '__post_init__', an ordered version of two integers,
a bag with a list of its own and a circle holding a point.

Beside them stand the point, the account, the bag and the circle as a
class of boxes writes them: a 'BaseObject' whose attributes are
'AttriBox' fields, and one whose attributes are 'FixBox' fields, set
once. The boxes generate no method, so such a class writes its own
constructor, here with '@overload', and checks itself there.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from dataclasses import dataclass, field

from worktoy.desc import AttriBox, FixBox
from worktoy.dispatch import overload
from worktoy.ezdata import EZData, EZField
from worktoy.mcls import BaseObject


@dataclass
class DataPoint:
  """Baseline: a dataclass of two floats with defaults."""

  x: float = 0.0
  y: float = 0.0


@dataclass(frozen=True)
class FrozenDataPoint:
  """Baseline: the same, frozen. A frozen dataclass cannot be based on
  one that is not, so it is a class of its own."""

  x: float = 0.0
  y: float = 0.0


@dataclass
class DataAccount:
  """Baseline: a dataclass that checks itself as it is made."""

  balance: float = 0.0

  def __post_init__(self) -> None:
    if self.balance < 0:
      raise ValueError('a balance cannot be negative')


@dataclass(order=True)
class DataVersion:
  """Baseline: an ordered dataclass of two integers."""

  major: int = 0
  minor: int = 0


@dataclass
class DataBag:
  """Baseline: a dataclass with a list of its own for each instance."""

  items: list = field(default_factory=list)


@dataclass
class DataCircle:
  """Baseline: a dataclass holding another, built for each instance."""

  center: DataPoint = field(default_factory=DataPoint)
  radius: float = 1.0


class EZPoint(EZData):
  """worktoy: an 'EZData' of two floats, declared by their values."""

  x = 0.0
  y = 0.0


class FrozenEZPoint(EZPoint, frozen=True):
  """worktoy: the same, frozen, as a subclass of the mutable one, which
  its instances compare equal to."""


class EZAccount(EZData):
  """worktoy: an 'EZData' that checks itself as it is made."""

  balance = 0.0

  def __post_init__(self) -> None:
    if self.balance < 0:
      raise ValueError('a balance cannot be negative')


class EZVersion(EZData, ordered=True):
  """worktoy: an ordered 'EZData' of two integers."""

  major = 0
  minor = 0


class EZBag(EZData):
  """worktoy: an 'EZData' with a list of its own for each instance."""

  items = EZField[list]()


class EZCircle(EZData):
  """worktoy: an 'EZData' holding another, built for each instance."""

  center = EZField[EZPoint]()
  radius = 1.0


class BoxPoint(BaseObject):
  """worktoy: a 'BaseObject' of two 'AttriBox' fields, taking both by
  position or neither."""

  x = AttriBox[float](0.0)
  y = AttriBox[float](0.0)

  @overload(float, float)
  def __init__(self, x: float, y: float) -> None:
    self.x = x
    self.y = y

  @overload()
  def __init__(self) -> None:
    pass


class BoxAccount(BaseObject):
  """worktoy: a class of one 'AttriBox' that checks itself as it is
  made, in the constructor it writes."""

  balance = AttriBox[float](0.0)

  @overload(float)
  def __init__(self, balance: float) -> None:
    self.balance = balance
    if self.balance < 0:
      raise ValueError('a balance cannot be negative')


class BoxBag(BaseObject):
  """worktoy: an 'AttriBox' building a list of its own for each
  instance, at its first read."""

  items = AttriBox[list]()


class BoxCircle(BaseObject):
  """worktoy: an 'AttriBox' building a point for each instance, at its
  first read."""

  center = AttriBox[BoxPoint]()
  radius = AttriBox[float](1.0)


class FixPoint(BaseObject):
  """worktoy: a 'BaseObject' of two 'FixBox' fields, each set once by
  the constructor."""

  x = FixBox[float](0.0)
  y = FixBox[float](0.0)

  @overload(float, float)
  def __init__(self, x: float, y: float) -> None:
    self.x = x
    self.y = y

  @overload()
  def __init__(self) -> None:
    pass


class FixAccount(BaseObject):
  """worktoy: a class of one 'FixBox' that checks itself as it is
  made."""

  balance = FixBox[float](0.0)

  @overload(float)
  def __init__(self, balance: float) -> None:
    self.balance = balance
    if self.balance < 0:
      raise ValueError('a balance cannot be negative')


class FixBag(BaseObject):
  """worktoy: a 'FixBox' building a list of its own for each instance,
  at its first read."""

  items = FixBox[list]()


class FixCircle(BaseObject):
  """worktoy: a 'FixBox' building a point for each instance, at its
  first read."""

  center = FixBox[FixPoint]()
  radius = FixBox[float](1.0)
