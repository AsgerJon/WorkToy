"""TypeNameSpace provides a namespace class specifically for the
AbstractType."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

import inspect
import os

from worktoy.worktype import AbstractNameSpace

Keys = type({}.keys())
Values = type({}.values())
Items = type({}.items())


class TypeNameSpace(AbstractNameSpace):
  """TypeNameSpace provides a namespace class specifically for the
  AbstractType."""

  def __init__(self, name: str, bases: tuple[type]) -> None:
    super().__init__()
    if not isinstance(name, str):
      raise TypeError
    if not isinstance(bases, tuple):
      raise TypeError
    self._iterContents = None
    self._contents = {}
    self._className = name
    self._bases = bases

  def _explicitSetter(self, key: str, val: object) -> None:
    self._contents[key] = val

  def _explicitGetter(self, key: str) -> object:
    val = self._contents.get(key, None)
    if val is None:
      raise KeyError(key)
    return val

  def _explicitDeleter(self, key: str) -> None:
      """
      Deletes the value associated with the given key from the TypeNameSpace.
      """
      if key in self._contents:
          del self._contents[key]

  def keys(self) -> Keys:
    """Implementation of keys method"""
    return self._contents.keys()

  def values(self) -> Values:
    """Implementation of values method"""
    return self._contents.values()

  def items(self) -> Items:
    """Implementation of items"""
    return self._contents.items()

  def __iter__(self, ) -> TypeNameSpace:
    """Implementation of iteration"""
    self._iterContents = [k for k in self.keys()]
    return self

  def __next__(self, ) -> object:
    """Implementation of iteration"""
    try:
      return self._iterContents.pop(0)
    except IndexError:
      self._iterContents = None
      raise StopIteration

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
    className = self._className

    protocolClassName = "%sProtocol" % className
    protocolCode = ["from typing import Protocol",
                    "from abc import abstractmethod", "",
                    "class %s(Protocol):" % protocolClassName]

    # Iterate over the namespace to identify methods
    # and generate their abstract versions
    for name, attribute in self.items():
      if callable(attribute):
        # Use the inspect module to get the signature of the function
        signature = inspect.signature(attribute)

        protocolCode.append("  @abstractmethod")
        protocolCode.append("  def %s%s -> None:" % (name, signature))
        protocolCode.append("    ...")
        protocolCode.append("")

    # Create the _typingversions directory if it doesn't exist
    os.makedirs("./_typingversions", exist_ok=True)

    # Saving the generated code to a file
    file_path = os.path.join("./_typingversions", f"{protocolClassName}.py")
    with open(file_path, 'w') as file:
      file.write('\n'.join(protocolCode))
