"""
The 'mostSpecificBase' function takes any number of classes and returns the
most specific class that is a base class of all the provided classes.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations


def mostSpecificBase(*classes: type, **kwargs) -> type:
  """
  The 'mostSpecificBase' function takes any number of classes and returns the
  most specific class that is a base class of all the provided classes.

  :param classes: A variable number of class types.
  :return: The most specific base class common to all provided classes.
  """
  if not classes:
    return object

  if len(classes) == 1:
    return classes[0]

  sample = kwargs.get('sample', None)
  if sample is None:
    sample = [b for b in classes[0].__mro__ if b is not object]
    prev = object
    return mostSpecificBase(*classes[1:], sample=sample, prev=prev)

  if not isinstance(sample, list):
    from worktoy.waitaminute import TypeException
    raise TypeException('sample', sample, list)

  prev = kwargs.get('prev', )
  if prev is None:
    from worktoy.waitaminute import TypeException
    raise TypeException('prev', prev, type)

  if not sample:
    return prev

  base = sample.pop(0)

  for cls in classes:
    if not issubclass(cls, base):
      return prev

  return mostSpecificBase(*classes, sample=sample, prev=base)
