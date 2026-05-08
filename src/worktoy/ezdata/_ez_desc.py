"""``EZDesc`` exposes a single class-creation keyword argument as an
attribute, reading the value from the owning class's namespace."""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from ..core import Object
from ..utilities import maybe
from ..waitaminute import TypeException

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any


class EZDesc(Object):
  """Descriptor that reads a class kwarg from ``__namespace__``.

  Parameters
  ----------
  key : str
      The keyword-argument name to look up.
  *args
      Up to two extra positional arguments: the expected value
      type (defaults to ``bool``), and the default value
      (defaults to ``None``). Extra positional arguments are
      ignored.

  When ``valueType`` is ``bool`` the descriptor returns a literal
  ``True`` or ``False`` for any truthy/falsy value. Otherwise the
  retrieved value must be an instance of ``valueType``;
  ``TypeException`` is raised if not.
  """

  __fallback_type__ = bool
  __keyword_argument__ = None
  __default_value__ = None
  __value_type__ = None

  def _getKwarg(self) -> Any:
    """Return the keyword-argument name configured at construction."""
    return self.__keyword_argument__

  def _getValueType(self) -> Any:
    """Return the configured value type, or the ``bool`` fallback."""
    return maybe(self.__value_type__, self.__fallback_type__)

  def __init__(self, key: str, *args) -> None:
    Object.__init__(self, key, *args)
    self.__keyword_argument__ = key
    type_, defVal, *_ = [*args, None, None]
    self.__value_type__ = type_
    self.__default_value__ = defVal

  def __instance_get__(
      self, instance: Any, owner: type, **kwargs
  ) -> Any:
    """Return the kwarg value associated with ``self.__keyword_argument__``.

    Looks up ``self.instance.__namespace__.__key_args__`` (the
    namespace dictionary set up by ``AbstractMetaclass``).
    """
    classKwargs = maybe(self.instance.__namespace__.__key_args__, dict())
    value = classKwargs.get(self.__keyword_argument__,
                            self.__default_value__)
    valueType = self._getValueType()
    if valueType is bool:
      return True if value else False
    if isinstance(value, valueType):
      return value
    raise TypeException('value', value, valueType)
