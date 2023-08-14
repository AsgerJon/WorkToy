"""ParseData simplifies the parsing of arguments. Subclasses should define
an object instantiated on an arbitrary combination of positional and
keyword arguments and populate a number of fields matching the required
values. """
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import Any, Never, Union

from worktoy.core import maybe
from worktoy.parsing import Signature

Keys = Union[list[str], str]


class _Mapping:
  """Mapping functionalities"""

  def __init__(self, *args, **kwargs) -> None:
    self._args = [arg for arg in args]
    self._kwargs = kwargs

  def _getArgs(self) -> list:
    """Getter-function for the list of positional arguments"""
    return self._args

  def _getKwargs(self) -> dict[str, Any]:
    """Getter-function for the dictionary containing the keyword
    arguments."""
    return self._kwargs

  def __getitem__(self, key: str, defVal: Any = None) -> Any:
    """Implementation of mapping applied to the keyword arguments"""
    if key not in self._getKwargs().keys():
      if defVal is not None:
        return defVal
      raise KeyError(key)
    return dict.__getitem__(self._getKwargs(), key)

  def __setitem__(self, *args, **kwargs) -> Never:
    """Illegal setter operation"""
    from worktoy.waitaminute import ReadOnlyError
    raise ReadOnlyError('kwargs')

  def __delitem__(self, key: str) -> Never:
    """Illegal deleter operation"""
    from worktoy.waitaminute import ProtectedPropertyError
    raise ProtectedPropertyError('kwargs')

  def keys(self) -> list[str]:
    """Implementation of keys reflecting the keyword arguments"""
    return [k for (k, v) in self._getKwargs().items()]

  def values(self) -> list[Any]:
    """Implementation of values reflecting the keyword arguments"""
    return [v for (k, v) in self._getKwargs().items()]

  def items(self, ) -> list[tuple[str, Any]]:
    """Implementation of items reflecting the keyword arguments"""
    return [(k, v) for (k, v) in self._getKwargs().items()]

  def get(self, key: str, defVal: Any = None) -> Any:
    """Implementation of get"""
    out = dict.get(self._getKwargs(), key, defVal)
    if out is not None:
      return out
    raise KeyError(key)


class AbstractParser:
  """ParseData simplifies the parsing of arguments. Subclasses should define
  an object instantiated on an arbitrary combination of positional and
  keyword arguments and populate a number of fields matching the required
  values.

  The Signature class provides instances capable of extracting values from
  instances of AbstractParser.

  class A(WorkType):
    # Using metaclass=WorkTypeMeta through the WorkType intermediary
    x = BaseField()
    y = BaseField()
  parser >> variableSignature: Signature -> variableValue
  parser >> signatureKey: str -> variableValue

  __init__(self, *args, **kwargs)
  """

  def __init__(self, *args, **kwargs) -> None:
    self._args = [arg for arg in args]
    self._kwargs = kwargs
    self._signatureDict = {}

  def _getArgs(self) -> list:
    """Getter-function for args"""
    return self._args

  def _setArgs(self, *_) -> None:
    """Illegal setter function"""
    from worktoy.waitaminute import ReadOnlyError
    raise ReadOnlyError('args')

  def _delArgs(self, ) -> Never:
    """Illegal deleter function"""
    from worktoy.waitaminute import ProtectedPropertyError
    raise ProtectedPropertyError('args')

  def _getKwargs(self) -> dict[str, Any]:
    """Getter-function for kwargs"""
    return self._kwargs

  def _setKwargs(self, *_) -> None:
    """Illegal setter function"""
    from worktoy.waitaminute import ReadOnlyError
    raise ReadOnlyError('kwargs')

  def _delKwargs(self, ) -> Never:
    """Illegal deleter function"""
    from worktoy.waitaminute import ProtectedPropertyError
    raise ProtectedPropertyError('kwargs')

  def _getSignatureDict(self) -> dict[str, Signature]:
    """Getter-function for signatureDict"""
    return self._signatureDict

  def _setSignatureDict(self, value: dict[str, Signature]) -> None:
    """Illegal setter function"""
    if self._signatureDict is not None:
      from worktoy.waitaminute import ReadOnlyError
      raise ReadOnlyError('signatureDict')
    self._signatureDict = value

  def _delSignatureDict(self, ) -> Never:
    """Illegal deleter function"""
    from worktoy.waitaminute import ProtectedPropertyError
    raise ProtectedPropertyError('signatureDict')

  args = property(_getArgs, _setArgs, _delArgs)
  kwargs = property(_getKwargs, _setKwargs, _delKwargs)
  signatureDict = property(_getSignatureDict,
                           _setSignatureDict,
                           _delSignatureDict)

  def _getPosType(self, type_: type) -> Any:
    """Getter-function for the first positional argument of the given
    type. The positional argument will not be available through this
    method again. If not such argument can be found, this method returns
    None."""
    for (i, arg) in enumerate(self._getArgs()):
      if isinstance(arg, type_):
        return arg

  def _getKwargType(self, keys: Keys, type_: type = None) -> Any:
    """Getter-function for the keyword argument defined on any of the
    given keys. If a type is provided the argument will not be returned if
    it is not an instance of the given type."""
    if isinstance(keys, str):
      return self._getKwargType([keys], type_)
    if type_ is None or isinstance(type_, type):
      type_ = object

    for key in keys:
      val = self._getKwargs().get(key, None)
      if val is not None and isinstance(val, type_):
        return val

  def _setKeySignature(self, key: str, signature: Signature) -> None:
    """Setter-function for the signature at the given key."""
    self.signatureDict.update({key: signature})

  def _keySignature(self, key: str) -> Signature:
    """Returns the signature associated with the given key."""
    return self.signatureDict[key]

  def _signatureValue(self, signature: Signature) -> Any:
    """Returns the value of the AbstractParser instance at the given
    signature."""
    kwargVal = self._getKwargType(signature.key, signature.type)
    posVal = self._getPosType(signature.type)
    defVal = signature.defVal
    val = maybe(kwargVal, posVal, defVal)
    if isinstance(val, str):
      return val
    raise TypeError

  def _keyValue(self, key) -> Any:
    """Returns the value of the parser at the signature defined at the
    given key."""
    return self._signatureValue(self._keySignature(key))
