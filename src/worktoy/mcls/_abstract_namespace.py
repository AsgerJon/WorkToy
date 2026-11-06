"""
AbstractNamespace is the base class for the custom namespace objects.
"""
#  Apache-2.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from ..utilities import maybe, textFmt, resolveMRO
from ..waitaminute import TypeException
from ..waitaminute.meta import HookException, DuplicateHook, ClaimedName
from .space_hooks import NamespaceHook, ReservedNamespaceHook

if TYPE_CHECKING:  # pragma: no cover, no mutate
  from typing import Any, TypeAlias, Iterator, Union, Self, Optional
  from .space_hooks import AbstractSpaceHook
  from . import AbstractMetaclass as AMeta

  Base: TypeAlias = tuple[type, ...]
  Bases: TypeAlias = tuple[Self, ...]
  Hooks: TypeAlias = list[AbstractSpaceHook]
  MROSpace: TypeAlias = dict[str, list[Any]]
  TypeName: TypeAlias = Union[str, type]


class AbstractNamespace(dict):
  """
  A metaclass learns about a class body only after it has run, as a
  plain dictionary of names. worktoy needs more: a mistake in the body,
  such as a misspelled dunder, must fail at its line; one name must be
  bindable several times, as with '@overload'; what the body declared
  must be turned into something else before the class is created; and a
  subclass must find what its bases declared, overloads included, once
  those bases exist. All of this must be split into pieces a namespace
  is assembled from, so a project can add its own.

  Implementation
  --------------

  'AbstractMetaclass.__prepare__' creates one namespace per class
  statement. Every binding, read and deletion of the body passes through
  the hooks of the namespace class, instances of 'AbstractSpaceHook'
  declared in its body; a hook may refuse a name, or claim a binding so
  the namespace does not store it. A shadow record of every binding
  keeps a claimed name readable in the body instead of falling through
  to the global names of the file. 'compile' assembles the dictionary for
  'type.__new__' from the hooks' defaults, the names of the body and the
  hooks' transformations, adds '__metaclass__', '__namespace__' and
  '__keyword_arguments__', and keeps it, so subclasses can read it later
  through 'getMROSpace'. Everything a class body bound therefore stays
  alive with the class. Every namespace refuses rebinding of reserved
  names ('ReservedNamespaceHook') and misspelled dunders
  ('NamespaceHook'); a subclass adds hooks by declaring them, and cannot
  replace an inherited hook by declaring one at the same name. The class
  keyword '_strictMRO=False' admits bases with no consistent resolution
  order, for a namespace built for inspection alone.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Class Variables
  __owner_hooks_list_name__: str = '__hook_objects__'

  #  Private Variables
  __metaclass__: Optional[AMeta] = None
  __class_name__ = None
  __base_classes__ = None
  __class_mro__ = None
  __key_args__ = None
  __compiled_space__ = None
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
    A name a hook claimed must stay readable in the class body, or reading
    it would silently find a global of the same name instead.

    Returns
    -------

    dict
      Every binding of the body so far, the latest per name.
    """
    return maybe(self.__shadow_space__, dict())

  def getClaimedDeletions(self, ) -> tuple[str, ...]:
    return maybe(self.__claimed_deletions__, ())

  def deepGetItem(self, item: str, ) -> Any:
    """
    A hook may need what a name holds in the body or, failing that, in the
    classes along the resolution order.

    Parameters
    ----------

    item : str
      The name to read.

    Returns
    -------

    Any
      The value the body bound, or the list of values the classes along
      the order hold, nearest first.

    Raises
    ------

    KeyError
      Neither holds the name.
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
      yield out

  @classmethod
  def classGetHooks(cls, ) -> Hooks:
    """
    A namespace must run the hooks its own class declares and those its
    bases declared, each once, in a fixed order, since the first hook
    claiming a binding hides it from the rest.

    Implementation
    --------------

    The hooks of the base namespace classes come first, then those of the
    subclass in declaration order.

    Returns
    -------

    Hooks
      A 'list[AbstractSpaceHook]'.
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
    if TYPE_CHECKING:  # pragma: no cover, no mutate
      assert isinstance(self.__metaclass__, AMeta)
    return self.__metaclass__

  def getClassName(self, ) -> str:
    return self.__class_name__

  def getKwargs(self, ) -> dict:
    return {**self.__key_args__, **dict()}

  def getMRO(self, ) -> list[type]:
    return self.__class_mro__

  def _getLookupOrder(self, ) -> list[type]:
    """
    A namespace built with '_strictMRO=False' for bases with no consistent
    resolution order still needs an order to search.

    Implementation
    --------------

    The computed order, or else each base's own order, bases left to
    right, each class kept at its first position.
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
    A subclass must read what its bases declared, each base as its own
    namespace compiled it, nearest first.

    Implementation
    --------------

    The compiled dictionary of every class along the lookup order built by
    a worktoy namespace is merged, read past any '__getattr__' or
    '__getattribute__' a class reimplements; plain classes are passed
    over.

    Returns
    -------

    MROSpace
      A 'dict[str, list[Any]]' from each name to the values the classes
      hold, nearest first.
    """
    lookupOrder = self._getLookupOrder()
    compiledSpaces = []
    for cls in lookupOrder:
      try:
        space = type.__getattribute__(cls, '__namespace__')
        compiledSpace = object.__getattribute__(space, '__compiled_space__')
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
    A hook declared in the body of a namespace class must register itself,
    and two different hooks at one name would leave it unclear which one
    runs.

    Parameters
    ----------

    hook : AbstractSpaceHook
      The hook.

    Raises
    ------

    DuplicateHook
      Another hook is registered at the name, on this class or a base.
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
    The namespace must know the class it serves before the body runs, so
    its hooks can screen every line.

    Implementation
    --------------

    The metaclass, name, bases and keywords are kept, the resolution order
    is computed, and every hook's 'preparePhase' runs.

    Parameters
    ----------

    mcls : AMeta
      The metaclass creating the class.

    name : str
      The name of the class.

    bases : Base
      A 'tuple[type, ...]' of the bases of the class statement.

    **kwargs
      The class keywords; '_strictMRO=False' admits bases with no
      consistent resolution order.

    Raises
    ------

    TypeError
      The bases admit no consistent resolution order.
    """
    self.__metaclass__ = mcls
    self.__class_name__ = name
    self.__base_classes__ = [*bases, ]
    self.__key_args__ = kwargs or {}
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
      hook.preparePhase(self)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __getitem__(self, key: str, **kwargs) -> Any:
    """
    Every read in the class body must pass the hooks, and a name a hook
    claimed must still read as bound.

    Implementation
    --------------

    The dictionary is asked, then the shadow record; every hook's
    'getItemPhase' runs, with the 'KeyError' as value on a miss, which is
    then raised again for the interpreter to look among the global names.

    Parameters
    ----------

    key : str
      The name read.

    Returns
    -------

    Any
      The value bound in the body.

    Raises
    ------

    KeyError
      The body never bound the name.

    HookException
      A hook raised; the original is its cause.
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
      try:
        hook.getItemPhase(key, val)
      except Exception as exception:
        raise HookException(exception, self, key, val, hook)
    if missing is not None:
      raise missing
    return val

  def __setitem__(self, key: str, val: Any, **kwargs) -> None:
    """
    Every binding in the class body must pass the hooks, any of which may
    refuse it or claim it.

    Implementation
    --------------

    The shadow record takes the binding first; the hooks run in order and
    the first claiming the binding ends the round; unclaimed, the value is
    stored.

    Parameters
    ----------

    key : str
      The name bound.

    val : Any
      The value bound.
    """
    shadow = self.getShadowSpace()
    shadow[key] = val
    self.__shadow_space__ = shadow
    try:
      oldVal = dict.__getitem__(self, key)
    except KeyError:
      oldVal = None
    for hook in self.getHooks():
      if hook.setItemPhase(key, val, oldVal):
        break  # Breaks out of the loop if handled by hook.
    else:  # If no 'break', the 'else' block is executed.
      dict.__setitem__(self, key, val)

  def __delitem__(self, key: str, **kwargs) -> None:
    """
    Every deletion in the class body must pass the hooks. A name whose
    latest binding a hook claimed cannot be deleted, since the hook
    registered the value already, and the interpreter replaces any
    exception a deletion in a class body raises with its own 'NameError'.

    Implementation
    --------------

    A hook may claim the deletion. Otherwise a claimed name is recorded,
    and 'compile' raises 'ClaimedName' for it; the name leaves the shadow
    record and the dictionary.

    Parameters
    ----------

    key : str
      The name deleted.

    Raises
    ------

    KeyError
      The body never bound the name.
    """
    shadow = self.getShadowSpace()
    if key not in shadow and not dict.__contains__(self, key):
      raise KeyError(key)
    if dict.__contains__(self, key):
      val = dict.__getitem__(self, key)
    else:
      val = shadow[key]
    for hook in self.getHooks():
      if hook.delItemPhase(key, val):
        return
    if self._isClaimed(key):
      self.__claimed_deletions__ = (*self.getClaimedDeletions(), key)
    shadow.pop(key, None)
    if dict.__contains__(self, key):
      dict.__delitem__(self, key)

  def _isClaimed(self, key: str) -> bool:
    """
    A deletion must know whether a hook claimed the latest binding of the
    name.

    Implementation
    --------------

    The shadow record holds every binding and the dictionary only the
    unclaimed ones, so they disagree exactly when the latest binding was
    claimed.
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
    A namespace subclass may need to change how the dictionary starts out,
    before the names of the body are merged in.

    Implementation
    --------------

    Every hook's 'preCompilePhase' runs over the dictionary.

    Parameters
    ----------

    namespace : dict, optional
      The dictionary to start from; a new one by default.

    Returns
    -------

    dict
      The dictionary.
    """
    if namespace is None:
      namespace = dict()
    elif not isinstance(namespace, dict):
      raise TypeException('namespace', namespace, dict)
    for hook in self.getHooks():
      namespace = hook.preCompilePhase(namespace)
    return namespace

  def compile(self, namespace: Optional[dict] = None) -> dict:
    """
    The metaclass needs the dictionary the class is created from, and
    subclasses of the class need it later to learn what the class
    declared.

    Implementation
    --------------

    A deletion of a claimed name raises 'ClaimedName' first. Then
    'preCompile', the names of the body, which replace the defaults,
    'postCompile', and the entries '__metaclass__', '__namespace__' and
    '__keyword_arguments__'. The result is kept as the compiled dictionary.
    A namespace subclass reimplements 'preCompile' or 'postCompile', not
    this method.

    Parameters
    ----------

    namespace : dict, optional
      The dictionary to start from; a new one by default.

    Returns
    -------

    dict
      The dictionary for 'type.__new__'.

    Raises
    ------

    ClaimedName
      The body deleted a name a hook had claimed.
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
    A namespace subclass may need to change the dictionary after the names
    of the body are merged in.

    Implementation
    --------------

    Every hook's 'postCompilePhase' runs over the dictionary; this is
    where 'LoadSpaceHook' builds the dispatchers.

    Parameters
    ----------

    namespace : dict
      The assembled dictionary.

    Returns
    -------

    dict
      The dictionary.
    """
    for hook in self.getHooks():
      namespace = hook.postCompilePhase(namespace)
    return namespace
