"""
StorageCollision is raised when a class body declares a box whose field
name derives a storage name another box of the class already uses.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from ...utilities import textFmt
from .. import WorkToyException


class StorageCollision(WorkToyException, SyntaxError):
  """
  StorageCollision is raised when a class body declares a box, an
  'AttriBox' or a class based on it, whose field name derives a storage
  name that another box of the same class already uses. A box stores the
  value of its field on each instance under the private name of the
  field, and names that differ only in how their words are joined or
  capitalised, 'fooBar' and 'foo_bar', or 'X' and 'x', derive one private
  name. Two such boxes used to share one slot without a word, so reading
  one gave the value of the other. The class body fails at the second of
  the two instead, as the class is created. It subclasses 'SyntaxError',
  as the other refusals of a class-body line do.

  Attributes
  ----------
  ownerName : str
    The name of the class under construction.
  fieldName : str
    The name of the box that was refused.
  existingName : str
    The name of the box already storing at the storage name.
  storageName : str
    The storage name both names derive.
  """

  __slots__ = ('ownerName', 'fieldName', 'existingName', 'storageName')

  def __init__(
      self,
      owner: type,
      fieldName: str,
      existingName: str,
      storageName: str,
  ) -> None:
    self.ownerName = owner.__name__
    self.fieldName = fieldName
    self.existingName = existingName
    self.storageName = storageName
    SyntaxError.__init__(self, )
    #  The traceback of a 'SyntaxError' shows 'msg' rather than 'str()'.
    self.msg = str(self)

  def __str__(self) -> str:
    spec = """The class body of '%s' declares a box at '%s' storing at
    '%s', where the box at '%s' already stores: the two names derive one
    private name. Rename one of the two."""
    names = (
      self.ownerName,
      self.fieldName,
      self.storageName,
      self.existingName,
    )
    return textFmt(spec % names)

  __repr__ = __str__
