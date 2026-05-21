"""
SubclassException subclasses 'TypeError' and provides a custom exception
raised to indicate that a given subclass was not a subclass of a given
baseclass.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from ..utilities import textFmt

if TYPE_CHECKING:  # pragma: no cover
  pass


class SubclassException(TypeError):
  """
  SubclassException subclasses 'TypeError' and provides a custom exception
  raised to indicate that a given subclass was not a subclass of a given
  baseclass.

  Attributes
  ----------
  subClass: type
    The class that was expected to be a subclass of the base class.
  baseClass: type
    The base class that the subClass was expected to be a subclass of.

  Examples
  --------
  >>> from typing import TypeAlias, Type
  >>> Number: TypeAlias = Type[int]
  >>> class Fraction:
  >>>  __slots__ = ('numerator', 'denominator', )
  >>>
  >>>  def __init__(self, numerator: Number, denominator: Number) -> None:
  >>>    if not isinstance(numerator, int):
  >>>      raise SubclassException(type(numerator), int)
  >>>    if not isinstance(denominator, int):
  >>>      raise SubclassException(type(denominator), int)
  >>>    if not denominator:
  >>>      raise ZeroDivisionError('Received zero denominator!')
  >>>    self.numerator = numerator
  >>>    self.denominator = denominator
  >>> try:
  ...   fraction = Fraction(69, '420')  # type: ignore[arg-type]
  ... except SubclassException as subclassException:
  ...   print(subclassException)
  """

  __slots__ = ('subClass', 'baseClass')

  def __init__(self, subClass: type, baseClass: type) -> None:
    """Initialize the exception with the object and expected base class."""
    self.subClass, self.baseClass = subClass, baseClass
    TypeError.__init__(self, )

  def __str__(self) -> str:
    """
    Return a string representation of the SubclassException object.
    """
    infoSpec = """Expected class '%s' to be a subclass of '%s'!"""
    clsName = self.subClass.__name__
    baseName = self.baseClass.__name__
    info = infoSpec % (clsName, baseName)
    return textFmt(info)

  __repr__ = __str__
