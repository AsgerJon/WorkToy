"""
NamespaceHook filters names used in the namespace system.
"""
#  Apache-2.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from ...core.sentinels import METACALL
from ...dispatch import overload, Dispatcher
from ...waitaminute.meta import QuestionableSyntax, DelException
from ...waitaminute.meta import UnboundClassHook, ShadowedClassHook
from ...waitaminute.meta import SlotsRefused
from . import AbstractSpaceHook

if TYPE_CHECKING:  # pragma: no cover, no mutate
  from typing import Any, TypeAlias, Optional

  NearMiss: TypeAlias = tuple[str, str]


class NamespaceHook(AbstractSpaceHook):
  """
  Python silently ignores a dunder method it does not know, so a
  misspelling such as '__setname__' for '__set_name__' or
  '__get_item__' for '__getitem__' leaves the class without the protocol
  and without any error. A finalizer, '__del__', ties the class to the
  garbage collector and is often written where '__delete__' was meant.
  The class-level hooks that 'AbstractMetaclass' consults, such as
  '__class_len__' for 'len(cls)', only work as classmethods, and a
  metaclass ahead of 'AbstractMetaclass' in the resolution order that
  implements the operation takes it over for its classes, which then
  cannot implement the hook. And '__slots__' cannot work in a worktoy
  class, whose instances always keep a '__dict__'.
  Each of these mistakes must fail at the line making it.

  Implementation
  --------------

  'setItemPhase' raises 'SlotsRefused' for '__slots__',
  'QuestionableSyntax' for a known near miss, and 'DelException' for
  '__del__' unless the class is declared with the class keyword
  'trustMeBro=True'. A class-level hook bound to anything but a
  classmethod, overloads declared as classmethods or 'METACALL' raises
  'UnboundClassHook', and one whose operation a metaclass based on
  'AbstractMetaclass' implements itself raises 'ShadowedClassHook'.
  'preCompilePhase' sets every class-level hook that neither the body nor
  a base supplies to 'METACALL', and holds the hook the nearest base
  supplies to the same rule as the body.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @classmethod
  def _getClassDunders(cls) -> list[str]:
    """
    The hook must know which names are the class-level hooks
    'AbstractMetaclass' consults.

    Returns
    -------

    list[str]
      The routed hook names.
    """
    return [
      '__class_call__',
      '__class_init__',
      '__class_instancecheck__',
      '__class_subclasscheck__',
      '__class_str__',
      '__class_repr__',
      '__class_iter__',
      '__class_next__',
      '__class_bool__',
      '__class_contains__',
      '__class_len__',
      '__class_hash__',
      #  '__class_eq__',  Exhibits highly undefined behaviour!
      #  '__class_ne__',  See above
      #  '__class_getitem__',  See footnote below
      '__class_setitem__',
      '__class_delitem__',
      '__class_getattr__',
      '__class_setattr__',
      '__class_delattr__',
      #  NOTE: '__class_getitem__' is commented out, rather than
      #  omitted, allowing this explanatory note to be found easily.
      #
      #  Since Python 3.7, support for the '__class_getitem__' became a
      #  feature of the interpreter itself. In fact, it inspired the
      #  implementation of all of the above class level hooks. Uniquely
      #  for '__class_getitem__', if it is defined on the class,
      #  the metaclass implementation of '__getitem__' will not be
      #  called.
      #
      #  This behaviour is opposite to the other hooks, as they
      #  are implemented here. 'AbstractMetaclass' provides
      #  implementations of the dunder methods, such that its classes
      #  may implement the methods to achieve behaviour otherwise
      #  requiring metaclass reimplementation.
    ]

  @classmethod
  def _getNearMisses(cls) -> list[NearMiss]:
    """
    The hook must know which misspellings to refuse, each with the name it
    stands for, for the message.

    Returns
    -------

    list[tuple[str, str]]
      The '(intended, mistyped)' pairs.
    """
    return [
      ('__set_name__', '__setname__'),  # NOQA, miss-spelled name
      ('__getitem__', '__get_item__'),
      ('__setitem__', '__set_item__'),
      ('__delitem__', '__del_item__'),
    ]

  @classmethod
  def _getChainedHooks(cls) -> list[str]:
    """
    '__class_init__' is not called from an operation a metaclass might
    implement, but by 'AbstractMetaclass.__init__', which every metaclass
    '__init__' reaches, so no metaclass takes it over.

    Returns
    -------

    list[str]
      The hooks exempt from 'ShadowedClassHook'.
    """
    return ['__class_init__']

  @staticmethod
  def _getOperation(hookName: str) -> str:
    return '__%s__' % hookName[len('__class_'):-2]

  def _getShadowingMetaclass(self, hookName: str) -> Optional[type]:
    """
    A metaclass ahead of 'AbstractMetaclass' in the resolution order that
    implements an operation, as 'KeeMeta' implements '__len__', takes the
    operation over for its classes, whether or not it hands on to
    'AbstractMetaclass', so a class-level hook of that operation is
    refused, and the body binding it must be told which metaclass took
    over. A metaclass behind 'AbstractMetaclass' takes nothing over, since
    'AbstractMetaclass' answers first.

    Implementation
    --------------

    The resolution order of the metaclass up to 'AbstractMetaclass' is
    searched for a class implementing the operation. 'AbstractMetaclass'
    is imported inside, since it loads after the hooks its namespace
    declares.

    Parameters
    ----------

    hookName : str
      The name of the hook.

    Returns
    -------

    type or None
      The metaclass taking the operation over, or 'None'.
    """
    if hookName in self._getChainedHooks():
      return None
    #  Local import: 'AbstractMetaclass' loads after the hooks, which its
    #  namespace declares.
    from .. import AbstractMetaclass
    mcls = self.space.getMetaclass()
    mro = getattr(mcls, '__mro__', ())
    if AbstractMetaclass not in mro:
      return None
    operation = self._getOperation(hookName)
    for klass in mro[:mro.index(AbstractMetaclass)]:
      if operation in klass.__dict__:
        return klass
    return None

  @staticmethod
  def _isClassHookValue(value: Any) -> bool:
    """
    The metaclass calls a class-level hook on the class, so the hook is a
    classmethod, overloads declared as classmethods, which become a
    dispatcher bound to the class, or 'METACALL'.

    Parameters
    ----------

    value : Any
      What the class body binds at a hook name, or what the nearest base
      holding the name holds there.

    Returns
    -------

    bool
      Whether the value may stand at a hook name.
    """
    if value is METACALL or isinstance(value, classmethod):
      return True
    if isinstance(value, (overload, Dispatcher)):
      return True if value.getMethodKind() is classmethod else False
    return False

  @classmethod
  def _validateName(cls, name: str) -> bool:
    nearMisses = cls._getNearMisses()
    for nearMiss in nearMisses:
      if name == nearMiss[1]:
        raise QuestionableSyntax(*nearMiss, )
    return False

  def _validateDel(self, ) -> bool:
    """
    A class that does mean to define '__del__' needs a way to say so.

    Implementation
    --------------

    The class keyword 'trustMeBro' is read from the namespace; a truthy
    value allows '__del__'.

    Returns
    -------

    bool
      Whether '__del__' is allowed.
    """
    kwargs = self.space.getKwargs()
    return True if kwargs.get('trustMeBro', False) else False

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  PARENT METHODS   # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def setItemPhase(self, key: str, val: Any, old: Any = None, ) -> bool:
    """
    Each name of the class body must be screened at the line binding it.

    Parameters
    ----------

    key : str
      The name bound.

    val : Any
      The value bound.

    old : Any, optional
      The value the name held, or 'None'.

    Returns
    -------

    bool
      'False', so the namespace stores an accepted name.

    Raises
    ------

    SlotsRefused
      '__slots__' is bound.

    DelException
      '__del__' without 'trustMeBro=True'.

    ShadowedClassHook
      A class-level hook whose operation the metaclass implements itself.

    UnboundClassHook
      A class-level hook that is neither a classmethod, overloads declared
      as classmethods nor 'METACALL'.

    QuestionableSyntax
      A near miss of a dunder method.
    """
    if key == '__slots__':
      raise SlotsRefused(self.space.getClassName())
    if key == '__del__':
      if self._validateDel():
        return False
      mcls = self.space.getMetaclass()
      name = self.space.getClassName()
      bases = self.space.getBases()
      raise DelException(mcls, name, bases, self.space)
    if key in self._getClassDunders():
      shadowing = self._getShadowingMetaclass(key)
      if shadowing is not None:
        clsName = self.space.getClassName()
        operation = self._getOperation(key)
        raise ShadowedClassHook(clsName, key, shadowing.__name__, operation)
      if not self._isClassHookValue(val):
        #  The metaclass invokes these hooks as bound classmethods. A
        #  plain function receives no class binding: most hooks fail
        #  with a confusing 'TypeError' at call time, and
        #  '__class_call__' silently swallows the first constructor
        #  argument as the class. An '@overload' of instance methods
        #  becomes a 'Dispatcher' expecting an instance the metaclass
        #  never passes.
        clsName = self.space.getClassName()
        raise UnboundClassHook(clsName, key)
    return self._validateName(key)

  def preCompilePhase(self, compiledSpace: dict) -> dict:
    """
    'AbstractMetaclass' tells a defined hook from an undefined one by
    comparing with 'METACALL', so every hook must hold a value, and a hook
    the class inherits must be held to the rule of the class body, since a
    plain base holding it was screened by no worktoy namespace.

    Implementation
    --------------

    A hook neither the body nor a class along the resolution order holds
    is set to 'METACALL'; the first worktoy class of a hierarchy therefore
    receives the 'METACALL' entries, and its subclasses inherit them. For
    a hook the body does not bind, the nearest class along the order
    holding it is checked by the rule of the body, whatever built that
    class; the hook of a worktoy base passes, its own namespace having
    screened it. A binding a hook claimed, as overloads are, counts as
    bound: what a base holds there is not checked, and the hook is set to
    'METACALL' until the claiming hook writes its value, as
    'LoadSpaceHook' writes the dispatcher after the names of the body are
    merged.

    Parameters
    ----------

    compiledSpace : dict
      The dictionary being assembled.

    Returns
    -------

    dict
      The dictionary.

    Raises
    ------

    UnboundClassHook
      The nearest base holding a hook holds something other than a
      classmethod, overloads declared as classmethods or 'METACALL', as a
      plain base may.
    """
    dunderNames = self._getClassDunders()
    mro = self.space._getLookupOrder()
    shadow = self.space.getShadowSpace()
    for name in dunderNames:
      if dict.__contains__(self.space, name):
        continue
      if name in shadow:
        #  This branch is reached by the following:
        #  - The class body bound the name to what a hook claimed, as
        #    overloads declared as classmethods, which replace what a base
        #    holds there
        compiledSpace[name] = METACALL
        continue
      for cls in mro:
        if name in cls.__dict__:
          self._validateInheritedHook(cls, name)
          break
      else:
        compiledSpace[name] = METACALL
    return compiledSpace

  def _validateInheritedHook(self, base: type, hookName: str) -> None:
    value = base.__dict__[hookName]
    if not self._isClassHookValue(value):
      clsName = self.space.getClassName()
      raise UnboundClassHook(clsName, hookName, base.__name__)
