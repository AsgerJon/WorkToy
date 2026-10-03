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
  validation or derived state. A class keyword that is none of the
  options goes down the '__init_subclass__' chain to the bases, as in
  'class Point(EZData, Tagged, tag='hello')' where 'Tagged' takes 'tag';
  with no base having an '__init_subclass__' of its own, such a keyword,
  a misspelled option for instance, raises 'ClassKeywordError' at the
  class statement.

  In return the class receives auto-generated '__init__',
  '__iter__', '__len__', '__eq__', '__setattr__', '__delattr__',
  'asDict', 'asTuple', 'replace', '__match_args__', and the display
  dunders. The '__len__' gives the number of fields, which '__iter__'
  yields. The '__setattr__' casts every field assignment the way
  '__init__' does, or refuses it on a frozen class, which additionally
  receives '__hash__'. A class body defining '__init__', '__iter__',
  '__len__', '__eq__', '__hash__', an ordering method, '__setattr__' or
  '__delattr__' raises 'ReservedMethodError', while a plain base, one not
  built by 'EZMeta', may define them, as a mixin written against the
  same protocol does, and the generated methods take precedence over
  them. A class body binding an attribute EZData sets on every class
  itself, such as '__kw_only__', raises 'ReservedAttributeError'. The
  optional names '__field_pairs__', 'asDict', 'asTuple', 'replace',
  '__repr__', '__str__' and '__match_args__' are generated only where
  neither the class body nor a base, EZData or plain, supplies one: the
  class body's own wins, then the first one written by hand along the
  bases. '__post_init__' is the hook for validation and derived state.
  Every field therefore holds an instance of its field type, though not
  necessarily of exactly that type: a 'bool' given to an 'int' field
  stays a 'bool'. Ordered classes receive the four comparison dunders.
  Several EZData classes with fields may be combined as bases. See
  'EZHook.postCompilePhase' for the full generation contract.

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

    def __len__(self) -> int: ...

    def __repr__(self) -> str: ...

    def __eq__(self, other: Any) -> bool: ...

    def __hash__(self) -> int: ...

    def __lt__(self, other: Self) -> bool: ...

    def __le__(self, other: Self) -> bool: ...

    def __gt__(self, other: Self) -> bool: ...

    def __ge__(self, other: Self) -> bool: ...

    def __setattr__(self, key: str, value: Any) -> None: ...

    def __delattr__(self, key: str) -> None: ...
