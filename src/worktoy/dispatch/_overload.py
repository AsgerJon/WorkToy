"""
The 'overload' decorator registers a type signature for one overloaded
function.
"""
#  Apache-2.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from types import FunctionType
from typing import TYPE_CHECKING

from ..core.sentinels import ARGS
from ..utilities import maybe, textFmt
from ..utilities.combinatorics import Arrangements
from ..waitaminute import MissingVariable, TypeException
from ..waitaminute.dispatch import BareOverload
from ..waitaminute.meta import MixedMethodKind
from . import TypeSig, PermuterMethod
from ._dispatcher import _MAX_EXPANDED_FLEX

if TYPE_CHECKING:  # pragma: no cover, no mutate
  from typing import Any, Callable, TypeAlias, Self, Iterator, Never
  from typing import Optional

  Method: TypeAlias = Callable[..., Any]
  Decorator: TypeAlias = Callable[[Method], Any]


class overload:  # NOQA
  """
  Python keeps only the last function bound to a name in a class body,
  so a method cannot be written once per signature:

    class Frob(BaseObject):

      @overload(int)
      def __init__(self, n: int) -> None:
        ...

      @overload(int, int)
      def __init__(self, n: int, m: int) -> None:
        ...

  Each declaration must survive the rebinding of its name and record its
  signature, so that all the declarations of a name, with those the class
  inherits, can become one dispatcher once the class exists. One function
  may also serve several signatures, or be the fallback or the finalizer
  of its name, by stacking decorators. An overloaded name may be a
  classmethod, as an alternative constructor taking several kinds of
  argument, or a staticmethod, with '@classmethod' or '@staticmethod'
  written above '@overload', below it, or between two decorators of a
  stack. Only a class whose metaclass is
  based on 'BaseMeta' has such a namespace; a class whose metaclass comes
  from another library overloads its methods through a metaclass combined
  with 'BaseMeta'. An 'overload' left in the body of any other class is
  refused as the class is created, and a record called anywhere is
  refused at the call.

  Implementation
  --------------

  '@overload(...)' returns a decorator, and the decorator returns an
  'overload' object recording the function and the signature; it does no
  dispatching. A decorator stacked above another adds its signature to
  the 'overload' below it. The class methods 'flex', 'fallback' and
  'finalize' declare the other roles the same way. A decorator given a
  'classmethod' or 'staticmethod' object takes the function out of it and
  keeps its kind; given one over the record of the decorator below, it
  extends that record, which takes the kind. 'LoadSpaceHook' does the
  same for one written above the whole stack. A stack holding both kinds
  raises 'MixedMethodKind'.
  The namespace of a 'BaseObject' class claims every 'overload' object,
  so the namespace never stores one, and 'LoadSpaceHook' builds the
  'Dispatcher' of each name, refusing a body that declares one name as
  two kinds of method; see 'Dispatcher' for how calls are matched, and
  for why the most specific signature is declared first. A subclass
  declaring an overload at a name it inherits keeps the inherited
  overloads and adds its own, an equal signature replacing the inherited
  one. A subclass overloading the name as another kind of method
  overrides it as a plain definition does, hiding the inherited
  overloads.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  STATIC METHODS   # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @staticmethod
  def peelMethodKinds(obj: Any) -> tuple[tuple, Any]:
    """
    '@classmethod' and '@staticmethod' may be written above '@overload',
    below it, or between two decorators of a stack, so a decorator and
    'LoadSpaceHook' must both find the function or the record under such
    layers, together with the kind of method each layer declares.

    Implementation
    --------------

    Each 'classmethod' or 'staticmethod' layer, a subclass of either
    included, is taken off with 'object.__getattribute__' reading
    '__func__', outermost first, and its kind recorded as the builtin.

    Parameters
    ----------

    obj : Any
      What a decorator or the class body received.

    Returns
    -------

    tuple[tuple, Any]
      The kinds of the layers, outermost first, and what they wrapped.
    """
    kinds = []
    while isinstance(obj, (classmethod, staticmethod)):
      if isinstance(obj, classmethod):
        kinds.append(classmethod)
      else:
        kinds.append(staticmethod)
      obj = object.__getattribute__(obj, '__func__')
    return (*kinds,), obj

  @staticmethod
  def agreeMethodKind(
      kinds: tuple,
      name: str,
      className: Optional[str] = None,
  ) -> Any:
    """
    One function is one kind of method, so the kinds a stack of decorators
    declares for it must be one kind. A classmethod and a staticmethod in
    one stack would mean something different on each version of Python.

    Implementation
    --------------

    The first kind is compared with every other by identity.

    Parameters
    ----------

    kinds : tuple
      The kinds declared, outermost first, each 'classmethod' or
      'staticmethod'.

    name : str
      The name of the function or of the overloaded name, for the
      message.

    className : str, optional
      The name of the class whose body declares it, for the message.

    Returns
    -------

    Any
      The kind, or 'None' when nothing declares one.

    Raises
    ------

    MixedMethodKind
      Two of the kinds disagree.
    """
    if not kinds:
      return None
    first = kinds[0]
    for kind in kinds[1:]:
      if kind is not first:
        raise MixedMethodKind(className, name, (first, kind))
    return first

  @staticmethod
  def _getFunctionName(func: Any) -> str:
    try:
      name = object.__getattribute__(func, '__name__')
    except AttributeError:
      #  This branch is reached by the following:
      #  - A decorator received a value without a name of its own, as a
      #    number or a 'functools.partial'
      return repr(func)
    else:
      return name

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Private Variables
  __sig_func_dict__ = None
  __variadic_sig_func_list__ = None
  __flex_sig_func_list__ = None
  __latest_func__ = None
  __fallback_func__ = None
  __finalizer_func__ = None
  __method_kind__ = None

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def getMethodKind(self) -> Any:
    """
    The dispatcher of a name must know whether its functions are instance
    methods, classmethods or staticmethods, and a decorator given a
    'classmethod' or 'staticmethod' object is the one to learn it.

    Returns
    -------

    Any
      'classmethod' or 'staticmethod', or 'None' when the decorators of
      the record were given a plain function.
    """
    return self.__method_kind__

  def _getSigFuncDict(self) -> dict[TypeSig, Method]:
    return maybe(self.__sig_func_dict__, dict())

  def getVariadics(self) -> list[tuple[TypeSig, Method]]:
    """
    'LoadSpaceHook' must read the variadic signatures of an 'overload'
    apart from the concrete ones, since they go to the dispatcher by
    another route.

    Returns
    -------

    list[tuple[TypeSig, Method]]
      The variadic pairs in declaration order, 'Method' being
      'Callable[..., Any]'.
    """
    return maybe(self.__variadic_sig_func_list__, [])

  def getFlexes(self) -> list[tuple[TypeSig, Method]]:
    """
    'LoadSpaceHook' must read the flexible declarations of more than three
    classes apart from the concrete signatures, since the dispatcher holds
    each of them as one registration standing for every order.

    Returns
    -------

    list[tuple[TypeSig, Method]]
      The pairs in declaration order, each signature in the order the
      function takes its arguments, 'Method' being 'Callable[..., Any]'.
    """
    return maybe(self.__flex_sig_func_list__, [])

  def _getLatestFunc(self) -> Method:
    if self.__latest_func__ is None:
      raise RuntimeError(
          "no function has been registered on this 'overload' yet"
      )
    return self.__latest_func__

  def isFallback(self) -> bool:
    return False if self.__fallback_func__ is None else True

  def getFallback(self, ) -> Method:
    return self.__fallback_func__

  def isFinalizer(self) -> bool:
    return False if self.__finalizer_func__ is None else True

  def getFinalizer(self, ) -> Method:
    return self.__finalizer_func__

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  SETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def _addSigFunc(self, sig: TypeSig, func: Method) -> None:
    """
    A stack of decorators may declare several signatures for one function,
    and a decorator stacked above must know which function the stack is
    for.

    Implementation
    --------------

    A signature ending in an 'ARGS' instance goes to the variadic list, any
    other into the concrete mapping, where an equal signature keeps its
    first position. The function becomes the latest one.

    Parameters
    ----------

    sig : TypeSig
      The signature.

    func : Method
      The function, or a 'PermuterMethod' of a flexible declaration.
    """
    raw = sig.getRawTypes()
    if raw and isinstance(raw[-1], ARGS):
      variadics = self.getVariadics()
      self.__variadic_sig_func_list__ = [*variadics, (sig, func,)]
    else:
      existing = self._getSigFuncDict()
      existing[sig] = func
      self.__sig_func_dict__ = existing
    self.__latest_func__ = func

  def _takeMethodKinds(self, kinds: tuple) -> None:
    """
    A '@classmethod' or '@staticmethod' written between two decorators of
    a stack declares the kind of the one function the stack decorates, as
    it does written above the stack or below it, so the record of the
    decorator below must take that kind, and refuse it when the stack
    declares another kind elsewhere.

    Implementation
    --------------

    The kinds of the layers, outermost first, are agreed with the kind the
    record holds already, which comes from below them, and the agreed kind
    is recorded.

    Parameters
    ----------

    kinds : tuple
      The kinds of the layers between this record and the decorator above
      it, outermost first; empty when nothing stands between them.

    Raises
    ------

    MixedMethodKind
      The stack declares a classmethod and a staticmethod.
    """
    if self.__method_kind__ is None:
      #  This branch is reached by the following:
      #  - No '@classmethod' or '@staticmethod' is written lower in the stack
      stack = kinds
    else:
      #  This branch is reached by the following:
      #  - '@classmethod' or '@staticmethod' is written lower in the stack,
      #    below its last decorator or between two decorators below this one
      stack = (*kinds, self.__method_kind__)
    name = self._getFunctionName(self._getLatestFunc())
    self.__method_kind__ = self.agreeMethodKind(stack, name)

  def _extendLatest(self, sig: TypeSig) -> None:
    self._addSigFunc(sig, self._getLatestFunc())

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __new__(cls, *types, **kwargs) -> Decorator:
    """
    '@overload(int, str)' must check its signature where it is written and
    give a decorator, which in turn must give an 'overload' object, new or
    the one of the decorator below it in a stack.

    Implementation
    --------------

    The entries are read through 'TypeSig.starARGS' and checked by
    'TypeSig.validateTypes' when '@overload(...)' is evaluated, and the
    decorator is returned instead of an instance. The decorator takes a
    'classmethod' or 'staticmethod' apart with 'peelMethodKinds'; a record
    beneath takes its kind and the signature, and a function is checked and
    given a new record keeping the kind. The class keyword '_root=True' is
    internal and builds a bare instance.

    Parameters
    ----------

    *types : type
      The classes of the positional arguments after 'self', optionally
      ending in an 'ARGS'.

    Returns
    -------

    Decorator
      A 'Callable[[Method], Any]' returning an 'overload' object.

    Raises
    ------

    TypeException
      An entry is not a class, or an 'ARGS' of one at the end.

    TypeError
      A keyword is given, or an entry is 'None' or a sentinel other than
      'THIS'.

    UncheckableType
      An entry is a class 'isinstance' refuses.

    BareOverload
      The decorator is written without parentheses.

    TypeException
      What lies under any 'classmethod' or 'staticmethod' cannot be called.

    MixedMethodKind
      The decorator is given a function decorated as both a classmethod
      and a staticmethod, or a stack declares both kinds.
    """

    if kwargs.get('_root', False):
      return super(overload, cls).__new__(cls)
    cls._refuseKeywords(**kwargs)
    cls._refuseBare('overload', *types)
    types = TypeSig.starARGS(*types)
    TypeSig.validateTypes(*types)

    def decorator(func: Method) -> Self:
      sig = TypeSig(*types, )
      kinds, func = cls.peelMethodKinds(func)
      if isinstance(func, cls):
        func._takeMethodKinds(kinds)
        func._extendLatest(sig)
        return func
      kind = cls.agreeMethodKind(kinds, cls._getFunctionName(func))
      cls._refuseUncallable(func)
      self = super(overload, cls).__new__(cls)
      self.__method_kind__ = kind
      self._addSigFunc(sig, func)
      return self

    return decorator

  def __init__(self, *args, **kwargs) -> None:
    pass

  @classmethod
  def flex(cls, *types: type) -> Decorator:
    """
    Some methods take arguments whose order carries no meaning, as a label
    taking a 'str' and an 'int', and their callers should be free to pass
    them in any order. Only the orders of the given classes may match;
    every other call is left to the other signatures and the fallback.

    Implementation
    --------------

    Up to three classes, each distinct order of the classes is recorded
    with a 'PermuterMethod' that puts the arguments back in the declared
    order. More classes are recorded once, in the declared order, since
    the orders number the factorial of the classes; the dispatcher matches
    them in any order. A decorator stacked above registers the function
    itself, not a wrapper.

    Parameters
    ----------

    *types : type
      The classes of the positional arguments after 'self', in the order
      the function declares them.

    Returns
    -------

    Decorator
      A 'Callable[[Method], Any]' returning an 'overload' object.

    Raises
    ------

    TypeException
      An entry is not a class; an 'ARGS' is refused too, since the entries
      are reordered.

    TypeError
      An entry is 'None', or a sentinel other than 'THIS'.

    UncheckableType
      An entry is a class 'isinstance' refuses.

    BareOverload
      The decorator is written without parentheses.
    """
    cls._refuseBare('overload.flex', *types)
    types = TypeSig.starARGS(*types)
    TypeSig.validateTypes(*types, variadic=False)

    def decorator(func: Method) -> Self:
      self, function = cls._stackOn(func)
      if len(types) > _MAX_EXPANDED_FLEX:
        flexes = self.getFlexes()
        self.__flex_sig_func_list__ = [*flexes, (TypeSig(*types), function)]
        return self
      for arrangement in Arrangements(*types):
        sig = TypeSig(*arrangement.values)
        if TYPE_CHECKING:  # pragma: no cover, no mutate
          assert isinstance(function, FunctionType)
        load = PermuterMethod(function, arrangement)
        self._addSigFunc(sig, load)
      #  A decorator stacked above registers the function itself, not the
      #  wrapper of the last arrangement.
      self.__latest_func__ = function
      return self

    return decorator

  @classmethod
  def fallback(cls, func) -> Self:
    """
    A call no declaration of the name accepts may need a function of its
    own instead of an error.

    Parameters
    ----------

    func : Method
      The function, or the 'overload' of a decorator below in the stack.

    Returns
    -------

    overload
      The 'overload' of the stack, or a new one.
    """
    self, function = cls._stackOn(func)
    self.__fallback_func__ = function
    return self

  @classmethod
  def finalize(cls, func: Method) -> Self:
    """
    Some work must follow every call of the name, whichever declaration
    took it and whether or not it raised.

    Parameters
    ----------

    func : Method
      The function, or the 'overload' of a decorator below in the stack.

    Returns
    -------

    overload
      The 'overload' of the stack, or a new one.
    """
    self, function = cls._stackOn(func)
    self.__finalizer_func__ = function
    return self

  @classmethod
  def _stackOn(cls, func: Any) -> tuple[Self, Method]:
    """
    The role decorators 'flex', 'fallback' and 'finalize' are called with
    whatever the decorator below them returned, and every decorator of a
    stack must register the one function the stack decorates.

    Implementation
    --------------

    Any 'classmethod' or 'staticmethod' is taken off first. An 'overload'
    beneath takes its kind and is returned with its latest function; a
    function is checked and given a new 'overload' keeping that kind.

    Parameters
    ----------

    func : Any
      A function, possibly a 'classmethod' or 'staticmethod', or an
      'overload'.

    Returns
    -------

    tuple[overload, Method]
      The 'overload' and the function.

    Raises
    ------

    TypeException
      What lies under any 'classmethod' or 'staticmethod' cannot be called.

    MixedMethodKind
      The function is decorated as both a classmethod and a staticmethod,
      or the stack declares both kinds.
    """
    kinds, func = cls.peelMethodKinds(func)
    if isinstance(func, cls):
      func._takeMethodKinds(kinds)
      return func, func._getLatestFunc()
    kind = cls.agreeMethodKind(kinds, cls._getFunctionName(func))
    cls._refuseUncallable(func)
    self = cls(_root=True)
    self.__method_kind__ = kind
    self.__latest_func__ = func
    return self, func

  @staticmethod
  def _refuseUncallable(func: Any) -> None:
    """
    The dispatcher a namespace builds calls every registered function
    itself, so what lies under the method kinds of a declaration must be
    callable, or the mistake would show only at the first call.

    Parameters
    ----------

    func : Any
      What the decorator registers.

    Raises
    ------

    TypeException
      'func' cannot be called.
    """
    if not callable(func):
      raise TypeException('func', func, FunctionType)

  @classmethod
  def _refuseBare(cls, decorator: str, *types) -> None:
    """
    '@overload' written without parentheses, as 'typing.overload' is
    written, hands the function to the decorator where the first class of
    the signature belongs, and the refusal must say that the parentheses
    are missing rather than that a function is no class.

    Implementation
    --------------

    A single entry that is a function, under any 'classmethod' or
    'staticmethod' layers, or a record of another decorator, is refused.

    Parameters
    ----------

    decorator : str
      The decorator, 'overload' or 'overload.flex', for the message.

    *types
      What the decorator received as its signature.

    Raises
    ------

    BareOverload
      The single entry is a function or a record.
    """
    if len(types) != 1:
      return
    _, entry = cls.peelMethodKinds(types[0])
    if isinstance(entry, (FunctionType, cls)):
      raise BareOverload(decorator, types[0])

  @staticmethod
  def _refuseKeywords(**kwargs) -> None:
    """
    'overload' takes no keyword, and a misspelled keyword must not pass
    unnoticed.

    Raises
    ------

    TypeError
      Any keyword is given, worded as Python words it.
    """
    for key in kwargs:
      infoSpec = """overload() got an unexpected keyword argument '%s'"""
      raise TypeError(infoSpec % key)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __getattr__(self, key: str) -> Any:
    if self.__latest_func__ is None:
      raise MissingVariable(self, key)
    func = self.__latest_func__
    try:
      value = getattr(func, key)
    except AttributeError:
      raise MissingVariable(self, key)
    else:
      return value

  def __iter__(self, ) -> Iterator[tuple[TypeSig, Method]]:
    """
    'LoadSpaceHook' must read the concrete signatures an 'overload'
    records, each with its function.

    Yields
    ------

    tuple[TypeSig, Method]
      Each concrete pair; the variadic ones come from 'getVariadics'.
    """
    yield from self._getSigFuncDict().items()

  def __set_name__(self, owner: type, name: str) -> Never:
    """
    In the body of a class whose metaclass is not based on 'BaseMeta',
    nothing claims an 'overload' record or builds a dispatcher from it, so
    the record would stay at its name, the class statement would succeed,
    and the mistake would show only at the first call, far from the
    class. The class statement is the place to refuse it.

    Implementation
    --------------

    Python calls this method only for a record left in the dictionary of
    the class, which the namespace of a 'BaseMeta' metaclass never stores.
    Before Python 3.12 the refusal reaches the class statement wrapped in
    a 'RuntimeError'.

    Parameters
    ----------

    owner : type
      The class being created.

    name : str
      The name the record is bound to.

    Raises
    ------

    TypeError
      Always.
    """
    infoSpec = """The class body of '%s' leaves the 'overload' of '%s' at
    its name: the metaclass of '%s' builds no dispatcher from it, and an
    'overload' only records a signature, so nothing would ever call it. A
    class using '@overload' is based on 'BaseObject', or built by a
    metaclass based on 'BaseMeta'; a class whose metaclass comes from
    another library takes a metaclass combined with 'BaseMeta'."""
    ownerName = owner.__name__
    raise TypeError(textFmt(infoSpec % (ownerName, name, ownerName)))

  def __call__(self, *args, **kwargs) -> Never:
    """
    A record is never called: it holds signatures for the namespace that
    builds the dispatcher. A call reaching one means it was declared where
    no namespace claims it, as on a function outside a class, and the
    error must say so, rather than only that the record cannot be called.

    Raises
    ------

    TypeError
      Always.
    """
    infoSpec = """The 'overload' of '%s' was called. An 'overload' only
    records a signature, which the namespace of a class based on
    'BaseObject' turns into a dispatcher, and is never called itself. A
    class using '@overload' is based on 'BaseObject', or built by a
    metaclass based on 'BaseMeta', as a metaclass combined with one of
    another library is; a function outside a class is not
    overloaded."""
    name = self._getFunctionName(self._getLatestFunc())
    raise TypeError(textFmt(infoSpec % name))

  def __str__(self, ) -> str:
    if self.__latest_func__ is None:
      return textFmt("""overload with no function registered so far""")
    roles = [str(sig) for sig, _ in self._getSigFuncDict().items()]
    roles += ['%s in any order' % sig for sig, _ in self.getFlexes()]
    roles += [str(sig) for sig, _ in self.getVariadics()]
    if self.isFallback():
      roles.append('the fallback')
    if self.isFinalizer():
      roles.append('the finalizer')
    infoSpec = """overload of function: '%s', registered as:<br><tab>%s"""
    name = self._getFunctionName(self._getLatestFunc())
    return textFmt(infoSpec % (name, '<br><tab>'.join(roles)))

  __repr__ = __str__
