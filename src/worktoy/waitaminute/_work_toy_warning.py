"""
WorkToyWarning is the common base of every warning in the
'worktoy.waitaminute' package, and the one place a warning is given.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

import os
import sys
import warnings

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover, no mutate
  from typing import Any


class WorkToyWarning(Warning):
  """
  A library that warns must point the warning at the line its user
  wrote, not at a line of its own, or the user is told that something
  is wrong without being told where. Python leaves this to every call
  of 'warnings.warn', which takes a 'stacklevel' counted by hand: one
  frame too few or too many and the warning names the wrong file.
  WorkToyWarning is the common base of the warnings of 'worktoy', as
  'WorkToyException' is of its exceptions, and its 'warn' method is the
  only place where a warning is given, so that no caller counts frames.
  Where an exception is raised, a warning is given:

    raise TypeException('price', price, int)
    RiskWarning('price', price, 'a till that pays the customer').warn()

  A warning class lists WorkToyWarning first and the builtin category
  it keeps after it, 'FutureWarning' for a deprecation, so the filters
  of the 'warnings' package keep working and one filter on
  WorkToyWarning covers every warning of the library. Like
  'TypeException', a warning is handed the things it is about, kept in
  its slots, and words the sentence itself in '__str__'.

  A project built upon 'worktoy' gives warnings of its own by
  subclassing a warning of the family in a package of its own. The
  warning then steps over the files of that project as well, and lands
  on the line of the project's user.

  Implementation
  --------------

  The 'warn' method walks out of the call stack until it stands on a
  frame that '_isInternal' does not claim: one whose file is neither
  inside a package of '_roots' nor part of the import system. It
  reports the warning for that file and line through
  'warnings.warn_explicit', with the registry of that frame's globals,
  which is what 'warnings.warn' does once it has counted. The filters,
  once for each line included, therefore apply as they do to any
  warning. The '_nameOf' method names a thing handed to a warning as a
  user would write it.
  """

  __slots__ = ()

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @classmethod
  def _roots(cls, ) -> tuple:
    """
    The '_roots' method gives the folder of every package that is the
    home of this class or of a warning class it subclasses, each folder
    once. The home of a class is the top-level package its '__module__'
    names. A class at home in a lone file, or in a package that was
    never imported, adds nothing.
    """
    roots = []
    for base in cls.__mro__:
      if not issubclass(base, WorkToyWarning):
        continue
      home = base.__module__.split('.')[0]
      if home not in sys.modules:
        continue
      package = sys.modules[home]
      if not hasattr(package, '__path__'):
        continue
      for path in package.__path__:
        root = os.path.abspath(path) + os.sep
        if root not in roots:
          roots.append(root)
    return (*roots,)

  @classmethod
  def _isInternal(cls, frame: Any) -> bool:
    """
    The '_isInternal' method reports whether a frame runs a file inside
    one of the folders of '_roots', or a file of the import system,
    which stands between an 'import' statement and the '__getattr__' of
    the package it imports from.
    """
    fileName = frame.f_code.co_filename
    if fileName.startswith('<frozen importlib'):
      return True
    return True if fileName.startswith(cls._roots()) else False

  @staticmethod
  def _isPlaced(thing: Any) -> bool:
    """
    The '_isPlaced' method reports whether 'thing' is a descriptor that
    knows the class it was placed on and the name it was placed at.
    """
    if not hasattr(thing, '__field_owner__'):
      return False
    if not hasattr(thing, '__field_name__'):
      return False
    return True if thing.__field_owner__ is not None else False

  @classmethod
  def _nameOf(cls, thing: Any) -> str:
    """
    The '_nameOf' method gives the name a user would write for 'thing',
    so that a warning is handed the thing itself and words it alone. A
    'str' is taken as the name. A class or function is named by its
    package and qualified name, with the private files left out, since
    a user imports from the package: 'worktoy.keenum.KeeBox', not
    'worktoy.keenum._kee_box.KeeBox'. A placed descriptor is named
    after its owner and its field. Anything else is shown by 'repr'.
    """
    if isinstance(thing, str):
      return thing
    if hasattr(thing, '__qualname__') and hasattr(thing, '__module__'):
      parts = thing.__module__.split('.')
      public = [part for part in parts if not part.startswith('_')]
      return str.join('.', [*public, thing.__qualname__])
    if cls._isPlaced(thing):
      owner = cls._nameOf(thing.__field_owner__)
      return """%s.%s""" % (owner, thing.__field_name__)
    return repr(thing)

  def warn(self, ) -> None:
    """
    The 'warn' method gives this warning at the nearest line that is
    neither a line of the library nor of a project whose warning this
    is. At the bottom of the stack it settles for the line it has.
    """
    frame = sys._getframe(1)
    while self._isInternal(frame) and frame.f_back is not None:
      frame = frame.f_back
    space = frame.f_globals
    if '__warningregistry__' not in space:
      space['__warningregistry__'] = dict()
    if '__name__' in space:
      name = space['__name__']
    else:
      #  This branch is reached by the following:
      #  - Text run by 'exec' in globals that hold no '__name__'
      name = '<string>'
    warnings.warn_explicit(
      self,
      type(self),
      frame.f_code.co_filename,
      frame.f_lineno,
      name,
      space['__warningregistry__'],
      space,
    )
