"""CopyClass provides a metaclass which changes calling a class from
instantiation to copy. This means that calling a class, the return value
is not an instance of the class but a copy of the class. """
#  Copyright (c) 2023 Asger Jon Vistisen
#  MIT Licence
from __future__ import annotations


class CopyClass(type):
  """CopyClass provides a metaclass which changes calling a class from
  instantiation to copy. This means that calling a class, the return value
  is not an instance of the class but a copy of the class. """

  #  Copyright (c) 2023 Asger Jon Vistisen
  #  MIT Licence
  def __call__(cls, *args, **kwargs):
    # Create a new class with the provided arguments
    newClass = type("NewClass", cls.__bases__, cls.__dict__.copy())
    return newClass
