"""
UncheckableType is raised when a type declared for values is a class that
'isinstance' refuses to check anything against.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from ..utilities import textFmt
from . import WorkToyException

if TYPE_CHECKING:  # pragma: no cover, no mutate
  from typing import Any, Optional


class UncheckableType(WorkToyException, TypeError):
  """
  UncheckableType is raised when a type declared for values is a class
  that 'isinstance' refuses to check anything against, as 'typing.Any' is
  from Python 3.11 on, and a 'Protocol' that is not marked
  '@runtime_checkable' is on every version. An overload signature matches
  each call with 'isinstance', and a box checks each value with it, so
  such a type would pass the declaration and then fail at every call or
  access with the interpreter's own 'TypeError'. The declaration is
  refused instead, at the line writing it. It differs from
  'TypeException', which is raised for a value of the wrong type, in that
  here the declared type itself cannot be used. It subclasses
  'TypeError', as the refusal of 'isinstance' does.

  Attributes
  ----------
  entry : Any
    The type declared.
  declaration : str
    The declaration as written: the entries of an overload signature, as
    '(int, Any)', or the subscript of a box, as 'AttriBox[Any]'.
  position : int or None
    The position of the type in an overload signature, or None for the
    field type of a box.
  refusal : TypeError
    The 'TypeError' 'isinstance' raised for the type.
  """

  __slots__ = ('entry', 'declaration', 'position', 'refusal')

  def __init__(
      self,
      entry: Any,
      declaration: str,
      position: Optional[int],
      refusal: TypeError,
  ) -> None:
    self.entry = entry
    self.declaration = declaration
    self.position = position
    self.refusal = refusal
    TypeError.__init__(self, )

  def __str__(self) -> str:
    entryName = getattr(self.entry, '__name__', None) or str(self.entry)
    if self.position is None:
      #  This branch is reached by the following:
      #  - The type was declared as the field type of a box
      spec = """The box '%s' declares '%s' as its field type, which
      'isinstance' refuses: %s."""
      info = spec % (self.declaration, entryName, self.refusal)
    else:
      #  This branch is reached by the following:
      #  - The type was declared in an overload signature
      spec = """The signature '%s' declares '%s' at position %d, which
      'isinstance' refuses: %s."""
      names = (self.declaration, entryName, self.position, self.refusal)
      info = spec % names
    rule = """Every value a declared type receives is checked with
    'isinstance', so the type is a class 'isinstance' accepts; 'typing.Any',
    and a 'Protocol' that is not '@runtime_checkable', are none."""
    return textFmt(info, rule)

  __repr__ = __str__
