"""WorkToy - Core - StateAware
Implementation of ready awareness. If a class has a complicated
constructor, this mixin class provides a ready method that should be
invoked at the end of the construction. Subclass can implement this method
to provide notification when an instance is ready."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from worktoy.core import FLAG

#
# class StateAware:
#   """WorkToy - Core - StateAware
#   Implementation of ready awareness. If a class has a complicated
#   constructor, this mixin class provides a ready method that should be
#   invoked at the end of the construction. Subclass can implement this
#   method
#   to provide notification when an instance is ready."""
#
#   __instance_ready__ = Flag[False, bool]
#
#   def __init__(self, *args, **kwargs) -> None:
#     self._listeners = []
#
#   def completed(self, *args, **kwargs) -> object:
#     """Should be invoked by subclasses at the conclusion of instance
#     creation."""
#     e = kwargs.get('_error', None)
#     if e is None:
#       for arg in args:
#         if isinstance(arg, Exception):
#           e = arg
#           break
#     if isinstance(e, Exception):
#       raise e
#     if e is not None:
#       raise Exception(e)
#
#     self.__instance_ready__ = True
#     return True
