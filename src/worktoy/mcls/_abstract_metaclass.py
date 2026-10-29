"""
AbstractMetaclass is the base class for the 'worktoy' metaclasses.
"""
#  Apache-2.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from ..core import MetaType
from ..core.sentinels import METACALL, SentinelMeta
from ..utilities import maybe
from ..waitaminute import MissingVariable
from . import AbstractNamespace as ASpace

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, TypeAlias, Type, Union

  from . import AbstractMetaclass

  AMeta: TypeAlias = Union[MetaType, AbstractMetaclass, type]

  Base: TypeAlias = tuple[type, ...]


class AbstractMetaclass(MetaType, metaclass=MetaType):
  """
  Abstract base for custom metaclasses that separates concerns between
  class construction and class behavior.

  This design delegates the initial class namespace to a custom object
  returned by '__prepare__', while keeping class semantics within the
  metaclass itself. The namespace object may define a method called
  'compile()', which should return the finalized dictionary to be passed
  to 'type.__new__'.

  Custom namespace compilation
  ----------------------------
  The 'AbstractNamespace' class is intended to be
  used with '__prepare__'. It defines a 'compile()' method and an
  '__init__()' signature compatible with the arguments passed to
  '__prepare__'. Specifically:

      def __prepare__(mcls, name: str, bases: Base, **kw) -> ASpace

  and 'AbstractNamespace' implements:

      def __init__(self, mcls: type, name: str, bases: Base, **kw)

  This allows the namespace object to be instantiated with full context
  about the class being defined, while remaining isolated from the
  behavior of the resulting class itself.

  Validation hooks
  ----------------
  Validation of the namespace is delegated to space hooks rather than
  performed by the metaclass itself. The 'NamespaceHook' raises
  'QuestionableSyntax' on near-miss dunder names such as
  '__set_item__' (intended '__setitem__') or '__setname__' (intended
  '__set_name__'), and raises 'DelException' on plain '__del__'.
  Pass 'trustMeBro=True' as a class keyword if a real '__del__'
  implementation is genuinely needed.

  Class-level behavior hooks
  --------------------------
  Once a class has been created by the metaclass system, it may define
  its own runtime behavior by implementing special methods prefixed with
  '__class_'. These resemble '__class_getitem__' from standard Python
  but are more general. The metaclass dispatches the corresponding
  builtin operation to the class-level hook when present, falling back
  to the default 'type' behavior otherwise. Hooks are detected by
  comparison against the 'METACALL' sentinel. A metaclass based on this
  one that implements an operation itself, as 'KeeMeta' implements
  '__len__', takes it over from the hook, and 'NamespaceHook' refuses
  that hook in the body of its classes with 'ShadowedClassHook'.

  Supported class-level hooks:

  - '__class_call__(clsName, *args, **kw) -> Any'
    Called when the class is invoked. Overrides instance construction.
  - '__class_instancecheck__(clsName, obj) -> bool'
    Called during 'isinstance(obj, clsName)'.
  - '__class_subclasscheck__(clsName, sub) -> bool'
    Called during 'issubclass(sub, clsName)'.
  - '__class_str__(clsName) -> str'
    Called when 'str(clsName)' is invoked.
  - '__class_repr__(clsName) -> str'
    Called when 'repr(clsName)' is invoked.
  - '__class_iter__(clsName) -> Iterator'
    Called when 'iter(clsName)' is invoked.
  - '__class_next__(clsName) -> Any'
    Called when 'next(clsName)' is invoked.
  - '__class_bool__(clsName) -> bool'
    Called when 'bool(clsName)' is invoked. If absent, falls back to
    '__class_len__' or '__class_iter__'.
  - '__class_contains__(clsName, item) -> bool'
    Called for membership checks. Falls back to iteration if absent.
  - '__class_len__(clsName) -> int'
    Called when 'len(clsName)' is invoked.
  - '__class_hash__(clsName) -> int'
    Called when 'hash(clsName)' is invoked. The default hashes the name
    of the class, the names of its bases other than 'object' and the
    bases marked '__skip_hash__' ('_Chill'), and the name of its
    metaclass:

        baseNames = [b.__name__ for b in bases]  # less object, _Chill
        metaName = type(clsName).__name__
        return hash((clsName.__name__, *baseNames, metaName))

    The default is computed at the first hash and kept in the class's
    own '__dict__' under '__class_hash_value__', so a class keeps its
    hash for life, as a plain class does: renamed afterwards, it stays
    where a dict or set holds it. A '__class_hash__' is asked at every
    hash.
  - '__class_init__(clsName, name, bases, space, **kw) -> None'
    Invoked after the class body has been fully executed.
  - '__class_setitem__(clsName, item, value) -> None'
    Called when 'clsName[item] = value' is invoked.
  - '__class_delitem__(clsName, item) -> None'
    Called when 'del clsName[item]' is invoked.
  - '__class_getattr__(clsName, name) -> Any'
    Called when an undefined attribute is accessed on the class.
  - '__class_setattr__(clsName, name, value) -> None'
  - '__class_delattr__(clsName, name) -> None'

  Note on '__class_getitem__': as of Python 3.7 the interpreter
  dispatches subscript on a class straight to '__class_getitem__' when
  it is defined, without going through the metaclass. This metaclass
  defines no '__getitem__', so subscripting a class that has no
  '__class_getitem__' raises 'TypeError'.

  A hook is a classmethod and nothing else. 'NamespaceHook' refuses any
  other binding at a hook name, a plain function, a staticmethod, an
  '@overload', a value, with 'UnboundClassHook' at the class-body line;
  an '@overload' there would become a 'Dispatcher' calling its functions
  with an instance first, which the metaclass, calling the hook on the
  class, never passes.

  Combining metaclasses
  ---------------------
  '__new__', '__init__' and every default that applies when a class
  declares no hook, those of '__call__', '__instancecheck__',
  '__subclasscheck__', '__str__', '__repr__', '__setattr__' and
  '__delattr__', hand over with 'super()'. A metaclass based on
  'MetaType' and mixed in beside this one, as in
  'class Meta(BaseMeta, OtherMeta)', therefore takes part: its own
  versions of those methods run, in the order of the metaclass
  resolution order. For a metaclass based on this one alone the next
  class is 'MetaType', as it always was.

  Unimplemented or intentionally rejected hooks
  ---------------------------------------------
  - '__class_eq__' and '__class_ne__' exhibit poorly defined behavior
    when classes participate in equality outside of identity. Not
    implemented.
  - '__class_get__', '__class_set__', '__class_delete__',
    '__class_set_name__' are not implemented. Referencing other class
    objects while a metaclass is awake (inside '__prepare__', '__new__',
    or '__init__') can leak context: Python may route calls to the
    wrong metaclass entirely.
  - '__class_new__' would refer to a hook running before the class
    exists, which is meaningless.
  - '__class_del__' is rejected for the same reasons '__del__' is
    rejected on instances.
  - '__class_getattribute__' is not implemented (cognito hazard).
  """

  __abstract_metaclass__: bool = True
  __class_getattr__: SentinelMeta = METACALL
  __class_setattr__: SentinelMeta = METACALL
  __class_delattr__: SentinelMeta = METACALL
  __class_call__: SentinelMeta = METACALL

  @classmethod
  def __prepare__(mcls, name: str, bases: Base, **kwargs) -> ASpace:
    """
    The __prepare__ method is invoked before the class is created. This
    method instantiates the namespace object used to collect the class
    body. The default implementation in 'type' returns a plain empty
    'dict' object. Subclasses of 'AbstractMetaclass' may override this
    method to provide a further customized namespace object.

    Also, this method removes nothing from the 'bases' tuple. Subclasses
    should also remove nothing from the 'bases' tuple.
    """
    # noinspection PyTypeChecker
    return ASpace(mcls, name, bases, **kwargs)

  def __new__(mcls, name: str, bases: Base, space: ASpace, **kw) -> AMeta:
    """
    The '__new__' method compiles the namespace and builds the class from
    it, then hands the class to the 'newClassPhase' of every hook. Called
    directly with a plain dict, as in 'BaseMeta(name, bases, {...})', it
    first copies the dict into a namespace of its own, and the hooks of
    that namespace run. The class itself is built by the next '__new__'
    along the metaclass resolution order, through 'super()'.
    """
    if not isinstance(space, ASpace):
      plain = space
      space = mcls.__prepare__(name, bases, **kw)
      for key, val in dict.items(plain):
        space[key] = val
    namespace = space.compile()
    cls: AMeta = super().__new__(mcls, name, bases, namespace, **kw)
    for hook in space.getHooks():
      setattr(hook, '__space_object__', space)
      cls = maybe(hook.newClassPhase(cls), cls)
    return cls

  def __init__(cls, name: str, bases: Base, space: ASpace, **kwargs) -> None:
    """Finalize the class. By now 'type.__new__' has already run
    '__set_name__' and '__init_subclass__'. This calls the next
    '__init__' along the metaclass resolution order through 'super()',
    then the optional '__class_init__' hook, then the subclass
    notification ('_notifySubclassHook')."""
    super().__init__(name, bases, space, **kwargs)
    if cls.__class_init__ is not METACALL:
      cls.__class_init__(name, bases, space, **kwargs)
    type(cls)._notifySubclassHook(cls, *bases)

  def __call__(cls, *args, **kwargs) -> Any:
    if cls.__class_call__ is METACALL:
      return super().__call__(*args, **kwargs)
    return cls.__class_call__(*args, **kwargs)

  def __instancecheck__(cls, obj: Any) -> bool:
    if cls.__class_instancecheck__ is METACALL:
      return super().__instancecheck__(obj)
    return cls.__class_instancecheck__(obj)

  def __subclasscheck__(cls, subclass: type) -> bool:
    if cls.__class_subclasscheck__ is METACALL:
      return super().__subclasscheck__(subclass)
    return cls.__class_subclasscheck__(subclass)

  def __str__(cls) -> str:
    if cls.__class_str__ is METACALL:
      return super().__str__()
    return cls.__class_str__()

  def __repr__(cls) -> str:
    if cls.__class_repr__ is METACALL:
      return super().__repr__()
    return cls.__class_repr__()

  def __iter__(cls) -> Any:
    if cls.__class_iter__ is METACALL:
      infoSpec = """type object '%s' is not iterable"""
      info = infoSpec % cls.__name__
      raise TypeError(info)
    return cls.__class_iter__()

  def __next__(cls) -> Any:
    if cls.__class_next__ is METACALL:
      infoSpec = """type object '%s' is not an iterator"""
      info = infoSpec % cls.__name__
      raise TypeError(info)
    return cls.__class_next__()

  def __bool__(cls) -> bool:
    """
    Here, too, I saw a nation of lost souls,
    far more than were above: they strained their chests
    against enormous weights, and with mad howls
    rolled them at one another. Then in haste
    they rolled them back, one party shouting out:
    "Why do you hoard?" and the other: "Why do you waste?"
    """
    if cls.__class_bool__ is not METACALL:
      return cls.__class_bool__()
    if cls.__class_len__ is not METACALL:
      return True if cls.__class_len__() else False
    if cls.__class_iter__ is not METACALL:
      for _ in cls:
        return True
      return False
    return True  # Default behavior if no custom bool or len defined

  def __contains__(cls, item: Any) -> bool:
    if cls.__class_contains__ is not METACALL:
      return cls.__class_contains__(item)
    if cls.__class_iter__ is not METACALL:
      for clsItem in cls:
        if clsItem == item:
          return True
      return False
    infoSpec = """argument of type '%s' is not iterable"""
    info = infoSpec % cls.__name__
    raise TypeError(info)

  def __len__(cls) -> int:
    if cls.__class_len__ is not METACALL:
      return cls.__class_len__()
    if cls.__class_iter__ is not METACALL:
      return sum(1 for _ in cls)  # Count items in the iterator
    infoSpec = """type object '%s' has no len()"""
    info = infoSpec % cls.__name__
    raise TypeError(info)

  @staticmethod
  def _skipHash(cls) -> bool:
    """
    The '_skipHash' method checks if the class has a '__skip_hash__'
    attribute set to True. This is used to determine if the class should
    skip custom hash computation. The flag is read with
    'type.__getattribute__', so that no '__getattr__', '__class_getattr__'
    or reimplemented '__getattribute__' of a base can answer for it.
    """
    try:
      return type.__getattribute__(cls, '__skip_hash__')
    except AttributeError:
      return False

  def __hash__(cls) -> int:
    """The '__class_hash__' of the class, asked at every hash, or else the
    default, computed at the first hash and kept in the class's own
    '__dict__' under '__class_hash_value__', so the class keeps its hash
    for life, as a plain class does, whatever becomes of its name or
    bases. Only the own '__dict__' is read, so a subclass computes its
    own."""
    if cls.__class_hash__ is not METACALL:
      return cls.__class_hash__()
    try:
      return cls.__dict__['__class_hash_value__']
    except KeyError:
      bases = (*(b for b in cls.__bases__ if not type(cls)._skipHash(b)),)
      bases = (*(b for b in bases if b is not object),)
      baseNames = [b.__name__ for b in bases]
      metaName = type(cls).__name__
      value = hash((cls.__name__, *baseNames, metaName))
      type.__setattr__(cls, '__class_hash_value__', value)
      return value

  #  DO NOT REMOVE THE FOLLOWING COMMENTED OUT METHODS
  # def __eq__(keeNum, other: Any) -> bool:
  #   """This method is disabled because of highly undefined behaviour!"""
  #
  #  def __ne__(keeNum, other: Any) -> bool:
  #    """See above"""
  #
  #  DO NOT REMOVE THIS COMMENTED OUT METHOD  (not related to above)
  # def __getitem__(keeNum, item: Any) -> Any:
  #   """
  #   This method is intentionally commented out, not removed, to ensure
  #   discoverability and traceability.
  #   """
  #
  #   For an explanation, see the '__class_getitem__' note in the 'NameHook'
  #   class, located in 'worktoy.mcls.space_hooks'. In short, the interpreter
  #   handles '__class_getitem__' directly as of Python 3.7, making this
  #   override unnecessary and potentially conflicting.

  def __setitem__(cls, item: Any, value: Any) -> None:
    if cls.__class_setitem__ is METACALL:
      infoSpec = """type object '%s' is not subscriptable"""
      info = infoSpec % cls.__name__
      raise TypeError(info)
    return cls.__class_setitem__(item, value)

  def __delitem__(cls, item: Any) -> None:
    if cls.__class_delitem__ is METACALL:
      infoSpec = """type object '%s' does not support item deletion"""
      info = infoSpec % cls.__name__
      raise TypeError(info)
    return cls.__class_delitem__(item)

  def __getattr__(cls, name: str) -> Any:
    """A miss on the class comes here, so the dot operator is safe in
    this method only for names the metaclass itself defines, such as
    '__class_getattr__', which never miss. Any other name read with it
    comes back here, so those take the clunky 'type.__getattribute__',
    or it is recursion time!"""
    if cls.__class_getattr__ is METACALL:
      raise MissingVariable(cls, name)
    return cls.__class_getattr__(name, )

  def __setattr__(cls, name: str, value: Any) -> None:
    if cls.__class_setattr__ is METACALL:
      return super().__setattr__(name, value)
    return cls.__class_setattr__(name, value)

  def __delattr__(cls, name: str) -> None:
    if cls.__class_delattr__ is METACALL:
      return super().__delattr__(name)
    return cls.__class_delattr__(name)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @staticmethod
  def _notifySubclassHook(cls, *bases) -> type:
    """The _notifySubclassHook method is invoked to notify each baseclass
    of the created class of the class creation."""
    for base in bases:
      base.__subclasshook__(cls)
    return cls

  def getNamespace(cls) -> ASpace:
    """
    The 'getNamespace' method returns the namespace object that built
    'clsName', read directly off '__namespace__' to bypass the class-level
    attribute hooks.
    """
    return type.__getattribute__(cls, '__namespace__', )

  @classmethod
  def getNamespaceClass(mcls) -> Type[ASpace]:
    """
    The 'getNamespaceClass' classmethod returns the namespace type this
    metaclass uses, obtained by inspecting the object '__prepare__'
    returns.
    """
    return type(mcls.__prepare__('_', ()))
