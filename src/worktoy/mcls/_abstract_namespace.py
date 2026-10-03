"""
AbstractNamespace is the base class for the custom namespace objects.
"""
#  Apache-2.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from ..utilities import maybe, textFmt, resolveMRO, NoPickle
from ..waitaminute import TypeException
from ..waitaminute.meta import HookException, DuplicateHook, ClaimedName
from .space_hooks import NamespaceHook, ReservedNamespaceHook

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, TypeAlias, Iterator, Union, Self, Optional
  from .space_hooks import AbstractSpaceHook
  from . import AbstractMetaclass as AMeta

  Base: TypeAlias = tuple[type, ...]
  Bases: TypeAlias = tuple[Self, ...]
  Hooks: TypeAlias = list[AbstractSpaceHook]
  MROSpace: TypeAlias = dict[str, list[Any]]
  TypeName: TypeAlias = Union[str, type]


class AbstractNamespace(NoPickle, dict):
  """
  AbstractNamespace defines the custom execution environment used by
  AbstractMetaclass during class construction. It provides a controlled
  and extensible context for evaluating class bodies, enabling advanced
  metaprogramming behavior.

  The core feature of AbstractNamespace is its support for modular
  hook-based behavior. Hooks are instances of subclasses of
  AbstractSpaceHook, declared directly within the body of the namespace
  class. Upon declaration, each hook registers itself with the namespace
  via the descriptor protocol.

  These hooks allow interception and transformation of key events during
  class construction, including symbol access, assignment, and final
  namespace compilation. For details on available hook methods and their
  intended usage, refer to the AbstractSpaceHook documentation.

  This design allows complex functionality, such as decorator-based
  overload resolution and placeholder replacement, to be cleanly
  separated into reusable components. By defining a namespace subclass
  with the desired combination of hooks, users can tailor the behavior of
  class construction without modifying the core metaclass logic.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Class Variables
  __owner_hooks_list_name__: str = '__hook_objects__'
  #  The class keywords the namespace reads off the class statement itself;
  #  its hooks name theirs in their own '__consumed_keys__'.
  __consumed_keys__: tuple[str, ...] = ('_strictMRO',)

  #  Private Variables
  __metaclass__: Optional[AMeta] = None
  __class_name__ = None
  __base_classes__ = None
  __class_mro__ = None
  __key_args__ = None
  __hash_value__ = None
  __compiled_space__ = None
  __deferred_annotations__ = None
  __type_annotations__ = None
  __class_annotations__ = None
  __global_scope__ = None
  __shadow_space__ = None
  __claimed_deletions__ = None

  #  Public Variables
  reservedNameHook = ReservedNamespaceHook()
  nameHook = NamespaceHook()

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def getBases(self) -> Bases:
    return (*self.__base_classes__,)

  def getShadowSpace(self, ) -> dict:
    """
    The 'getShadowSpace' method returns the shadow mapping recording
    every assignment the class body has made, including assignments a
    hook claimed away from the namespace itself. The reading protocol
    falls back to this mapping, so a name bound earlier in the class
    body remains readable even after a hook has claimed it. Without
    this fallback, reading a claimed name would escape to the module
    scope, silently picking up whatever global happens to share the
    name.

    Returns
    -------
    dict
      The mapping of every class-body assignment seen so far, with
      the most recent assignment winning on repeated names.
    """
    return maybe(self.__shadow_space__, dict())

  def getClaimedDeletions(self, ) -> tuple[str, ...]:
    """
    The 'getClaimedDeletions' method returns the names the class body
    deleted after a hook had claimed them, in the order deleted; see
    '__delitem__'.
    """
    return maybe(self.__claimed_deletions__, ())

  def deepGetItem(self, item: str, ) -> Any:
    """
    The 'deepGetItem' method looks up 'item' in the namespace itself,
    then in the combined MRO namespace if absent, raising 'KeyError'
    when neither holds it. A value found in the MRO namespace is the list
    of the values the classes along it contribute; see 'getMROSpace'.
    """
    if dict.__contains__(self, item):
      return dict.__getitem__(self, item)
    mroSpace = self.getMROSpace()
    if item in mroSpace:
      return mroSpace[item]
    raise KeyError(item)

  @classmethod
  def getHookListName(cls, ) -> str:
    return cls.__owner_hooks_list_name__

  def getHooks(self, ) -> Iterator[AbstractSpaceHook]:
    cls = type(self)
    hooks = self.classGetHooks()
    for hook in hooks:
      out = hook.__get__(self, cls, )
      setattr(out, '__space_object__', self)
      yield out

  @classmethod
  def classGetHooks(cls, ) -> Hooks:
    """
    The 'classGetHooks' classmethod returns the hooks registered on this
    namespace class and its bases, de-duplicated in MRO order.
    """
    pvtName = cls.getHookListName()
    out = []
    for base in cls.mro():
      if issubclass(base, dict):
        hooks = getattr(base, pvtName, [])
        for hook in hooks:
          if hook in out:
            continue
          out.append(hook)
    return out

  def getMetaclass(self, ) -> AMeta:
    if TYPE_CHECKING:  # pragma: no cover
      assert isinstance(self.__metaclass__, AMeta)
    return self.__metaclass__

  def getClassName(self, ) -> str:
    return self.__class_name__

  def getKwargs(self, ) -> dict:
    return {**self.__key_args__, **dict()}

  def getConsumedKeywords(self, ) -> tuple[str, ...]:
    """
    The 'getConsumedKeywords' method names the class keywords that this
    namespace and its hooks read off the class statement: '_strictMRO' for
    the namespace itself, 'trustMeBro' for 'NamespaceHook' and the option
    spellings of 'EZData' for 'EZHook'. 'AbstractMetaclass' keeps these out
    of the call to 'type.__new__', and so out of the '__init_subclass__'
    chain of the bases, since they were read here and
    'object.__init_subclass__' would refuse them. Every other keyword goes
    down that chain, for a base to take or 'object' to refuse.
    """
    out = [*self.__consumed_keys__]
    for hook in self.classGetHooks():
      out.extend(hook.__consumed_keys__)
    return (*out,)

  def getMRO(self, ) -> list[type]:
    return self.__class_mro__

  def _getLookupOrder(self, ) -> list[type]:
    """
    The '_getLookupOrder' method returns the classes after the class under
    construction in its method resolution order. A namespace created with
    '_strictMRO=False' for bases admitting no consistent order has none,
    and falls back to each base's own order, bases left to right, with
    repeated classes kept at their first position.
    """
    mro: Optional[list[type]] = self.getMRO()
    if mro is not None:
      return [*mro, ]
    out = []
    for base in self.getBases():
      for cls in base.__mro__:
        if cls not in out:
          out.append(cls)
    return out

  def getMROSpace(self, ) -> MROSpace:
    """
    The 'getMROSpace' method combines the compiled namespaces of every
    base in the MRO into one dict, where each key maps to the list of
    values contributed for it across the MRO. It follows the lookup order
    of '_getLookupOrder', so a namespace without a resolved order still
    answers.
    """
    lookupOrder = self._getLookupOrder()
    mroClasses = [b for b in lookupOrder if hasattr(b, '__namespace__')]
    mroSpaces = [getattr(b, '__namespace__', ) for b in mroClasses]
    compiledSpaces = []
    for space in mroSpaces:
      try:
        compiledSpace = getattr(space, '__compiled_space__')
      except AttributeError:
        continue
      else:
        compiledSpaces.append(compiledSpace)
    out = dict()
    for compiledSpace in compiledSpaces:
      for key, val in compiledSpace.items():
        existing = out.get(key, [])
        out[key] = [*existing, val]
    return out

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  SETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @classmethod
  def addHook(cls, hook: AbstractSpaceHook) -> None:
    """
    The 'addHook' classmethod registers 'hook' on the namespace class,
    raising 'DuplicateHook' if a different hook is already registered
    under the same field name.
    """
    existingHooks = cls.classGetHooks()
    for existingHook in existingHooks:
      existingName = existingHook.getFieldName()
      newName = hook.getFieldName()
      if existingName == newName:
        if existingHook is hook:
          return
        hooks = (existingHook, hook)
        raise DuplicateHook(cls, newName, *hooks)
    pvtName = cls.getHookListName()
    setattr(cls, pvtName, [*existingHooks, hook])

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __init__(self, mcls: AMeta, name: str, bases: Base, **kwargs) -> None:
    """
    Please note that setting the '_strictMRO' keyword argument to 'False'
    allows bases admitting no consistent method resolution order. This
    serves a namespace built directly alone, since no class can be
    created from such bases: 'getMRO' is then None, and the lookup order
    falls back to the own order of each base; see '_getLookupOrder'.
    """
    self.__metaclass__ = mcls
    self.__class_name__ = name
    self.__base_classes__ = [*bases, ]
    self.__key_args__ = kwargs or {}
    baseNames = tuple(b.__name__ for b in bases)
    self.__hash_value__ = hash((name, *baseNames, mcls.__name__))
    try:
      self.__class_mro__ = resolveMRO(*bases, )
    except TypeError as typeError:
      #  MRO inconsistency is the only 'TypeError' that 'resolveMRO' is
      #  capable of raising. For this reason, we omit the brittle
      #  inspection check of the exception message. The reason
      #  'resolveMRO' will never raise any other 'TypeError' is because it
      #  would always raise 'AttributeError' first.
      if kwargs.get('_strictMRO', True):
        raise typeError
    for hook in self.getHooks():
      setattr(hook, '__space_object__', self)
      hook.preparePhase(self)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __getitem__(self, key: str, **kwargs) -> Any:
    """
    The '__getitem__' method fetches 'key', then runs every hook's
    'getItemPhase' before returning the value or re-raising the
    'KeyError'. A key absent from the namespace but present in the
    shadow space resolves to its shadow value: the class body can
    read back a name even after a hook has claimed the assignment.
    """
    #  The miss is kept apart from the value, which a class body may well
    #  bind to a 'KeyError' of its own.
    missing = None
    try:
      val = dict.__getitem__(self, key)
    except KeyError as keyError:
      shadow = self.getShadowSpace()
      if key in shadow:
        val = shadow[key]
      else:
        val = missing = keyError
    for hook in self.getHooks():
      setattr(hook, '__space_object__', self)
      try:
        hook.getItemPhase(key, val)
      except Exception as exception:
        raise HookException(exception, self, key, val, hook)
    if missing is not None:
      raise missing
    return val

  def __setitem__(self, key: str, val: Any, **kwargs) -> None:
    """
    The '__setitem__' method offers each hook's 'setItemPhase' a chance
    to handle 'key' first; the namespace performs the default assignment
    only when no hook claims it. Every assignment is also recorded in
    the shadow space, claimed or not, keeping the name readable from
    the class body either way.
    """
    shadow = self.getShadowSpace()
    shadow[key] = val
    self.__shadow_space__ = shadow
    try:
      oldVal = dict.__getitem__(self, key)
    except KeyError:
      oldVal = None
    for hook in self.getHooks():
      setattr(hook, '__space_object__', self)
      if hook.setItemPhase(key, val, oldVal):
        break  # Breaks out of the loop if handled by hook.
    else:  # If no 'break', the 'else' block is executed.
      dict.__setitem__(self, key, val)

  def __delitem__(self, key: str, **kwargs) -> None:
    """
    The '__delitem__' method runs 'del' in the class body. The name is
    removed from the namespace and from the shadow space alike, so a later
    read in the class body no longer finds it, as in a plain class. A name
    the class body never bound raises 'KeyError', which the interpreter
    reports as a 'NameError'.

    A name whose latest binding a hook claimed cannot be deleted, since
    the hook registered the value as it was bound. The deletion is
    recorded instead, and 'compile' raises 'ClaimedName' for it as the
    class is created. Raising here would be lost: the interpreter replaces
    any exception a deletion in a class body raises with its own
    'NameError', saying that the name is not defined.
    """
    shadow = self.getShadowSpace()
    if key not in shadow and not dict.__contains__(self, key):
      raise KeyError(key)
    if self._isClaimed(key):
      self.__claimed_deletions__ = (*self.getClaimedDeletions(), key)
    shadow.pop(key, None)
    if dict.__contains__(self, key):
      dict.__delitem__(self, key)

  def _isClaimed(self, key: str) -> bool:
    """
    The '_isClaimed' method reports whether a hook claimed the latest
    binding of 'key' in the class body: the shadow space records every
    binding, while the namespace holds only those no hook claimed, so the
    two disagree exactly when the latest one was claimed.
    """
    shadow = self.getShadowSpace()
    if not dict.__contains__(self, key):
      return True if key in shadow else False
    value = dict.__getitem__(self, key)
    return True if shadow.get(key, value) is not value else False

  def __str__(self, ) -> str:
    bases = self.getBases()
    spaceName = type(self).__name__
    clsName = self.getClassName()
    baseNames = ', '.join([base.__name__ for base in bases])
    mclsName = self.getMetaclass().__name__
    info = """Namespace object of type: '%s' created by the '__prepare__' 
    method on metaclass: '%s' with bases: (%s) to create class: '%s'."""
    return textFmt(info % (spaceName, mclsName, baseNames, clsName))

  def __repr__(self, ) -> str:
    bases = self.getBases()
    spaceName = type(self).__name__
    clsName = self.getClassName()
    mclsName = self.getMetaclass().__name__
    baseNames = '%s' % ', '.join([base.__name__ for base in bases])
    args = """%s, '%s', (%s)""" % (mclsName, clsName, baseNames)
    kwargs = [(k, v) for (k, v) in self.getKwargs().items()]
    kwargStr = ', '.join(['%s=%s' % (k, str(v)) for (k, v) in kwargs])
    if kwargStr:
      kwargStr = ', %s' % kwargStr
    return """%s(%s%s)""" % (spaceName, args, kwargStr)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def preCompile(self, namespace: Optional[dict] = None) -> dict:
    """
    The 'preCompile' method runs each hook's 'preCompilePhase' over the
    starting namespace dict (a fresh dict when none is given) and returns
    the accumulated result, which 'compile' then merges the class-body
    names into.
    """
    if namespace is None:
      namespace = dict()
    elif not isinstance(namespace, dict):
      raise TypeException('namespace', namespace, dict)
    for hook in self.getHooks():
      setattr(hook, '__space_object__', self)
      namespace = hook.preCompilePhase(namespace)
    return namespace

  def compile(self, namespace: Optional[dict] = None) -> dict:
    """
    The 'compile' method builds the final namespace passed to
    'type.__new__': it runs 'preCompile', merges in the class-body names,
    runs 'postCompile', and records the metaclass, namespace, and
    keyword arguments. Subclasses may reimplement 'preCompile' or
    'postCompile' as needed, but must not reimplement this method. A
    class body that deleted a name a hook claimed raises 'ClaimedName'
    here, before anything is compiled; see '__delitem__'.
    """
    for key in self.getClaimedDeletions():
      raise ClaimedName(self.getClassName(), key)
    namespace = self.preCompile(namespace)
    for (key, val) in dict.items(self, ):
      namespace[key] = val
    namespace = self.postCompile(namespace)
    namespace['__metaclass__'] = self.getMetaclass()
    namespace['__namespace__'] = self
    namespace['__keyword_arguments__'] = self.getKwargs()
    self.__compiled_space__ = namespace
    return namespace

  def postCompile(self, namespace: dict) -> dict:
    """
    The 'postCompile' method runs each hook's 'postCompilePhase' over the
    assembled namespace and returns the result, which 'compile' hands to
    the metaclass. This is where 'LoadSpaceHook' turns collected
    overloads into 'Dispatcher' objects.
    """
    for hook in self.getHooks():
      setattr(hook, '__space_object__', self)
      namespace = hook.postCompilePhase(namespace)
    return namespace
