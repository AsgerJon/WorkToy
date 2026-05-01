"""
Diagnostic facilitates inspection of overload objects.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.dispatch import overload
from worktoy.mcls import BaseSpace, BaseMeta

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, Optional


class DiagnosticSpace(BaseSpace):
  """
  This namespace monitors and logs 'overload' entries as they are
  encountered during the class body execution.
  """

  __exp_load__: bool = False
  __overload_diagnostics__: Optional[tuple[overload, ...]] = None

  def _getOverloadDiagnostics(self, **kwargs) -> tuple[overload, ...]:
    if self.__overload_diagnostics__ is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      self.__overload_diagnostics__ = ()
      return self._getOverloadDiagnostics(_recursion=True, )
    return self.__overload_diagnostics__

  def _registerOverloadDiagnostic(self, load: overload) -> None:
    existing = self._getOverloadDiagnostics()
    self.__overload_diagnostics__ = (*existing, load,)

  def __getitem__(self, key: str, **kwargs) -> Any:
    try:
      value = BaseSpace.__getitem__(self, key)
    except KeyError as keyError:
      if """'overload'""" == str(keyError):
        self.__exp_load__ = True
      raise keyError
    else:
      return value

  def __setitem__(self, key: str, value: Any, **kwargs) -> None:
    if self.__exp_load__:
      self._registerOverloadDiagnostic(value)
    self.__exp_load__ = False
    BaseSpace.__setitem__(self, key, value)

  def compile(self, namespace: dict = None) -> dict:
    namespace = BaseSpace.compile(self, namespace)
    namespace['overloadDiagnostics'] = (*self._getOverloadDiagnostics(),)
    return namespace


class DiagnosticMetaclass(BaseMeta):
  """
  This class exists solely to carry the 'DiagnosticSpace' and its
  hook.
  """

  @classmethod
  def __prepare__(mcls, name: str, bases: tuple, **kw) -> dict:
    return DiagnosticSpace(mcls, name, bases, **kw)


class Diagnostic(metaclass=DiagnosticMetaclass):
  """
  This class exists solely to be the target of the test, which is to
  inspect the 'str' representations of the 'overload' objects as they
  are seen by the 'DiagnosticHook'.
  """

  testing = True

  @overload()
  def method(self) -> None:
    pass

  @overload(int)
  def method(self, x: int) -> None:
    pass

  @overload.flex(str, int)
  def method(self, *args) -> None:
    pass
