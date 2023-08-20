"""TypeNameSpace provides a namespace class specifically for the
AbstractType."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

import inspect
import os

from icecream import ic

from worktoy.worktype import AbstractNameSpace

ic.configureOutput(includeContext=True)

Keys = type({}.keys())
Values = type({}.values())
Items = type({}.items())


class TypeNameSpace(AbstractNameSpace):
  """TypeNameSpace provides a namespace class specifically for the
  AbstractType."""

  def __init__(self, name, bases, ) -> None:
    """Implicit alternative to __init__"""
    self._iterContents = None
    self._bases = None
    self._className = None
    self._contents = {}
    AbstractNameSpace.__init__(self, name, bases)

  def _setName(self, name: str) -> None:
    if not isinstance(name, str):
      raise TypeError
    self._className = name

  def _setBases(self, bases: tuple) -> None:
    if not isinstance(bases, tuple):
      raise TypeError
    self._bases = bases

  def _explicitSetter(self, key: str, val: object) -> None:
    self._contents[key] = val

  def _explicitGetter(self, key: str) -> object:
    if key not in self._contents:
      raise KeyError
    val = self._contents.get(key, None)
    if val is None:
      raise KeyError(key)
    return val

  def _explicitDeleter(self, key: str) -> None:
    """
    Deletes the value associated with the given key from the TypeNameSpace.
    """

  def keys(self) -> Keys:
    """Implementation of keys method"""
    return self._contents.keys()

  def values(self) -> Values:
    """Implementation of values method"""
    return self._contents.values()

  def items(self) -> Items:
    """Implementation of items"""
    return self._contents.items()

  #
  # def __iter__(self, ) -> TypeNameSpace:
  #   """Implementation of iteration"""
  #   self._iterContents = [k for k in self.keys()]
  #   return self
  #
  # def __next__(self, ) -> object:
  #   """Implementation of iteration"""
  #   try:
  #     return self._iterContents.pop(0)
  #   except IndexError:
  #     self._iterContents = None
  #     raise StopIteration

  def protocolify(self, *__, **_) -> None:
    """
    Generates a protocol version of the class based on the methods
    and attributes contained within this namespace. The generated
    protocol class will be saved as a `.py` file in the
    `./_typingversions` directory.

    Args:
    - className (str): Name of the class for which the protocol
                       version is to be generated.

    Returns:
    - None

    Raises:
    - KeyError: If a method or attribute in the namespace is not
                found during the generation process.
    """
    if self._className[0] == '_':
      return
    protocolCode = ['\"\"\"LMAO\"\"\"',
                    "from __future__ import annotations", '',
                    "from typing import Protocol, Never", "", '',
                    "class %s(Protocol):" % self._className,
                    '  \"\"\"LMAO\"\"\"']

    # Iterate over the namespace to identify methods
    # and generate their abstract versions
    for name, attribute in self.items():
      if callable(attribute):
        # Use the inspect module to get the signature of the function
        signature = inspect.signature(attribute)

        # protocolCode.append("  @abstractmethod")
        protocolCode.append(
          ("  def %s%s:" % (name, signature)).replace("""'""", ''))
        protocolCode.append("    ...")
        protocolCode.append("")

    # Create the _typingversions directory if it doesn't exist
    here = os.path.dirname(__file__)
    there = os.path.join(here, '_typingversions')
    filePath = os.path.join(there, '_%s.py' % self._className.lower())
    # os.makedirs("./_typingversions", exist_ok=True)

    # Saving the generated code to a file
    with open(filePath, 'w') as file:
      file.write('\n'.join(protocolCode))
