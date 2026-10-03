"""
ShadowedClassHook is raised when a class body binds a routed
'__class_*__' hook under a metaclass that implements the operation
itself, so the hook would never be called.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from ...utilities import textFmt, NoPickle


class ShadowedClassHook(NoPickle, SyntaxError):
  """
  ShadowedClassHook is raised when a class body binds one of the routed
  '__class_*__' hook names under a metaclass that implements the
  operation itself. 'AbstractMetaclass' calls each hook from its own
  implementation of the operation, '__class_len__' from '__len__' for
  instance, so a metaclass based on it that implements '__len__' again
  takes the operation over, and a '__class_len__' in the body of one of
  its classes would never run. 'KeeMeta' and 'KeeFlagsMeta' implement
  most of the operations for their enumerations themselves, and 'EZMeta'
  iterates, measures and searches the fields of its classes itself. Such
  a hook used to be accepted without a word, and a '__class_call__' in an
  enumeration body even broke the class statement with an unrelated
  error, since the hook ran as the members were created. The class body
  fails at the line binding the hook instead. It subclasses
  'SyntaxError', as the other refusals of a class-body line do.

  Attributes
  ----------
  className : str
    The name of the class under construction.
  hookName : str
    The routed hook name the class body binds.
  metaclassName : str
    The name of the metaclass implementing the operation, which may be a
    base of the metaclass building the class.
  methodName : str
    The name of the method that metaclass implements in place of calling
    the hook, such as '__len__' for '__class_len__'.
  """

  __slots__ = ('className', 'hookName', 'metaclassName', 'methodName',)

  def __init__(
      self,
      className: str,
      hookName: str,
      metaclassName: str,
      methodName: str,
  ) -> None:
    self.className = className
    self.hookName = hookName
    self.metaclassName = metaclassName
    self.methodName = methodName
    SyntaxError.__init__(self, )
    #  The traceback of a 'SyntaxError' shows 'msg' rather than 'str()'.
    self.msg = str(self)

  def __str__(self) -> str:
    spec = """The class body of '%s' binds '%s', but the metaclass '%s'
    implements '%s' itself and does not call the hook, so the binding
    would never run."""
    names = (self.className, self.hookName, self.metaclassName,
             self.methodName)
    return textFmt(spec % names)

  __repr__ = __str__
