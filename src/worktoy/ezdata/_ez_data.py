"""
EZData is the base class for 'worktoy' dataclasses.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from . import EZMeta
from ..core import Object

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, Iterator, Self


class EZData(Object, metaclass=EZMeta):
  """
  EZData is the base class users subclass to declare a worktoy
  dataclass. Subclasses place their fields in the class body as
  'EZField[T](...)' instances, optionally pass build-option
  keywords ('frozen=True', 'ordered=True', 'kwOnly=True' or any
  of their synonyms), and optionally define '__post_init__' for
  validation or derived state.

  In return the class receives auto-generated '__init__',
  '__iter__', '__eq__', '__delattr__', 'asDict', 'asTuple',
  'replace', '__match_args__', and the display dunders. Frozen
  classes additionally receive '__hash__' and a rejecting
  '__setattr__'; ordered classes receive the four comparison
  dunders. See 'EZHook.postCompilePhase' for the full
  generation contract.

  Example
  -------
      class Point2D(EZData):
        x = EZField[float](0.0)
        y = EZField[float](0.0)

      class Circle(EZData, frozen=True, kwOnly=True):
        center = EZField[Point2D]()
        radius = EZField[float](1.0)
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  if TYPE_CHECKING:  # pragma: no cover
    #  These stubs shadow the dunder methods 'EZHook' generates at
    #  class creation. They exist only so type-checkers see accurate
    #  signatures for 'EZData' instances; the factory-built methods in
    #  '_ez_hook.py' hint to 'Any' because 'Self' is invalid there.
    def __init__(self, *args, **kwargs) -> None: ...

    def __iter__(self) -> Iterator[Any]: ...

    def __repr__(self) -> str: ...

    def __eq__(self, other: Any) -> bool: ...

    def __hash__(self) -> int: ...

    def __lt__(self, other: Self) -> bool: ...

    def __le__(self, other: Self) -> bool: ...

    def __gt__(self, other: Self) -> bool: ...

    def __ge__(self, other: Self) -> bool: ...

    def __setattr__(self, key: str, value: Any) -> None: ...

    def __delattr__(self, key: str) -> None: ...
