"""
NamespaceHook filters names used in the namespace system.
"""
#  Apache-2.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from types import FunctionType

from ...core.sentinels import METACALL
from ...waitaminute.meta import QuestionableSyntax, DelException
from ...waitaminute.meta import UnboundClassHook, ShadowedClassHook
from . import AbstractSpaceHook

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, TypeAlias, Optional

  NearMiss: TypeAlias = tuple[str, str]


class NamespaceHook(AbstractSpaceHook):
  """
  NamespaceHook intercepts names added to the namespace and filters out
  near-miss identifiers that resemble critical Python dunder methods.
  These mistakes often go unnoticed, leading to subtle bugs or broken
  protocol support.

  This hook raises a 'QuestionableSyntax' exception when such names are
  detected during assignment in the namespace.

  Purpose
  -------
  Many magic methods in Python have specific names that must be spelled
  exactly. If a user misspells one by inserting or omitting underscores,
  the name is silently ignored by Python and treated as an ordinary
  attribute, sometimes shadowing a builtin or behaving unexpectedly.

  Near-miss examples
  ------------------
  Intended name    Mistyped name    Notes
  '__set_name__'   '__setname__'    Misses descriptor registration
  '__getitem__'    '__get_item__'   Breaks item access in dict-like APIs
  '__setitem__'    '__set_item__'   Same as above
  '__delitem__'    '__del_item__'   Silent failure of delete protocol
  '__delete__'     '__del__'        High risk: '__del__' ties to GC hooks

  These errors are difficult to diagnose because they usually do not
  raise any errors directly. Instead, they silently fail to participate
  in expected behaviors or override builtin methods.

  Shadowed class hooks
  --------------------
  'AbstractMetaclass' calls each routed '__class_*__' hook from its own
  implementation of the operation, '__class_len__' from '__len__'. A
  metaclass based on it that implements the operation again takes it
  over, so the hook would never run: 'KeeMeta' measures, iterates and
  searches its members itself, and 'EZMeta' its fields. A class body
  binding such a hook raises 'ShadowedClassHook' at the line binding it,
  naming the metaclass and the method that take the operation over.
  '__class_init__' is exempt, since it is not called from an operation:
  every metaclass '__init__' hands over to the inherited one, which
  calls it.

  Usage
  -----
  To use 'NamespaceHook', declare it in your namespace class:

      class Space(AbstractNamespace):
        nameHook = NamespaceHook()
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Class Variables
  #  'trustMeBro' is read by '_validateDel' and goes no further.
  __consumed_keys__ = ('trustMeBro',)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @classmethod
  def _getClassDunders(cls) -> list[str]:
    """
    The '_getClassDunders' method returns the class-level dunder hook
    names that 'AbstractMetaclass' routes to its own implementations.
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
      #  implementations of the dunder methods, such that derived
      #  may implement the methods to achieve behaviour otherwise
      #  requiring metaclass reimplementation.
    ]

  @classmethod
  def _getNearMisses(cls) -> list[NearMiss]:
    """
    The '_getNearMisses' method returns the '(intended, mistyped)' name
    pairs that the hook rejects on sight.
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
    The '_getChainedHooks' method returns the class hooks that no
    metaclass method takes over: '__class_init__' is called by
    'AbstractMetaclass.__init__', which every metaclass '__init__' hands
    over to, rather than from an operation a metaclass may implement
    itself.
    """
    return ['__class_init__']

  @staticmethod
  def _getOperation(hookName: str) -> str:
    """
    The '_getOperation' method returns the name of the operation a
    routed hook is called from, '__len__' for '__class_len__'.
    """
    return '__%s__' % hookName[len('__class_'):-2]

  def _getShadowingMetaclass(self, hookName: str) -> Optional[type]:
    """
    The '_getShadowingMetaclass' method returns the metaclass that
    implements the operation of 'hookName' itself, so that the hook would
    never be called, or None when the operation is left to
    'AbstractMetaclass', which calls the hook. The metaclass building the
    class and its bases before 'AbstractMetaclass' are searched, since a
    metaclass derived from 'KeeMeta' inherits its '__len__'. A metaclass
    not based on 'AbstractMetaclass' calls no hook, and takes none over.
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

  @classmethod
  def _validateName(cls, name: str) -> bool:
    """
    The '_validateName' method compares 'name' against the near-miss
    list and raises 'QuestionableSyntax' on a match, otherwise returning
    False so the assignment proceeds.
    """
    nearMisses = cls._getNearMisses()
    for nearMiss in nearMisses:
      if name == nearMiss[1]:
        raise QuestionableSyntax(*nearMiss, )
    return False

  def _validateDel(self, ) -> bool:
    """
    The '_validateDel' method reports whether the current class is
    allowed to implement '__del__', which it is only when the class was
    declared with a truthy 'trustMeBro' keyword (for example
    'trustMeBro=True'). An absent keyword, or a falsy value such as
    'trustMeBro=False', denies it.
    """
    kwargs = self.space.getKwargs()
    return True if kwargs.get('trustMeBro', False) else False

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  PARENT METHODS   # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def setItemPhase(self, key: str, val: Any, old: Any = None, ) -> bool:
    """
    The 'setItemPhase' method screens each name as it is bound. A
    '__del__' definition raises 'DelException' unless the class opted in
    with 'trustMeBro'; any near-miss dunder raises 'QuestionableSyntax'.
    Returns False for an acceptable name so the namespace stores it
    normally.

    Parameters
    ----------
    key : str
        The name being bound in the class body.
    val : Any
        The value being bound.
    old : Any, optional
        The previous value bound under 'key', if any.

    Returns
    -------
    bool
        False, so the namespace performs the default assignment.

    Raises
    ------
    DelException
        If '__del__' is defined without the 'trustMeBro' keyword.
    ShadowedClassHook
        If 'key' is a routed '__class_*__' hook name whose operation the
        metaclass implements itself, so the hook would never be called.
    UnboundClassHook
        If 'key' is a routed '__class_*__' hook name bound to a plain
        function or staticmethod rather than a classmethod.
    QuestionableSyntax
        If 'key' is a near-miss spelling of a known dunder.
    """
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
      if isinstance(val, (FunctionType, staticmethod)):
        #  The metaclass invokes these hooks as bound classmethods. A
        #  plain function receives no class binding: most hooks fail
        #  with a confusing 'TypeError' at call time, and
        #  '__class_call__' silently swallows the first constructor
        #  argument as the class.
        clsName = self.space.getClassName()
        raise UnboundClassHook(clsName, key)
    return self._validateName(key)

  def preCompilePhase(self, compiledSpace: dict) -> dict:
    """
    The 'preCompilePhase' method seeds the class-dunder hook names with
    the 'METACALL' sentinel, but only where neither the class body nor a
    class along the method resolution order supplies one, a plain mixin
    included. This is what lets 'AbstractMetaclass' route
    '__class_len__', '__class_iter__', and the rest to its own
    implementations.

    Parameters
    ----------
    compiledSpace : dict
        The namespace dict being assembled.

    Returns
    -------
    dict
        The same dict, with 'METACALL' filled in for any unhandled
        class-dunder name.
    """
    dunderNames = self._getClassDunders()
    mro = self.space._getLookupOrder()
    for name in dunderNames:
      if dict.__contains__(self.space, name):
        continue
      if any(name in cls.__dict__ for cls in mro):
        continue
      compiledSpace[name] = METACALL
    return compiledSpace
