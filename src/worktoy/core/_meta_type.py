"""
MetaType is the meta-metaclass for the 'worktoy' library.
"""
#  Apache-2.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING, Generic

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, TypeAlias

  Bases: TypeAlias = tuple[type, ...]
  Space: TypeAlias = dict[str, Any]

  from . import MetaType as MType


class MetaType(type):
  """
  MetaType provides the meta-metaclass for the 'worktoy' library.
  'AbstractMetaclass', and so every metaclass based on it, both
  subclasses 'MetaType' and derives from it, or from a subclass of it
  such as 'KeeMetaMeta', so combining those metaclasses does not raise a
  metaclass conflict. 'SentinelMeta', 'MetaFlow' and '_MetaSlice'
  subclass 'type' directly.

  The keywords of a class statement go two ways. The namespace of the
  metaclass records every one of them, its hooks read the ones that are
  theirs, such as 'trustMeBro', and '__class_init__' receives them all.
  'type.__new__' hands them down the '__init_subclass__' chain of the
  bases as well, which 'MetaType' allows only when a base along the method
  resolution order has an '__init_subclass__' of its own to take them,
  since the chain otherwise ends at once in 'object', which refuses every
  keyword; see 'takesKeywords'. 'AbstractMetaclass' keeps the keywords its
  namespace read out of that call, so the bases see only the keywords
  meant for them, and what a base passes on that none of them takes
  reaches 'object' and is refused there.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __str__(cls, ) -> str:
    return """%s[metaclass=%s]""" % (cls.__name__, cls.__class__.__name__)

  __repr__ = __str__

  #  The 'mmcls' parameter refers this being a meta-metaclass
  #  noinspection PyMethodParameters
  def __new__(mmcls, name: str, bases: Bases, space: Space, **kw) -> MType:
    if '__namespace__' not in space:
      space['__namespace__'] = space
    if kw and not mmcls.takesKeywords(bases):
      #  Only 'object.__init_subclass__' would receive the class keywords,
      #  and it refuses every keyword. The namespace keeps them anyway.
      return super().__new__(mmcls, name, bases, space)
    return super().__new__(mmcls, name, bases, space, **kw)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @classmethod
  def takesKeywords(mmcls, bases: Bases) -> bool:
    """
    The 'takesKeywords' method reports whether a class based on 'bases'
    would hand its class keywords to an '__init_subclass__' other than that
    of 'object', which refuses every keyword. That of 'typing.Generic' does
    not count either, since it hands every keyword on to that of 'object'.
    'EZHook' asks this as well, to refuse at the class statement a class
    keyword that nothing could read.
    """
    for base in bases:
      for cls in base.__mro__:
        if cls is object or cls is Generic:
          continue
        if '__init_subclass__' in cls.__dict__:
          return True
    return False
