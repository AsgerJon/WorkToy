"""
BaseDescriptor adds access-notification hook decorators to a descriptor.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar, Generic, overload, Callable, Any
from types import FunctionType as Func

from ..utilities import maybe
from ..core import Object
from ..dispatch import flexCall
from ..waitaminute import TypeException
from ..waitaminute.desc import NamelessCallback, SharedDescriptor

T = TypeVar('T', )
#  A decorated callback keeps its own type for a checker.
F = TypeVar('F', bound=Callable[..., Any])

if TYPE_CHECKING:  # pragma: no cover, no mutate
  from typing import TypeAlias, Self, Union, Optional

  Keys: TypeAlias = tuple[str, ...]


class BaseDescriptor(Object, Generic[T]):
  """
  A class holding a descriptor often needs to react to its accesses:
  check a value before it is written, log it after, observe reads or
  deletions, or register the descriptor somewhere as the class is
  created. These reactions belong in the owning class, as methods, and a
  subclass must be able to change them by overriding a method, without
  touching the descriptor. A descriptor bound to two names in one body
  must give two attributes, and one descriptor cannot serve two classes.

  Implementation
  --------------

  Seven decorators register a method of the owning class: 'preGet' and
  'onGet' around a read, 'preSet' and 'onSet' around a write,
  'preDelete' and 'onDelete' around a deletion, and 'setName' when the
  descriptor is placed, for which the method is a classmethod receiving
  the class and the descriptor:

    class Account(BaseObject):

      balance = AttriBox[int](0)

      @balance.preSet
      def _checkBalance(self, value: int) -> None:
        ...

  The decorators record the name of the method, and the hooks of
  'Object' look it up on the class of the instance at each access, so an
  override in a subclass is called instead. A private name is recorded
  mangled, '_Account__audit' for '__audit', and a lambda, which has no
  name to look up, is refused with 'NamelessCallback'. A callback is
  called by the kind of method the class holds at its name, as Python
  would call 'instance.name(value)': a method receives the instance, a
  classmethod the class of the instance, a staticmethod the value alone.
  '@classmethod' and '@staticmethod' may be written above a decorator or
  below it, and a subclass may override a callback as any kind; anything
  with no function to look up by name, as a 'functools.partial', is
  refused with 'TypeException'. Each decorator returns the method wrapped
  by 'flexCall', so a method may declare fewer parameters than it is
  passed. A 'setName' callback, called as the class is created, receives
  the class and the descriptor, or the descriptor alone as a
  staticmethod.
  'BaseDescriptor' itself stores nothing: it reads back as itself and
  refuses writes and deletions, as 'Object' does; a subclass defines the
  storage in the three '__instance_*__' methods and leaves '__get__',
  '__set__' and '__delete__' alone, since they call the hooks. A second
  name in the same class body receives a clone; a second class raises
  'SharedDescriptor'.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Class Variables

  #  Fallback Variables

  #  Private Variables
  __pre_get_keys__: Optional[tuple[str, ...]] = None
  __on_get_keys__: Optional[tuple[str, ...]] = None
  __pre_set_keys__: Optional[tuple[str, ...]] = None
  __on_set_keys__: Optional[tuple[str, ...]] = None
  __pre_delete_keys__: Optional[tuple[str, ...]] = None
  __on_delete_keys__: Optional[tuple[str, ...]] = None
  __set_name_keys__: Optional[tuple[str, ...]] = None
  #  The 'flexCall' wrapper of each callback function found so far
  __callback_wrappers__: Optional[dict[Callable, Callable]] = None

  #  Public Variables

  #  Virtual Variables

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Key getters

  def _getPreGetKeys(self) -> tuple[str, ...]:
    return maybe(self.__pre_get_keys__, ())

  def _getOnGetKeys(self) -> tuple[str, ...]:
    return maybe(self.__on_get_keys__, ())

  def _getPreSetKeys(self) -> tuple[str, ...]:
    return maybe(self.__pre_set_keys__, ())

  def _getOnSetKeys(self) -> tuple[str, ...]:
    return maybe(self.__on_set_keys__, ())

  def _getPreDeleteKeys(self) -> tuple[str, ...]:
    return maybe(self.__pre_delete_keys__, ())

  def _getOnDeleteKeys(self) -> tuple[str, ...]:
    return maybe(self.__on_delete_keys__, ())

  def _getSetNameKeys(self) -> tuple[str, ...]:
    return maybe(self.__set_name_keys__, ())

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  SETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @staticmethod
  def _peelCallback(callback: Any) -> tuple:
    """
    A callback may be a method, a classmethod or a staticmethod, the last
    two with '@classmethod' or '@staticmethod' written below the decorator,
    and the decorator needs the function under the layer, for its name and
    for 'flexCall', since a 'classmethod' object has no '__name__' before
    Python 3.10. Anything else, as a 'functools.partial' or a builtin, has
    no function to be found by name.

    Implementation
    --------------

    One 'classmethod' or 'staticmethod' layer is taken off with
    'object.__getattribute__' reading '__func__'.

    Parameters
    ----------

    callback : Any
      What the decorator received.

    Returns
    -------

    tuple
      The kind, 'classmethod', 'staticmethod' or None for a plain
      function, and the function.

    Raises
    ------

    TypeException
      The callback is neither a plain function nor a classmethod or
      staticmethod over one.
    """
    if isinstance(callback, Func):
      return None, callback
    for kind in (classmethod, staticmethod):
      if isinstance(callback, kind):
        func = object.__getattribute__(callback, '__func__')
        if isinstance(func, Func):
          return kind, func
    raise TypeException(
      'callback',
      callback,
      Func,
      classmethod,
      staticmethod
      )

  @classmethod
  def _wrapCallback(cls, callback: Any) -> Any:
    """
    A decorator returns the callback it received, its function wrapped by
    'flexCall' so that it may declare fewer parameters than it is passed,
    and still of the kind it was declared as.

    Parameters
    ----------

    callback : Any
      A plain function, or a classmethod or staticmethod over one.

    Returns
    -------

    Any
      The 'flexCall' wrapper, under a new layer of the same kind.
    """
    kind, func = cls._peelCallback(callback)
    if kind is None:
      return flexCall(func)
    return kind(flexCall(func))

  def _getCallbackName(self, role: str, callback: Any) -> str:
    """
    A callback is found again by name on the class of the instance, so the
    name recorded must be the one the class actually stores it at, read
    through a 'classmethod' or 'staticmethod' layer, and anything with no
    function to be found by name must be refused before a name is
    recorded.

    Implementation
    --------------

    The function is taken from under its layer by '_peelCallback', which
    refuses anything else. A private name, two leading underscores and not
    two trailing, is mangled as Python mangles it, with the class taken
    from the '__qualname__' of the function. A lambda, or a private
    function defined inside another function, cannot be found by any
    lookup and is refused.

    Parameters
    ----------

    role : str
      The name of the decorator, for the message.

    callback : Any
      The decorated function.

    Returns
    -------

    str
      The name to record.

    Raises
    ------

    TypeException
      The callback is neither a plain function nor a classmethod or
      staticmethod over one.

    NamelessCallback
      The callback cannot be found by name.
    """
    _, func = self._peelCallback(callback)
    name: str = object.__getattribute__(func, '__name__')
    if name == '<lambda>':
      raise NamelessCallback(self, role, callback)
    if str.startswith(name, '__') and not str.endswith(name, '__'):
      qualName: str = object.__getattribute__(func, '__qualname__')
      qualParts = str.split(qualName, '.')
      if len(qualParts) < 2 or qualParts[-2] == '<locals>':
        raise NamelessCallback(self, role, callback)
      className = str.lstrip(qualParts[-2], '_')
      if not className:
        #  Python mangles nothing in a class named with underscores alone.
        return name
      return '_%s%s' % (className, name)
    return name

  def preGet(self, callback: F) -> F:
    existing = self._getPreGetKeys()
    name = self._getCallbackName('preGet', callback)
    object.__setattr__(self, '__pre_get_keys__', (*existing, name))
    return self._wrapCallback(callback)

  def onGet(self, callback: F) -> F:
    existing = self._getOnGetKeys()
    name = self._getCallbackName('onGet', callback)
    object.__setattr__(self, '__on_get_keys__', (*existing, name))
    return self._wrapCallback(callback)

  def preSet(self, callback: F) -> F:
    existing = self._getPreSetKeys()
    name = self._getCallbackName('preSet', callback)
    object.__setattr__(self, '__pre_set_keys__', (*existing, name))
    return self._wrapCallback(callback)

  def onSet(self, callback: F) -> F:
    """
    A class may need to react after every write of the descriptor through
    an instance, with the value as stored.

    Implementation
    --------------

    The name of the method is recorded, and 'hookOnSet' calls what the
    class of the instance holds under it by its kind: a method with the
    instance and the value, a classmethod with the class and the value, a
    staticmethod with the value. 'preGet', 'onGet', 'preSet', 'preDelete',
    'onDelete' and 'setName' work the same way for their moments.

    Parameters
    ----------

    callback : F
      A function of the class body, or a classmethod or staticmethod over
      one.

    Returns
    -------

    F
      The function wrapped by 'flexCall', under a layer of the kind it
      came in.

    Raises
    ------

    NamelessCallback
      The function cannot be found by name.

    TypeException
      The object is neither a function nor a classmethod or staticmethod
      over one, as a 'functools.partial' is.
    """
    existing = self._getOnSetKeys()
    name = self._getCallbackName('onSet', callback)
    object.__setattr__(self, '__on_set_keys__', (*existing, name))
    return self._wrapCallback(callback)

  def preDelete(self, callback: F) -> F:
    existing = self._getPreDeleteKeys()
    name = self._getCallbackName('preDelete', callback)
    object.__setattr__(self, '__pre_delete_keys__', (*existing, name))
    return self._wrapCallback(callback)

  def onDelete(self, callback: F) -> F:
    existing = self._getOnDeleteKeys()
    name = self._getCallbackName('onDelete', callback)
    object.__setattr__(self, '__on_delete_keys__', (*existing, name))
    return self._wrapCallback(callback)

  def setName(self, callback: F) -> F:
    existing = self._getSetNameKeys()
    name = self._getCallbackName('setName', callback)
    object.__setattr__(self, '__set_name_keys__', (*existing, name))
    return self._wrapCallback(callback)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def clone(self) -> Self:
    """
    'THIS[Parent].name' must give a subclass its own copy of an inherited
    descriptor, and the second name of 'a = b = AttriBox[int](0)' must get
    a descriptor of its own. The copy must carry what the descriptor
    captured, its arguments, field type and callbacks, and nothing tied to
    where it was placed. 'copy.copy' cannot serve, since a box answers it
    with itself.

    Implementation
    --------------

    The instance dictionary is copied field by field, except the owner,
    the field name, '__private_name__', the stack of frames, which starts
    empty, and the record of the read hooks running. A subclass keeping a
    cache built from the field name clears it when the copy is placed.

    Returns
    -------

    BaseDescriptor
      The copy, unplaced.
    """
    cls = type(self)
    new = object.__new__(cls)
    skipped = (
      '__field_owner__',
      '__field_name__',
      '__private_name__',
      '__call_chain__',
      '__get_lock__',
    )
    for key, value in vars(self).items():
      if key in skipped:
        continue
      object.__setattr__(new, key, value)
    object.__setattr__(new, '__call_chain__', [])
    return new

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @staticmethod
  def _findRawCallback(owner: type, key: str) -> Any:
    """
    A callback is called by the kind of method the class holds at its
    name, so it must be found as the class holds it, a 'classmethod' or
    'staticmethod' object included, and not as a read of the name gives
    it, past any '__getattr__' or '__class_getattr__'.

    Implementation
    --------------

    The first own dictionary along the resolution order holding the name
    answers.

    Parameters
    ----------

    owner : type
      The class of the instance.

    key : str
      The recorded name.

    Returns
    -------

    Any
      What the class holds at the name.

    Raises
    ------

    AttributeError
      No class along the resolution order holds the name.
    """
    for cls in owner.__mro__:
      try:
        return cls.__dict__[key]
      except KeyError:
        continue
    #  The rest of the method is reached by the following:
    #  - No class along the resolution order holds the name, as when a
    #    subclass deleted the callback; Python's own refusal is raised
    return type.__getattribute__(owner, key)

  @staticmethod
  def _bindRaw(raw: Any, instance: Any, owner: type) -> Any:
    """
    What the class holds at a name must be bound to the instance as Python
    binds it for 'instance.name': a function to the instance, a
    classmethod to the class, a staticmethod to nothing, and any other
    descriptor, as the dispatcher of overloads, through its own '__get__'.

    Parameters
    ----------

    raw : Any
      What the class holds at the name.

    instance : Any
      The instance of the access.

    owner : type
      The class of the instance.

    Returns
    -------

    Any
      The bound callable.
    """
    try:
      get = type.__getattribute__(type(raw), '__get__')
    except AttributeError:
      #  This branch is reached by the following:
      #  - The class holds an object that is no descriptor at the name, as a
      #    callable instance
      return raw
    return get(raw, instance, owner)

  def _bindCallback(self, instance: Any, owner: type, key: str) -> Any:
    """
    A 'Field' calls the accessor at a name with exactly its arguments,
    bound as Python binds 'instance.name'.

    Parameters
    ----------

    instance : Any
      The instance of the access.

    owner : type
      The class the accessor is looked up on.

    key : str
      The recorded name.

    Returns
    -------

    Any
      The bound callable.
    """
    raw = self._findRawCallback(owner, key)
    return self._bindRaw(raw, instance, owner)

  def _callCallback(self, instance: Any, key: str, *args, **kwargs) -> None:
    """
    A notification is found by name on the class of the instance, so a
    subclass may put any kind of method there, and the notification must
    reach it as Python would call 'instance.name(*args)': a method
    receives the instance, a classmethod the class of the instance, a
    staticmethod the arguments alone. A method declaring fewer parameters
    than it is passed must still be called, without a new wrapper being
    built at every access.

    Implementation
    --------------

    The function of a method, classmethod or staticmethod is called
    through its 'flexCall' wrapper, cached by '_getWrapper', with the
    receiver its kind takes. Anything else at the name is bound by
    '_bindRaw' and called with the arguments as they are.

    Parameters
    ----------

    instance : Any
      The instance of the access.

    key : str
      The recorded name.

    *args
      The arguments after the instance: the value, where there is one.

    **kwargs
      Keyword arguments of the hook, passed on.
    """
    owner = type(instance)
    raw = self._findRawCallback(owner, key)
    if isinstance(raw, Func):
      return self._getWrapper(raw)(instance, *args, **kwargs)
    if isinstance(raw, classmethod):
      func = object.__getattribute__(raw, '__func__')
      return self._getWrapper(func)(owner, *args, **kwargs)
    if isinstance(raw, staticmethod):
      func = object.__getattribute__(raw, '__func__')
      return self._getWrapper(func)(*args, **kwargs)
    #  The rest of the method is reached by the following:
    #  - A subclass holds another descriptor at the name, as the dispatcher
    #    its overloads of the name build
    #  - A subclass holds an object that is no descriptor at the name
    return self._bindRaw(raw, instance, owner)(*args, **kwargs)

  def _getWrapper(self, func: Func) -> Func:
    """
    The 'flexCall' wrapper of a callback function is built once and kept.

    Implementation
    --------------

    The wrapper is kept in '__callback_wrappers__', keyed by the function
    itself, so a class that replaces its callback later gets the function
    it now holds; 'flexCall' returns a function wrapped already as it is.

    Parameters
    ----------

    func : Func
      The function.

    Returns
    -------

    Func
      The wrapper.
    """
    wrappers = self.__callback_wrappers__
    if wrappers is None:
      wrappers = dict()
      object.__setattr__(self, '__callback_wrappers__', wrappers)
    try:
      return wrappers[func]
    except KeyError:
      wrapped = flexCall(func)
      wrappers[func] = wrapped
      return wrapped

  def hookPreGet(self, instance: Any, **kwargs) -> None:
    for key in self._getPreGetKeys():
      self._callCallback(instance, key, **kwargs)

  def hookOnGet(self, instance: Any, value: Any, **kwargs) -> None:
    for key in self._getOnGetKeys():
      self._callCallback(instance, key, value, **kwargs)

  def hookPreSet(self, instance: Any, value: Any, **kwargs) -> None:
    for key in self._getPreSetKeys():
      self._callCallback(instance, key, value, **kwargs)

  def hookOnSet(self, instance: Any, value: Any, **kwargs) -> None:
    for key in self._getOnSetKeys():
      self._callCallback(instance, key, value, **kwargs)

  def hookPreDelete(self, instance: Any, **kwargs) -> None:
    for key in self._getPreDeleteKeys():
      self._callCallback(instance, key, **kwargs)

  def hookOnDelete(self, instance: Any, **kwargs) -> None:
    for key in self._getOnDeleteKeys():
      self._callCallback(instance, key, **kwargs)

  def hookSetName(self, owner: type, name: str, **kwargs) -> None:
    """
    A class may react as the descriptor is placed in it, before any
    instance exists, so a 'setName' callback receives the class and the
    descriptor, by the kind of method the class holds at its name.

    Implementation
    --------------

    A classmethod, and a plain function, receive the class and then the
    descriptor; a staticmethod the descriptor alone; anything else is
    bound to the class by '_bindRaw' and receives the descriptor. Each
    function is called through its 'flexCall' wrapper.

    Parameters
    ----------

    owner : type
      The class the descriptor is placed in.

    name : str
      The name it is placed at.
    """
    for key in self._getSetNameKeys():
      raw = self._findRawCallback(owner, key)
      if isinstance(raw, Func):
        self._getWrapper(raw)(owner, self, **kwargs)
        continue
      if isinstance(raw, classmethod):
        func = object.__getattribute__(raw, '__func__')
        self._getWrapper(func)(owner, self, **kwargs)
        continue
      if isinstance(raw, staticmethod):
        func = object.__getattribute__(raw, '__func__')
        self._getWrapper(func)(self, **kwargs)
        continue
      #  The rest of the loop is reached by the following:
      #  - The class holds another descriptor at the name, or an object
      #    that is no descriptor
      self._bindRaw(raw, None, owner)(self, **kwargs)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __set_name__(self, owner: type, name: str, **kwargs) -> None:
    """
    One descriptor bound to two names in a class body must give two
    attributes, and one descriptor bound in the bodies of two classes must
    be refused, since it cannot serve both.

    Implementation
    --------------

    The first placement records the owner and name and calls the
    'setName' callbacks, through 'Object.__set_name__'. A second name in
    the same class receives a clone, which is safe since 'type.__new__'
    iterates a copy of the class dictionary.

    Parameters
    ----------

    owner : type
      The class being created.

    name : str
      The name the descriptor is bound to.

    Raises
    ------

    SharedDescriptor
      The descriptor is placed on another class already.
    """
    placedOwner: Optional[type] = self.__field_owner__
    if placedOwner is not None:
      placedName = self.__field_name__
      if placedOwner is not owner:
        raise SharedDescriptor(self, placedOwner, placedName, owner, name)
      if placedName != name:
        #  'type.__new__' runs '__set_name__' over a copy of the class
        #  dict, so the second name may take the clone here.
        clone = self.clone()
        type.__setattr__(owner, name, clone)
        return clone.__set_name__(owner, name, **kwargs)
    return super().__set_name__(owner, name, **kwargs)

  # @formatter:off
  if TYPE_CHECKING:  # pragma: no cover, no mutate
    @overload
    def __get__(self, instance: None, owner: type) -> Self: ...
    @overload
    def __get__(self, instance: Any, owner: type) -> T: ...

    def __get__(self, instance: Any, owner: type) -> Union[Any, T]:
      return super().__get__(instance, owner)

    #  Writes require T statically, so type-checked callers are held
    #  to the field type. Runtime salvage still rescues dynamic or
    #  untyped callers that pass something coercible.
    # noinspection PyMethodOverriding
    def __set__(self, instance: Any, value: Any) -> None: ...
  # @formatter:on
