"""
AbstractMetaclass is the base class for the 'worktoy' metaclasses.
"""
#  Apache-2.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from ..core import MetaType
from ..core.sentinels import METACALL
from ..utilities import maybe
from ..waitaminute import MissingVariable
from . import AbstractNamespace as ASpace

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, TypeAlias

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
  comparison against the 'METACALL' sentinel.

  Supported class-level hooks:

  - '__class_call__(cls, *args, **kw) -> Any'
    Called when the class is invoked. Overrides instance construction.
  - '__class_instancecheck__(cls, obj) -> bool'
    Called during 'isinstance(obj, cls)'.
  - '__class_subclasscheck__(cls, sub) -> bool'
    Called during 'issubclass(sub, cls)'.
  - '__class_str__(cls) -> str'
    Called when 'str(cls)' is invoked.
  - '__class_repr__(cls) -> str'
    Called when 'repr(cls)' is invoked.
  - '__class_iter__(cls) -> Iterator'
    Called when 'iter(cls)' is invoked.
  - '__class_next__(cls) -> Any'
    Called when 'next(cls)' is invoked.
  - '__class_bool__(cls) -> bool'
    Called when 'bool(cls)' is invoked. If absent, falls back to
    '__class_len__' or '__class_iter__'.
  - '__class_contains__(cls, item) -> bool'
    Called for membership checks. Falls back to iteration if absent.
  - '__class_len__(cls) -> int'
    Called when 'len(cls)' is invoked.
  - '__class_hash__(cls) -> int'
    Called when 'hash(cls)' is invoked. The default implementation is:

        baseNames = [b.__name__ for b in cls.__bases__]
        metaName = type(cls).__name__
        return hash((cls.__name__, *baseNames, metaName))

    Note: the 'overload' protocol in worktoy.dispatch expects this
    exact default. Overriding '__class_hash__' prevents the dispatcher
    from fast-path recognizing the class.
  - '__class_init__(cls, name, bases, space, **kw) -> None'
    Invoked after the class body has been fully executed.
  - '__class_setitem__(cls, item, value) -> None'
    Called when 'cls[item] = value' is invoked.
  - '__class_delitem__(cls, item) -> None'
    Called when 'del cls[item]' is invoked.
  - '__class_getattr__(cls, name) -> Any'
    Called when an undefined attribute is accessed on the class.
  - '__class_setattr__(cls, name, value) -> None'
  - '__class_delattr__(cls, name) -> None'

  Note on '__class_getitem__': as of Python 3.7 the interpreter
  dispatches subscript on a class straight to '__class_getitem__' when
  it is defined, without going through the metaclass. This metaclass
  defines no '__getitem__', so subscripting a class that has no
  '__class_getitem__' raises 'TypeError'.

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

  __abstract_metaclass__ = True
  __class_getattr__ = METACALL
  __class_setattr__ = METACALL
  __class_delattr__ = METACALL
  __class_call__ = METACALL

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
    return ASpace(mcls, name, bases, **kwargs)

  def __new__(mcls, name: str, bases: Base, space: ASpace, **kw) -> type:
    if isinstance(space, ASpace):
      namespace = space.compile()
    else:
      namespace = mcls.__prepare__(name, bases, **kw)
      for key, val in dict.items(space):
        namespace[key] = val
      namespace = namespace.compile()
    cls = MetaType.__new__(mcls, name, bases, namespace, **kw)
    if hasattr(space, 'getHooks'):
      for hook in space.getHooks():
        setattr(hook, '__space_object__', space)
        cls = maybe(hook.newClassPhase(cls), cls)
    return cls

  def __init__(cls, name: str, bases: Base, space: ASpace, **kwargs) -> None:
    """Finalize the class. By now 'type.__new__' has already run
    '__set_name__' and '__init_subclass__'. This calls
    'MetaType.__init__', then the optional '__class_init__' hook, then
    the subclass notification ('_notifySubclassHook')."""
    MetaType.__init__(cls, name, bases, space, **kwargs)
    if cls.__class_init__ is not METACALL:
      cls.__class_init__(name, bases, space, **kwargs)
    cls._notifySubclassHook(cls, *bases)

  def __call__(cls, *args, **kwargs) -> Any:
    if cls.__class_call__ is METACALL:
      return MetaType.__call__(cls, *args, **kwargs)
    return cls.__class_call__(*args, **kwargs)

  def __instancecheck__(cls, obj: Any) -> bool:
    if cls.__class_instancecheck__ is METACALL:
      return MetaType.__instancecheck__(cls, obj)
    return cls.__class_instancecheck__(obj)

  def __subclasscheck__(cls, subclass: type) -> bool:
    if cls.__class_subclasscheck__ is METACALL:
      return MetaType.__subclasscheck__(cls, subclass)
    return cls.__class_subclasscheck__(subclass)

  def __str__(cls) -> str:
    if cls.__class_str__ is METACALL:
      return MetaType.__str__(cls)  # NOQA
    return cls.__class_str__()

  def __repr__(cls) -> str:
    if cls.__class_repr__ is METACALL:
      return MetaType.__repr__(cls)
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

  def __hash__(cls) -> int:
    if cls.__class_hash__ is METACALL:
      baseNames = [b.__name__ for b in cls.__bases__]
      metaName = type(cls).__name__
      nameTuple = (cls.__name__, *baseNames, metaName)
      return hash(nameTuple)  # NOQA
    return cls.__class_hash__()

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
    """Do not use the 'dot' operator to access class attributes during
    this method! Instead, the clunky 'object.__getattribute__' must be
    used to avoid infinite recursion. This is not an edge case, if you
    bring the 'dot' operator into an implementation here, it is recursion
    time!"""
    if cls.__class_getattr__ is METACALL:
      raise MissingVariable(cls, name)
    return cls.__class_getattr__(name, )

  def __setattr__(cls, name: str, value: Any) -> None:
    if cls.__class_setattr__ is METACALL:
      return MetaType.__setattr__(cls, name, value)  # NOQA
    return cls.__class_setattr__(name, value)

  def __delattr__(cls, name: str) -> None:
    if cls.__class_delattr__ is METACALL:
      return MetaType.__delattr__(cls, name)
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
    'cls', read directly off '__namespace__' to bypass the class-level
    attribute hooks.
    """
    return type.__getattribute__(cls, '__namespace__', )

  @classmethod
  def getNamespaceClass(mcls) -> type:
    """
    The 'getNamespaceClass' classmethod returns the namespace type this
    metaclass uses, obtained by inspecting the object '__prepare__'
    returns.
    """
    return type(mcls.__prepare__('_', ()))
