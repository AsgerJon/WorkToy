"""
RiskWarning warns that an object received at a name is carried out as
promised, at a risk.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from ..utilities import textFmt
from . import WorkToyWarning

if TYPE_CHECKING:  # pragma: no cover, no mutate
  from typing import Any


class RiskWarning(WorkToyWarning, RuntimeWarning):
  """
  Some things a library promises to carry out are still unwise to ask
  of it. Refusing them would break the promise, and carrying them out
  in silence leaves the user to find the cost alone. RiskWarning is
  given in that case: what was asked is carried out as promised, and
  the warning names the object received, the name it was received at,
  and what going on with it risks, as 'TypeException' names the object
  and the name where it refuses.

    RiskWarning('price', price, 'a till that pays the customer').warn()

  It is offered to the projects built upon 'worktoy' as much as to
  'worktoy' itself: a project subclasses it in a package of its own,
  as the 'WorkToyWarning' docstring describes.

  Attributes
  ----------
  varName : str
    The name of the variable or argument that received the object.
  actualObject : Any
    The object that was received.
  risk : str
    What going on with that object risks, worded to end the sentence
    'This is promised to function correctly, but risks ...'.
  """

  __slots__ = ('varName', 'actualObject', 'risk')

  def __init__(self, name: str, obj: Any, risk: str) -> None:
    RuntimeWarning.__init__(self, )
    self.varName = name
    self.actualObject = obj
    self.risk = risk

  def __str__(self) -> str:
    infoSpec = """Received object at name '%s': %s of type '%s'. This
    is promised to function correctly, but risks %s!"""
    objStr = repr(self.actualObject)
    if len(objStr) > 50:
      objStr = """%s...""" % objStr[:47]
    clsType = type(self.actualObject).__name__
    info = infoSpec % (self.varName, objStr, clsType, self.risk)
    return textFmt(info)

  __repr__ = __str__
