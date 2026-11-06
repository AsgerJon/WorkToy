"""
MetaType is the meta-metaclass for the 'worktoy' library.
"""
#  Apache-2.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

#  Python 3.14 added 'annotationlib' with the deferred annotations of PEP
#  649 and PEP 749. Before 3.14 a class body writes its annotations into a
#  dict itself, and nothing needs the package.
try:
  import annotationlib
except ImportError:  # pragma: no cover, no mutate
  annotationlib = None

if TYPE_CHECKING:  # pragma: no cover, no mutate
  from typing import Any, Callable, Optional, Self, TypeAlias
  from . import MetaType as MType

  Bases: TypeAlias = tuple[type, ...]
  Space: TypeAlias = dict[str, Any]


class _DefinedAnnotationsBehaviour(dict):
  """
  PEP 649 and PEP 749 leave the '__annotations__' attribute of a class
  with undefined behaviour. This class gives it a defined behaviour
  regardless, rerouting 'cls.__annotations__' to what Python's
  recommended way of reading annotations gives for the class:
  'annotationlib.get_annotations' from Python 3.14, and
  'inspect.get_annotations' from 3.10.

  The undefined behaviour shows when the metaclass annotates its own
  body: the class may then report the annotations of its metaclass, or of
  a base, instead of its own.

  Implementation
  --------------

  'MetaType.__new__' writes one into the namespace of every class it
  builds, where a read finds it first. It is a dict of the annotations the
  class body declares. On Python 3.14, annotations the body leaves to an
  annotate function are evaluated at the first read, not while the class
  statement runs. A class rebuilt from the dictionary of another receives
  an entry of its own.

  Attributes
  ----------

  __annotate_function__ : Callable or None
    The annotate function of the class body until the first read calls
    it, or 'None' when the body wrote its annotations itself.
  """

  #  Private Variables
  __annotate_function__: Optional[Callable] = None

  @classmethod
  def fromNamespace(cls, space: Space) -> Optional[Self]:
    """
    'MetaType.__new__' needs the entry of the class it is building, made
    from what the class body left in the namespace. A body may also bind
    '__annotations__' itself, to any value, an instance of a subclass of
    dict included; Python accepts that, and such a value must then stay as
    it is. A class rebuilt from the dictionary of another, as
    'dataclass(slots=True)' rebuilds a class, finds the entry of the other
    class there, and must still receive an entry of its own, including an
    evaluation the other class has not made yet.

    Implementation
    --------------

    A plain dict under '__annotations__', as Python writes it, is copied
    into a new entry. An entry of another class is copied as well, its
    annotate function included. With nothing under the name the entry
    starts empty, and on Python 3.14 keeps the annotate function
    'annotationlib.get_annotate_from_class_namespace' finds, if any. Any
    other value under the name, an instance of another subclass of dict
    included, gives 'None'.

    Parameters
    ----------

    space : Space
      A 'dict[str, Any]', or a subclass of dict, holding the class body.

    Returns
    -------

    _DefinedAnnotationsBehaviour or None
      The entry, or 'None' when the body bound the name to something other
      than a plain dict or an entry.
    """
    try:
      written = space['__annotations__']
    except KeyError:
      #  This branch is reached by the following:
      #  - The class body contained no annotations
      #  - On Python 3.14 and later, the class body contained annotations,
      #    and the file does not begin with 'from __future__ import
      #    annotations'
      entry = cls()
      if annotationlib is None:  # pragma: no cover, no mutate
        #  This branch is reached by the following:
        #  - Before Python 3.14, the class body contained no annotations
        return entry
      #  The rest of this branch is reached by the following:
      #  - On Python 3.14 and later, the class body contained no annotations
      #  - On Python 3.14 and later, the class body contained annotations,
      #    and the file does not begin with 'from __future__ import
      #    annotations'
      annotate = annotationlib.get_annotate_from_class_namespace(space)
      entry.__annotate_function__ = annotate
      return entry
    else:
      if type(written) is dict:
        #  This branch is reached by the following:
        #  - Before Python 3.14, the class body contained annotations
        #  - On Python 3.14 and later, the class body contained annotations,
        #    and the file begins with 'from __future__ import annotations'
        #  - The class body bound '__annotations__' itself, to a plain dict
        return cls(written)
      if isinstance(written, cls):
        #  This branch is reached by the following:
        #  - The class is built from the dictionary of a class 'MetaType'
        #    built before, as 'dataclass(slots=True)' rebuilds a class
        entry = cls(written)
        entry.__annotate_function__ = written.__annotate_function__
        return entry
      #  This branch is reached by the following:
      #  - The class body bound '__annotations__' itself, to an instance of a
      #    subclass of dict other than this class
      #  - The class body bound '__annotations__' itself, to a value that is
      #    not a dict
      return None

  def __get__(self, instance: Any, owner: Optional[type] = None) -> Self:
    """
    A read of 'cls.__annotations__' must give the annotations of the class,
    and on Python 3.14 evaluate them no sooner than that read.

    Implementation
    --------------

    A waiting annotate function is called through
    'annotationlib.call_annotate_function' in the 'VALUE' format, its
    result taken into the entry and the function dropped, so it runs once.
    A 'NameError' it raises reaches the reader as it would for a plain
    class, and the next read tries again. The entry itself is returned,
    whether read through the class, through an instance or by the getter
    of 'type'.

    Parameters
    ----------

    instance : Any
      The instance read through, or 'None'.

    owner : type, optional
      The class read through.

    Returns
    -------

    _DefinedAnnotationsBehaviour
      The entry, holding the annotations of its class.
    """
    annotate = self.__annotate_function__
    if annotate is None:
      #  This branch is reached by the following:
      #  - Before Python 3.14
      #  - On Python 3.14 and later, the class body contained no annotations
      #  - On Python 3.14 and later, the class body contained annotations,
      #    and the file begins with 'from __future__ import annotations'
      #  - On Python 3.14 and later, the class body contained annotations,
      #    the file does not begin with 'from __future__ import
      #    annotations', and an earlier read has evaluated them
      return self
    #  The rest of the method is reached by the following:
    #  - On Python 3.14 and later, the class body contained annotations,
    #    the file does not begin with 'from __future__ import annotations',
    #    and no earlier read has evaluated them
    Format = annotationlib.Format
    values = annotationlib.call_annotate_function(annotate, Format.VALUE)
    self.update(values)
    self.__annotate_function__ = None
    return self


class _Chill:
  """
  The worktoy metaclasses read keyword arguments from the class
  statement, so a worktoy class statement must be able to carry them.
  Python allows keyword arguments next to the bases of a class statement:

    class Foo(key=True):  pass

  The keyword 'metaclass' is taken by Python itself. Every other keyword
  is passed to the metaclass, and then to '__init_subclass__', which the
  bases may define to take the keywords meant for them, each passing the
  rest on to the next class along the method resolution order with the
  'super()' call. The last class in that order is always 'object',
  and 'object.__init_subclass__' accepts no keywords at all, so the class
  statement above fails with the dreaded error:

    TypeError: Foo.__init_subclass__() takes no keyword arguments

  Every base whose '__init_subclass__' takes a keyword must still
  receive it, yet no keyword may be left by the time
  'object.__init_subclass__' would be called. This must hold whatever
  bases the class statement lists, with nothing required of the author
  of the class.

  Implementation
  --------------

  'MetaType.__new__' appends '_Chill' to the bases of a class unless the
  last base is already a worktoy class, whose resolution order ends in
  '_Chill' anyway. '_Chill' therefore comes right before 'object' in the
  resolution order of every worktoy class. Its '__init_subclass__'
  accepts any keywords and passes nothing on.

  Attributes
  ----------

  __skip_hash__ : bool
    'True' on '_Chill' alone, and set to 'False' on every class built by
    'MetaType'. 'AbstractMetaclass' hashes a class by the names of its
    bases and leaves out a base marked 'True', since a class the library
    adds to every worktoy class must not change that hash.
  """
  __skip_hash__: bool = True

  @classmethod
  def __init_subclass__(cls, **kwargs) -> None:
    """
    Why are we still here?
    """
    #  '_Chill' is last in the resolution order of every class it is a base
    #  of, so nothing follows it but 'object', whose '__init_subclass__'
    #  takes no keyword, and the chain ends here.


class MetaType(type):
  """
  Every class worktoy builds needs a few things plain 'type' does not
  give, whichever kind of class it is: a sentinel, a control-flow signal,
  a 'BaseObject' class or a metaclass. Its class statement must be able
  to carry keyword arguments for the metaclass to read. Code inspecting a
  finished class must be able to find the namespace object the class body
  ran in, since that object holds what a worktoy metaclass learned from
  the body. Reading the annotations of a class must give that class's
  own, as for a plain class, although the worktoy metaclasses annotate
  their own bodies. And the text of a class should name the metaclass that
  built it, since the metaclass decides how the class behaves.

  The worktoy metaclasses must also combine with each other: a project
  may base one metaclass on two worktoy metaclasses at once, and the
  class creating that combined metaclass must be one both parents agree
  on.

  Implementation
  --------------

  Every worktoy metaclass is both a subclass and an instance of
  'MetaType', as 'type' is of itself, so the metaclasses share one
  creator. '__new__' places '_Chill' last in the resolution order of the
  new class, drops 'object' from the explicit bases, and stores the
  namespace object of the class body on the class under '__namespace__'
  unless the body defines that name, and gives the class an
  '__annotations__' entry of its own, a '_DefinedAnnotationsBehaviour'.
  '__init__' marks the class with
  '__skip_hash__ = False' and hands it on, with every keyword, to the
  next '__init__' along the resolution order of its metaclass, so a
  metaclass of another library combined with a worktoy one does its work
  in either order, as long as it hands on in turn. '__str__' and
  '__repr__' give 'Name[metaclass=MetaName]'.

  Attributes
  ----------

  __namespace__ : dict
    Set on every class 'MetaType' builds: the namespace object its class
    body ran in.

  __annotations__ : dict
    Set on every class 'MetaType' builds: the annotations of that class
    alone; see '_DefinedAnnotationsBehaviour'.

  __skip_hash__ : bool
    'False' on every class 'MetaType' builds; see '_Chill'.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __str__(cls, ) -> str:
    return """%s[metaclass=%s]""" % (cls.__name__, cls.__class__.__name__)

  __repr__ = __str__

  #  The 'mmcls' parameter refers this being a meta-metaclass
  #  noinspection PyMethodParameters
  def __new__(mmcls, name: str, bases: Bases, space: Space, **kw) -> MType:
    """
    A metaclass based on 'MetaType' that reimplements '__new__' still
    needs the class it creates to accept keywords in its class statement
    and to keep the namespace of its body, whatever bases and namespace it
    receives. It therefore passes every keyword on to this method.

    Implementation
    --------------

    '_Chill' is appended to the bases unless the last base is already a
    'MetaType' instance or '_Chill' itself, as when a class is rebuilt
    from its own bases, and 'object' is removed from them. Unless the body
    defines '__namespace__', the namespace object is written into itself
    under that name, so that 'type.__new__' copies the reference into the
    class, and removed again afterwards, so the namespace does not refer to
    itself. A namespace from 'AbstractNamespace.compile' already holds the
    name and is left as it is. The annotations of the body become an entry
    of the class's own, made by '_DefinedAnnotationsBehaviour.fromNamespace'.
    Both entries are written, and '__namespace__' removed, with the methods
    of 'dict', past the '__setitem__' and '__delitem__' of a namespace that
    refuses or records names, as 'ControlSpace' refuses them, so such a
    namespace sees the names of the class body alone.

    Parameters
    ----------

    name : str
      The name of the class.

    bases : Bases
      A 'tuple[type, ...]' of the bases of the class statement.

    space : Space
      A 'dict[str, Any]', or a subclass of dict, holding the class body.

    **kw
      The class keywords, passed on to 'type.__new__'.

    Returns
    -------

    MetaType
      The new class.
    """
    lastBase = (bases or (object,))[-1]
    if not isinstance(lastBase, MetaType) and lastBase is not _Chill:
      bases: tuple[type, ...] = (*bases, _Chill)
    bases: tuple[type, ...] = (*(b for b in bases if b is not object),)
    spaceState: bool = True if '__namespace__' in space else False
    ownAnnotations = _DefinedAnnotationsBehaviour.fromNamespace(space)
    #  'ownAnnotations' is 'None' only for a class whose body provides a
    #  custom value at '__annotations__' itself, anything but a plain dict
    #  or an entry of another class; that value stays as it is.
    if ownAnnotations is not None:
      dict.__setitem__(space, '__annotations__', ownAnnotations)
    if not spaceState:
      dict.__setitem__(space, '__namespace__', space)
    cls = super().__new__(mmcls, name, bases, space, **kw)
    if not spaceState:
      dict.__delitem__(space, '__namespace__')
    return cls

  def __init__(cls, name: str, bases: Bases, space: Space, **kw) -> None:
    """
    A project may combine a worktoy metaclass with a metaclass of another
    library that does its own work in '__init__', such as recording every
    class it builds. Python calls only the first '__init__' along the
    resolution order of the combined metaclass, and each one hands on to
    the next, so a worktoy metaclass listed first must hand on as well,
    with every class keyword, or the work of the other is lost without a
    word. The classes 'MetaType' initializes include metaclasses based on
    'MetaType' itself, and the hand-on must reach the right '__init__' for
    those too.

    Implementation
    --------------

    The class is marked with '__skip_hash__ = False', then handed to the
    next '__init__' after 'MetaType' along the resolution order of the
    metaclass building it, 'type(cls)', with every keyword. The
    two-argument 'super' with 'type(cls)' finds that '__init__' unbound,
    so 'cls' is passed by hand. A zero-argument 'super()' would mean
    'super(MetaType, cls)', which for a 'cls' based on 'MetaType', such as
    'SentinelMeta', searches the resolution order of 'cls' itself, and the
    library would fail as it is imported.

    Parameters
    ----------

    name : str
      The name of the class.

    bases : Bases
      A 'tuple[type, ...]' of the bases of the class statement.

    space : Space
      A 'dict[str, Any]', or a subclass of dict, holding the class body.

    **kw
      The class keywords, passed on to the next '__init__'.
    """
    type.__setattr__(cls, '__skip_hash__', False)
    super(MetaType, type(cls)).__init__(cls, name, bases, space, **kw)
