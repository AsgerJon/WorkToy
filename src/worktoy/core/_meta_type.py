"""
MetaType is the meta-metaclass for the 'worktoy' library.
"""
#  Apache-2.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, TypeAlias
  from . import MetaType as MType

  Bases: TypeAlias = tuple[type, ...]
  Space: TypeAlias = dict[str, Any]


class _Chill:
  __skip_hash__: bool = True

  @classmethod
  def __init_subclass__(cls, **kwargs) -> None:
    """
    Why are we still here?
    """
    type.__setattr__(cls, '__skip_hash__', False)
    #  '_Chill' is last in the resolution order of every class it is a base
    #  of, so nothing follows it but 'object', whose '__init_subclass__'
    #  takes no keyword, and the chain ends here.


class MetaType(type):
  """
  MetaType provides the meta-metaclass for the 'worktoy' library.
  'AbstractMetaclass', and so every metaclass based on it, both
  subclasses 'MetaType' and derives from it, or from a subclass of it
  such as 'KeeMetaMeta', so combining those metaclasses does not raise a
  metaclass conflict. 'SentinelMeta', 'MetaFlow' and '_MetaSlice'
  subclass 'type' directly.
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
    lastBase = (bases or (object,))[-1]
    if not isinstance(lastBase, MetaType):
      bases: tuple[type, ...] = (*bases, _Chill)
    bases: tuple[type, ...] = (*(b for b in bases if b is not object),)
    spaceState: bool = True if '__namespace__' in space else False
    if not spaceState:
      space['__namespace__'] = space
    cls = super().__new__(mmcls, name, bases, space, **kw)
    if not spaceState:
      del space['__namespace__']
    return cls

  def __init__(cls, name: str, bases: Bases, space: Space, **kw) -> None:
    type.__setattr__(cls, '__skip_hash__', False)
