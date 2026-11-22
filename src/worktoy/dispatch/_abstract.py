"""
The 'abstract' decorator declares a method a subclass has to write, and
is the record of that declaration.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

import dis
from types import FunctionType
from typing import TYPE_CHECKING

from ..utilities import textFmt
from ..waitaminute import TypeException

if TYPE_CHECKING:  # pragma: no cover, no mutate
  from typing import Any, Optional

_CO_VARARGS: int = 0x04  # CPython compile flag
_CO_VARKEYWORDS: int = 0x08  # CPython compile flag
#  CO_GENERATOR, CO_COROUTINE, CO_ITERABLE_COROUTINE, CO_ASYNC_GENERATOR
_CO_GENERATORS: int = 0x20 | 0x80 | 0x100 | 0x200

#  What Python compiles a blank body to, whichever way it is written:
#  a load of 'None' and a return, under the names of every version from
#  3.7 to 3.15. 'RESUME' opens every function from 3.11 on.
_SKIPPED_STEPS: tuple = ('RESUME', 'NOP')
_BLANK_STEPS: tuple = (
  'LOAD_CONST', 'LOAD_COMMON_CONSTANT', 'RETURN_VALUE', 'RETURN_CONST',
)



class abstract:  # NOQA
  """
  Some classes declare a method without having anything to run for it:
  every class based on them has to write it, as a model of a list has to
  say how many rows it holds. The class body must be able to say so at
  the method, for a bound method, a classmethod and a staticmethod, and
  for the signatures of an overloaded name:

    class Model(BaseObject, metaclass=ABCMeta):

      @abstract
      def rowCount(self) -> int: ...

      @overload(str, int)
      @abstract
      def data(self, index: str, role: int) -> Any: ...

  Such a declaration runs nothing, so a function with a body under it
  is a mistake and must be refused where it is written. What it declares
  must be on record, since a subclass writing the method is held to it:
  the kind of method, and what the method receives. And a call that
  does reach the declaration, as through 'super()', must do nothing.

  Implementation
  --------------

  '@abstract' over a blank function gives an 'abstract' object, the
  record of that function, as '@overload' gives a record of its own. A
  body of '...', of 'pass', of a docstring alone or of 'return None' is
  blank, Python compiling each to the same thing; any other body, and a
  generator or coroutine function, raises 'TypeError'. The record keeps
  the function, its name and its docstring, gives the shape of its
  parameters through 'getShape', and does nothing when called. Given a
  'classmethod' or 'staticmethod' object it returns one of the same kind
  over the record. Given the record of '@overload', it puts itself in
  the place of the function that record holds, so '@abstract' stands at
  any position among the '@overload' decorators of a stack. A class
  built by 'ABCMeta' of 'worktoy.mcls' holds its subclasses to what is
  declared, and the space hook of its namespace says so on each record
  of its body by setting '__abc_only__'. A record no such hook took is
  refused as its class is created, since nothing there would hold a
  subclass to it.

  Attributes
  ----------

  __wrapped__ : FunctionType
    The blank function.

  __name__, __qualname__, __module__, __doc__ : str
    Those of the blank function.

  __abc_only__ : bool
    'False' on a new record, and set to 'True' by the namespace of an
    abstract class for each record of its body.

  __declaring_class__ : type or None
    The class whose body declares the record, once that class exists,
    and 'None' until then. A class based on it inherits the record and
    leaves this as it is.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Private Variables
  __abc_only__: bool = False
  __declaring_class__: Optional[type] = None

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  STATIC METHODS   # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @staticmethod
  def _isBlank(func: FunctionType) -> bool:
    """
    A function under '@abstract' must have no implementation, and that
    must be read off the function itself, on every version of Python.

    Implementation
    --------------

    Python compiles a body of '...', of 'pass', of a docstring alone and
    of 'return None' to a load of 'None' and a return, and nothing else.
    The steps 'dis' gives are held to that: each is one of those two,
    under any of the names the versions give them, and carries no value
    but 'None'.

    Parameters
    ----------

    func : FunctionType
      The function.

    Returns
    -------

    bool
      Whether the body of the function is blank.
    """
    for step in dis.get_instructions(func):
      if step.opname in _SKIPPED_STEPS:
        continue
      if step.opname not in _BLANK_STEPS:
        return False
      if step.argval is not None:
        return False
    return True

  @staticmethod
  def shapeOf(func: FunctionType, kind: Any) -> tuple:
    """
    Whether a method written in a subclass can take what an abstract one
    declares is decided by what each receives: how many arguments by
    position, whether any number more, which by keyword alone, and
    whether any keyword. A default plays no part: a parameter counts the
    same with one or without.

    Implementation
    --------------

    The counts are read off the code of the function. The first
    positional parameter of a bound method or a classmethod is the
    receiver and is left out; a function taking the receiver through
    '*args' counts none, and one that cannot take a receiver at all
    counts -1, which fits nothing.

    Parameters
    ----------

    func : FunctionType
      The function.

    kind : Any
      'classmethod', 'staticmethod', or 'None' for a bound method.

    Returns
    -------

    tuple
      The number of positional parameters after the receiver, whether
      the function takes '*args', the names of its keyword-only
      parameters, and whether it takes '**kwargs'.
    """
    code = func.__code__
    count = code.co_argcount
    starred = True if code.co_flags & _CO_VARARGS else False
    doubled = True if code.co_flags & _CO_VARKEYWORDS else False
    if kind is not staticmethod:
      if count or not starred:
        count -= 1
    first = code.co_argcount
    keyed = code.co_varnames[first:first + code.co_kwonlyargcount]
    return count, starred, (*keyed,), doubled

  @staticmethod
  def fits(declared: tuple, written: tuple) -> bool:
    """
    A method written in a subclass implements an abstract one when it can
    receive everything the abstract one declares.

    Implementation
    --------------

    A written function takes exactly as many arguments by position as it
    has positional parameters, and with '*args' any number from there
    up. Where the declaration itself takes any number, the written one
    has to as well, from no more than the declared number. Each
    keyword-only parameter declared needs the same one or '**kwargs',
    and a declared '**kwargs' needs '**kwargs'.

    Parameters
    ----------

    declared : tuple
      The shape declared, as 'shapeOf' gives one.

    written : tuple
      The shape of the function written.

    Returns
    -------

    bool
      Whether the written shape can take what the declared one takes.
    """
    count, starred, keyed, doubled = declared
    writtenCount, writtenStarred, writtenKeyed, writtenDoubled = written
    if starred and not writtenStarred:
      return False
    if writtenStarred:
      if writtenCount > count:
        return False
    elif writtenCount != count:
      return False
    if doubled and not writtenDoubled:
      return False
    for name in keyed:
      if name not in writtenKeyed and not writtenDoubled:
        return False
    return True

  @staticmethod
  def describe(kind: Any, shape: tuple) -> str:
    """
    The refusal of a wrong implementation must say what was declared and
    what was written in the same words, so the two can be compared.

    Parameters
    ----------

    kind : Any
      'classmethod', 'staticmethod', or 'None' for a bound method.

    shape : tuple
      A shape as 'shapeOf' gives one.

    Returns
    -------

    str
      The kind and what it takes, as "a method taking 2 by position".
    """
    count, starred, keyed, doubled = shape
    if kind is classmethod:
      out = 'a classmethod taking %d' % count
    elif kind is staticmethod:
      out = 'a staticmethod taking %d' % count
    else:
      out = 'a method taking %d' % count
    if starred:
      out = '%s or more' % out
    out = '%s by position' % out
    for name in keyed:
      out = "%s, '%s' by keyword" % (out, name)
    if doubled:
      out = '%s, any keyword' % out
    return out

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def requireHost(self, mcls: type, className: str, name: str) -> None:
    """
    An abstract method is a claim on the classes based on its class, and
    only a namespace made for it holds them to the claim. Declared in
    any other class, the method would be answered with nothing and no
    subclass would ever be asked to write it, so the declaration must
    fail as that class is created.

    Implementation
    --------------

    The space hook of an abstract class sets '__abc_only__' on each
    record of its body, as 'ABCHook' of 'worktoy.mcls' does. A record
    whose flag is still 'False' was taken by no such hook.

    Parameters
    ----------

    mcls : type
      The metaclass of the class whose body declares the method, for
      the message.

    className : str
      The name of that class.

    name : str
      The name declared abstract.

    Raises
    ------

    TypeError
      No space hook of an abstract class took the record.
    """
    if self.__abc_only__:
      return
    infoSpec = """The class body of '%s' declares '%s' abstract, and its
    metaclass '%s' is not based on 'ABCMeta', so no class based on it
    would be held to writing '%s'. A class declaring abstract methods is
    built by 'ABCMeta' of 'worktoy.mcls'."""
    info = infoSpec % (className, name, mcls.__name__, name)
    raise TypeError(textFmt(info))

  def getShape(self, kind: Any) -> tuple:
    """
    What the blank function declares depends on the kind of method it
    is, which the layers around the record say, not the record.

    Parameters
    ----------

    kind : Any
      'classmethod', 'staticmethod', or 'None' for a bound method.

    Returns
    -------

    tuple
      The shape of the blank function, as 'shapeOf' gives it.
    """
    return self.shapeOf(self.__wrapped__, kind)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __new__(cls, func: Any) -> Any:
    """
    '@abstract' is written above a blank function, above or below
    '@classmethod' or '@staticmethod', and at any position among the
    '@overload' decorators of a stack. Whatever it receives, the one
    function of the stack must end up declared abstract, and anything
    that cannot be an abstract declaration must be refused at that line.

    Implementation
    --------------

    The 'classmethod' and 'staticmethod' layers are taken off first. A
    record of '@overload' underneath is asked to put a new 'abstract' in
    the place of its function, and is returned as it came. A function is
    checked and recorded, and returned under a layer of the kind it came
    in.

    Parameters
    ----------

    func : Any
      A blank function, a classmethod or staticmethod over one, or the
      record of an '@overload' decorator below.

    Returns
    -------

    Any
      The record, under a layer of the kind it came in, or the record of
      '@overload' it was given.

    Raises
    ------

    TypeException
      What lies under the layers is no plain function, as a function
      declared abstract already.

    TypeError
      The function has a body, or is a generator or coroutine function.

    MixedMethodKind
      The function is decorated as both a classmethod and a
      staticmethod.
    """
    #  Local import: 'overload' loads after this file, which it imports.
    from . import overload
    kinds, inner = overload.peelMethodKinds(func)
    if isinstance(inner, overload):
      inner._makeAbstract(cls)
      return func
    if not isinstance(inner, FunctionType):
      raise TypeException('func', inner, FunctionType)
    name: str = inner.__name__
    kind = overload.agreeMethodKind(kinds, name)
    if inner.__code__.co_flags & _CO_GENERATORS:
      infoSpec = """The function '%s' under '@abstract' is a generator or
      a coroutine function. An abstract method is declared on an ordinary
      function."""
      raise TypeError(textFmt(infoSpec % name))
    if not cls._isBlank(inner):
      infoSpec = """The function '%s' under '@abstract' has a body. An
      abstract method declares what a subclass has to write and runs
      nothing itself, so its body is left blank: '...', 'pass' or a
      docstring alone."""
      raise TypeError(textFmt(infoSpec % name))
    self = object.__new__(cls)
    self.__wrapped__ = inner
    self.__name__ = name
    self.__qualname__ = inner.__qualname__
    self.__module__ = inner.__module__
    self.__doc__ = inner.__doc__
    if kind is None:
      return self
    return kind(self)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __call__(self, *args, **kwargs) -> None:
    """
    A call may reach an abstract method, as through 'super()' from the
    method a subclass wrote, or on a class that is still abstract through
    a classmethod or a staticmethod. The declaration has nothing to run.

    Implementation
    --------------

    Whatever it is called with, it does nothing and returns 'None', as an
    abstract method of Python's 'abc' with a blank body does.
    """

  def __set_name__(self, owner: type, name: str) -> None:
    """
    A record left in the body of a class that no hosting metaclass built
    must fail as that class is created, not at the first call.

    Implementation
    --------------

    Python calls this method for a record held in the dictionary of a
    new class. 'requireHost' refuses a record whose '__abc_only__' no
    space hook of an abstract class has set, and a record that passes
    keeps the class as '__declaring_class__'. Before Python 3.12 the
    refusal reaches the class statement wrapped in a 'RuntimeError'.
    Python does not call this method for a record under a 'classmethod'
    or 'staticmethod' layer, nor for one a dispatcher holds; in a class
    built by 'BaseMeta' those are refused by 'LoadSpaceHook' instead.
    In a plain Python class nothing asks a record under such a layer,
    and it passes unnoticed: 'classmethod' and 'staticmethod' wrap
    anything and pass no '__set_name__' on.

    Parameters
    ----------

    owner : type
      The class being created.

    name : str
      The name the record is bound to.

    Raises
    ------

    TypeError
      No space hook of an abstract class took the record.
    """
    self.requireHost(type(owner), owner.__name__, name)
    self.__declaring_class__ = owner

  def __str__(self, ) -> str:
    return """abstract '%s'""" % self.__name__

  __repr__ = __str__
