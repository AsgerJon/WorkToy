"""
SourceBlock subclasses 'CodeBlock' and provides a code block showing the
source code for a given class or function using the 'inspect.getsource'
function.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from inspect import getsource
from typing import TYPE_CHECKING

from ..desc import Field
from ..dispatch import overload
from ..waitaminute import MissingVariable, TypeException
from . import CodeBlock

if TYPE_CHECKING:  # pragma: no cover
  from typing import TypeAlias, Union, Optional

  MaybeStr: TypeAlias = Optional[str]
  StrField: TypeAlias = Union[str, Field]
  MaybeType: TypeAlias = Optional[type]
  TypeField: TypeAlias = Union[type, Field]


class SourceBlock(CodeBlock):
  """
  SourceBlock subclasses 'CodeBlock' and provides a code block showing the
  source code for a given class or function using the 'inspect.getsource'
  function.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Private Variables
  __example_class__: MaybeType = None

  #  Public Variables
  exampleClass: TypeField = Field()

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @exampleClass.GET
  def _getExampleClass(self, ) -> type:
    if self.__example_class__ is None:
      cls = type(self)
      desc = cls.exampleClass
      raise MissingVariable(desc, '__example_class__', type)
    if isinstance(self.__example_class__, type):
      return self.__example_class__
    name, value = '__example_class__', self.__example_class__
    raise TypeException(name, value, type)

  @exampleClass.onSet
  def _createSourceCode(self, ) -> None:
    """
    This method uses 'inspect.getsource' to get the source code of the
    example class and sets it as the content of the block.
    """
    infoSpec = """```python\n%s\n```"""
    info = infoSpec % getsource(self.exampleClass)
    self.__source_code__ = info

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  SETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @exampleClass.SET
  def _setExampleClass(self, value: type) -> None:
    if not isinstance(value, type):
      name, value = 'value', value
      raise TypeException(name, value, type)
    self.__example_class__ = value

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @overload(type)
  def __init__(self, exampleClass: type) -> None:
    self.exampleClass = exampleClass
