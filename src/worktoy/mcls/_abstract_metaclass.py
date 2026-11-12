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

if TYPE_CHECKING:  # pragma: no cover, no mutate
  from typing import Any, TypeAlias, Type, Union

  from . import AbstractMetaclass

  AMeta: TypeAlias = Union[MetaType, AbstractMetaclass, type]

  Base: TypeAlias = tuple[type, ...]


class AbstractMetaclass(MetaType, metaclass=MetaType):
  """
  A class is an object too, and some classes want to behave as objects
  do: a registry class iterated over its members, a class with a
  length, a class answering 'isinstance' its own way, a class building
  its instances in its own way. In plain Python each of these takes a
  metaclass of its own, and metaclasses combine badly. worktoy needs one
  metaclass under which a class defines such behaviour itself, in its
  own body, and leaves every operation it does not define as a plain
  class would have it. The same metaclass must build the class from a
  namespace whose hooks screen and transform the class body, and let a
  base refuse a subclass.

  Implementation
  --------------

  '__prepare__' returns an 'AbstractNamespace'; '__new__' compiles it,
  creates the class through 'MetaType', and hands it to every hook's
  'newClassPhase'; '__init__' calls the class hook '__class_init__', if
  defined, then '__subclasshook__' on each base with the new class, so a
  base may refuse it by raising. Each operation on the class consults a
  classmethod hook of the class: '__class_call__', '__class_init__',
  '__class_instancecheck__', '__class_subclasscheck__', '__class_str__',
  '__class_repr__', '__class_iter__', '__class_next__',
  '__class_bool__', '__class_contains__', '__class_len__',
  '__class_hash__', '__class_setitem__', '__class_delitem__',
  '__class_getattr__' for a missing attribute, '__class_setattr__' and
  '__class_delattr__'. A hook not defined holds 'METACALL', and the
  operation then behaves as for a plain class: 'bool' answers from
  '__class_len__' or else 'True', 'in' searches the items
  '__class_iter__' yields, and 'len' fails. 'NamespaceHook'
  holds every hook to being a classmethod or 'METACALL'. Equality of
  classes stays identity; '__class_eq__', '__class_ne__' and a
  class-level '__getitem__' are deliberately not offered, and a
  subscript of a class goes to its '__class_getitem__' as in plain
  Python. The defaults of '__call__', '__instancecheck__',
  '__subclasscheck__', '__str__', '__repr__', '__setattr__' and
  '__delattr__' hand over with 'super()', so a metaclass based on
  'MetaType' mixed in beside this one takes part in those. The defaults
  of the other operations answer themselves and reach no metaclass
  listed after this one.

  Python expects one of two behaviours from an object that iterates: an
  iterable, whose '__iter__' returns a fresh iterator at every call and
  which iteration leaves as it was, or an iterator, whose '__iter__'
  returns itself and whose '__next__' hands out each item once. The
  class hooks are held to the same expectation: '__class_iter__'
  returning a new iterator each time makes the class an iterable, and
  '__class_iter__' returning the class itself beside a '__class_next__'
  makes it an iterator. Hooks implemented in a way that falls outside
  those two, as a class that iterates itself yet also counts or
  searches itself by iterating, give undefined behaviour in some
  circumstances. That undefined behaviour is the same as for a plain
  class implementing '__iter__', '__next__' and '__len__' in the same
  in-between way.

  A note on 'collections.abc', for any reader puzzled by it: because
  this metaclass implements '__iter__', '__next__', '__len__' and
  '__contains__', so that each of its classes may opt in through the
  hooks above, 'isinstance' reports every class it builds as an
  'Iterable', 'Iterator', 'Sized', 'Container' and 'Collection', the
  classes defining no hook included. That report is wrong, and the fault
  is with 'collections.abc', not with worktoy. Those structural checks
  never call the methods. They only look for the names in the
  dictionary of the type of the object, which for a class is its
  metaclass, so they cannot tell one class of a metaclass from another.
  The one signal they honour, a name set to 'None', would switch the
  operation off for every class of the metaclass at once, so Python
  leaves a single class no way to answer for itself. The Python
  documentation itself names 'iter(obj)' as the only reliable test of
  whether an object iterates. The routing stays as it is, by decision.
  Code that must know whether a worktoy class iterates, or has a length,
  calls 'iter(cls)' or 'len(cls)' and catches 'TypeError'.
  """

  __abstract_metaclass__: bool = True
  __class_getattr__: SentinelMeta = METACALL
  __class_setattr__: SentinelMeta = METACALL
  __class_delattr__: SentinelMeta = METACALL
  __class_call__: SentinelMeta = METACALL

  @classmethod
  def __prepare__(mcls, name: str, bases: Base, **kwargs) -> ASpace:
    """
    The class body must run in a namespace whose hooks screen it. A
    metaclass based on this one supplies another namespace by
    reimplementing this method to return an instance of an
    'AbstractNamespace' subclass, and leaves the bases as they are.

    Returns
    -------

    AbstractNamespace
      The namespace of the class body.
    """
    # noinspection PyTypeChecker
    return ASpace(mcls, name, bases, **kwargs)

  def __new__(mcls, name: str, bases: Base, space: ASpace, **kw) -> AMeta:
    """
    The class must be created from what the hooks made of the class body,
    and the hooks must see the finished class. A class created by calling
    the metaclass with a plain dictionary, as 'BaseMeta(name, bases,
    {...})', must be screened as a class body would be.

    Implementation
    --------------

    A plain dictionary is replayed into a new namespace first. The
    namespace is compiled, the class is created by the next '__new__'
    along the metaclass order, and every hook's 'newClassPhase' may
    replace it. Class keywords pass on and end in '_Chill'.

    Parameters
    ----------

    name : str
      The name of the class.

    bases : Base
      A 'tuple[type, ...]' of the bases.

    space : ASpace
      The namespace of the class body, or a plain dictionary.

    **kw
      Class keywords.

    Returns
    -------

    AMeta
      The new class.
    """
    if not isinstance(space, ASpace):
      plain = space
      space = mcls.__prepare__(name, bases, **kw)
      for key, val in dict.items(plain):
        space[key] = val
    namespace = space.compile()
    cls: AMeta = super().__new__(mcls, name, bases, namespace, **kw)
    for hook in space.getHooks():
      cls = maybe(hook.newClassPhase(cls), cls)
    return cls

  def __init__(cls, name: str, bases: Base, space: ASpace, **kwargs) -> None:
    """
    A class may need to finish itself once it exists, and a base may need
    to accept or refuse each subclass.

    Implementation
    --------------

    After the next '__init__' along the metaclass order, the class hook
    '__class_init__' receives the name, the bases, the namespace object
    and the keywords, and each base as written receives the class through
    '__subclasshook__', whose answer is ignored but whose exception
    refuses the class.
    """
    super().__init__(name, bases, space, **kwargs)
    if cls.__class_init__ is not METACALL:
      namespace: dict = type.__getattribute__(cls, '__namespace__')
      cls.__class_init__(name, bases, namespace, **kwargs)
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
    """
    A class may need to be iterable itself, as a registry of its members,
    by defining '__class_iter__' as a classmethod returning an iterator.
    A class without the hook must fail to iterate, as a plain class does.
    A hook returning a fresh iterator at every call makes the class an
    iterable; one returning the class itself, beside '__class_next__',
    makes it an iterator. The class docstring says what Python expects
    of each, and what falls outside the two.

    A note on 'collections.abc': 'isinstance(cls, Iterable)' answers
    'True' for every class this metaclass builds, the ones without the
    hook included. That answer is wrong, and the fault is with
    'collections.abc', not here. Its structural check never calls
    '__iter__'; it only looks whether the type of the object, for a class
    its metaclass, holds an '__iter__' in its dictionary. This metaclass
    must hold one for any of its classes to opt in, and Python gives a
    single class no way to tell the check otherwise: the one signal it
    honours, '__iter__ = None', would apply to every class of the
    metaclass at once. The Python documentation itself names 'iter(obj)'
    as the only reliable test of whether an object iterates, so code that
    must know whether a worktoy class iterates calls 'iter(cls)' and
    catches 'TypeError'.

    Returns
    -------

    Iterator
      The iterator '__class_iter__' returns.

    Raises
    ------

    TypeError
      The class defines no '__class_iter__'.
    """
    if cls.__class_iter__ is METACALL:
      infoSpec = """type object '%s' is not iterable"""
      info = infoSpec % cls.__name__
      raise TypeError(info)
    return cls.__class_iter__()

  def __next__(cls) -> Any:
    """
    A class acting as its own iterator defines '__class_next__' as a
    classmethod, raising 'StopIteration' when done; a class without it is
    no iterator. An iterator class has no length, and a search with 'in'
    consumes it, as for a plain iterator; see the class docstring.

    'isinstance(cls, Iterator)' from 'collections.abc' answers 'True' for
    every class this metaclass builds, hook or not. The fault is with
    'collections.abc', whose check only looks for '__iter__' and
    '__next__' on the metaclass and never asks the class; see '__iter__'
    and the class docstring.

    Raises
    ------

    TypeError
      The class defines no '__class_next__'.
    """
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
    return True  # Default behavior if no custom bool or len defined

  def __contains__(cls, item: Any) -> bool:
    """
    'item in cls' must ask '__class_contains__' when the class defines it,
    search the items of an iterable class otherwise, and fail for a class
    that is neither, as for a plain class.

    'isinstance(cls, Container)' from 'collections.abc' answers 'True' for
    every class this metaclass builds, hooks or not. The fault is with
    'collections.abc', whose check only looks for '__contains__' on the
    metaclass and never asks the class; see '__iter__' and the class
    docstring.

    Implementation
    --------------

    Without '__class_contains__', the items '__class_iter__' yields are
    compared with '==', as Python's 'in' searches an object without
    '__contains__' through its iterator. An iterator class is consumed
    by the search, as a plain one is.

    Parameters
    ----------

    item : Any
      The object looked for.

    Returns
    -------

    bool
      Whether the class holds the item.

    Raises
    ------

    TypeError
      The class defines neither '__class_contains__' nor '__class_iter__'.
    """
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
    """
    'len(cls)' must ask '__class_len__' when the class defines it, and
    fail otherwise, as it does for a plain class without '__len__'. It
    does not count the items of a class defining only '__class_iter__':
    Python gives an iterable without '__len__' no length, and counting by
    iteration would consume a class that is its own iterator, as a
    plain class with such a counting '__len__' is consumed. A registry
    class wanting a length defines '__class_len__'.

    'isinstance(cls, Sized)' from 'collections.abc' answers 'True' for
    every class this metaclass builds, hooks or not, and so does
    'isinstance(cls, Collection)'. The fault is with 'collections.abc',
    whose checks only look for the method names on the metaclass and never
    ask the class; see '__iter__' and the class docstring. Code that must
    know whether a worktoy class has a length calls 'len(cls)' and catches
    'TypeError'.

    Returns
    -------

    int
      The length of the class.

    Raises
    ------

    TypeError
      The class defines no '__class_len__'.
    """
    if cls.__class_len__ is not METACALL:
      return cls.__class_len__()
    infoSpec = """type object '%s' has no len()"""
    info = infoSpec % cls.__name__
    raise TypeError(info)

  @staticmethod
  def _skipHash(cls) -> bool:
    """
    '_Chill' is a base of every worktoy class and must not take part in
    the hash of a class, or no class would hash as its declared bases
    suggest.

    Implementation
    --------------

    The flag '__skip_hash__' is read with 'type.__getattribute__', so no
    '__getattr__' of a base answers for it; a plain base without the flag
    counts as 'False'.
    """
    try:
      return type.__getattribute__(cls, '__skip_hash__')
    except AttributeError:
      return False

  def __hash__(cls) -> int:
    """
    A class must hash the same for its whole life, as a plain class does,
    so it stays findable in a dictionary or set, even if renamed later;
    and a class defining '__class_hash__' must hash as it says.

    Implementation
    --------------

    Without '__class_hash__', the hash is computed at the first hash from
    the name of the class, the names of its direct bases other than
    'object' and '_Chill', and the name of its metaclass, and kept in the
    class's own dictionary under '__class_hash_value__'. A subclass
    computes its own.

    Returns
    -------

    int
      The hash.
    """
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
    """
    A class may answer for attributes it does not have, by defining
    '__class_getattr__'; otherwise a missing class attribute must fail as
    'AttributeError', so 'hasattr' answers. Inside this method, only names
    the metaclass itself defines are safe to read with the dot operator,
    since any other missing name would come back here.

    Parameters
    ----------

    name : str
      The missing name.

    Returns
    -------

    Any
      What '__class_getattr__' returns.

    Raises
    ------

    MissingVariable
      The class defines no '__class_getattr__'.
    """
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
    """
    A base must be able to see, and refuse, each class created from it.

    Implementation
    --------------

    '__subclasshook__' is called on each base with the new class; its
    answer is ignored.
    """
    for base in bases:
      base.__subclasshook__(cls)
    return cls

  def getNamespace(cls) -> ASpace:
    """
    Code inspecting a worktoy class may need the namespace object its body
    ran in, read past any class-level attribute hook.

    Returns
    -------

    AbstractNamespace
      The namespace that built the class.
    """
    return type.__getattribute__(cls, '__namespace__', )

  @classmethod
  def getNamespaceClass(mcls) -> Type[ASpace]:
    """
    Code building on a metaclass may need to know which namespace class it
    uses.

    Implementation
    --------------

    '__prepare__' is called for a class named '_' without bases, which
    runs every hook's 'preparePhase' once for that name.

    Returns
    -------

    Type[ASpace]
      The class of the namespace.
    """
    return type(mcls.__prepare__('_', ()))
