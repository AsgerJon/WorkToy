"""
KeeSpaceHook collects the 'Kee' descriptors from a 'KeeNum' class body.
"""
#  Apache-2.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from types import FunctionType
from typing import TYPE_CHECKING

from ..mcls.space_hooks import AbstractSpaceHook
from ..waitaminute.keenum import KeeMemberNameError, KeeCaseException
from ..waitaminute.keenum import KeeDuplicate
from ..waitaminute.meta import UnboundClassHook, ReservedName
from . import Kee

if TYPE_CHECKING:  # pragma: no cover, no mutate
  from typing import Any

  from . import KeeSpace


class KeeSpaceHook(AbstractSpaceHook):
  """
  An enumeration body binds its members as ordinary names, 'RED =
  Kee[int](1)', yet the class must hold members at those names and
  nothing else: a plain value bound at a member's name, before or after
  the member, would be replaced without a word. The 'Kee' objects must
  therefore reach the namespace's record and never its dictionary, and
  a body binding a member's name twice must fail at that line. The
  members are constants, and their names are upper case, which keeps
  them apart from every other name of the class; a name in another case
  must fail at its line as well, unless the class says on its class
  statement that it wants such names, as a class of unit symbols does,
  or is based on a class that said so.
  Whatever their case, two members must not share a name once case is
  ignored, as 'MW' beside 'mW': a lookup by name ignores case and could
  not tell them apart, so the second must fail at its line. And a class
  that gives up the upper-case rule gives up what kept its members apart
  from the other names of the class, as 'members', 'space' and the
  methods of its bases, so a member at such a name must fail at its line
  too, since it would replace that name on the class without a word.

  Implementation
  --------------

  'setItemPhase' hands every 'Kee' to 'addNum' of the namespace and
  claims the binding. A 'Kee' bound at a name the dictionary holds, or
  a plain value bound at a name a member takes, declared or inherited,
  raises 'KeeMemberNameError'. A 'Kee' bound at a name that is not
  upper case raises 'KeeCaseException', unless the class keyword
  'strictCase=False' holds for the class: '_isStrictCase' reads it off
  the namespace, and for a class statement without it off the nearest
  class along the resolution order that gave it. 'preparePhase' reads
  the keyword once as the namespace is created, so a value that is no
  'bool' raises 'TypeException' before the body runs, whatever the body
  declares. A 'Kee' bound at a name that 'getNumsIgnoringCase' of the
  namespace finds on record, for a member declared or inherited, in the
  same case or another, raises 'KeeDuplicate'. Where the upper-case rule
  does not hold, a 'Kee' bound at a name that '_isTakenName' finds on a
  base or on the metaclass raises 'ReservedName'. A '__class_resolve__'
  bound to a plain function or a staticmethod raises 'UnboundClassHook',
  as a routed class hook does, since the lookups call the hook bound to
  the class. One hook object serves every body, so it keeps nothing of
  its own.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def _isStrictCase(self) -> bool:
    """
    The names of the members of an enumeration are upper case, and a
    class that needs names in another case must say so, on its class
    statement, with a value that cannot be misread. A subclass of such a
    class adds members of the same kind and must not have to say it
    again, while a subclass that wants the rule back must be able to
    take it.

    Implementation
    --------------

    The class keyword 'strictCase' is read off the namespace with
    'parseKwargs', which admits a 'bool' alone. A class statement that
    does not give it takes the choice of the nearest class along its
    resolution order whose class statement did, as an attribute is found
    along that order; the keywords of each are read off the
    '__keyword_arguments__' that a worktoy namespace writes into its
    class. With no such class the names are held to upper case.

    Returns
    -------

    bool
      Whether the member names of the class body must be upper case.

    Raises
    ------

    TypeException
      'strictCase' is given and is no 'bool'.
    """
    kwargs = self.space.getKwargs()
    strictCase, _ = self.parseKwargs('strictCase', bool, **kwargs)
    if strictCase is not None:
      #  This branch is reached by the following:
      #  - The class statement gives the 'strictCase' keyword itself
      return strictCase
    for base in self.space._getLookupOrder():
      try:
        given = base.__dict__['__keyword_arguments__']
      except KeyError:
        #  This branch is reached by the following:
        #  - The base was built by no worktoy namespace, as 'KeeBase', a
        #    plain mixin and 'object' are
        continue
      inherited, _ = self.parseKwargs('strictCase', bool, **given)
      if inherited is not None:
        #  This branch is reached by the following:
        #  - A class along the resolution order gave the keyword
        return inherited
    #  The rest of the method is reached by the following:
    #  - Neither the class statement nor a class it is based on gives the
    #    keyword
    return True

  def _isTakenName(self, name: str) -> bool:
    """
    The upper-case rule keeps the name of a member apart from every other
    name of its class, none of which is upper case in the library: the
    accessors of the enumeration, as 'members' and 'space', the methods
    of its members, and whatever a base or the metaclass defines. Without
    the rule a member could take such a name, and would then replace the
    accessor or the method on the class without a word, or fail on a
    property of the metaclass with an error that names neither the member
    nor a rule.

    Implementation
    --------------

    A name is taken when a class dictionary holds it, along the
    resolution order of the bases or along that of the metaclass. The
    dictionaries are read as they are, so no property is asked for its
    value.

    Parameters
    ----------

    name : str
      The name a member is being bound at.

    Returns
    -------

    bool
      Whether a base or the metaclass holds the name already.
    """
    metaclass = self.space.getMetaclass()
    for cls in (*self.space._getLookupOrder(), *metaclass.__mro__):
      if name in cls.__dict__:
        return True
    return False

  def preparePhase(self, space: KeeSpace) -> None:
    """
    A class statement giving 'strictCase' a value that is no 'bool' is
    mistaken whether or not its body declares a member, and the mistake
    must fail before the body runs, not at the line of the first member,
    and not pass unnoticed in a body declaring none.

    Implementation
    --------------

    The namespace binds the hook to itself before it runs this phase, so
    '_isStrictCase' reads the keyword of the namespace being created, and
    its refusal leaves the class statement from '__prepare__'. The answer
    itself is not needed here.

    Parameters
    ----------

    space : KeeSpace
      The new namespace.

    Raises
    ------

    TypeException
      'strictCase' is given and is no 'bool'.
    """
    self._isStrictCase()

  def setItemPhase(self, key: str, val: Any, old: Any = None, ) -> bool:
    if key == '__class_resolve__':
      if isinstance(val, (FunctionType, staticmethod)):
        raise UnboundClassHook(self.space.getClassName(), key)
    if isinstance(val, Kee):
      clsName = self.space.getClassName()
      if dict.__contains__(self.space, key):
        raise KeeMemberNameError(clsName, key)
      strictCase = self._isStrictCase()
      if strictCase and not key.isupper():
        raise KeeCaseException(key)
      for held in self.space.getNumsIgnoringCase(key):
        #  This loop is entered by the following:
        #  - A member, declared or inherited, has the name already
        #  - A member has a name that differs from it by case alone
        raise KeeDuplicate(clsName, key, held, val)
      if not strictCase and self._isTakenName(key):
        #  This branch is reached by the following:
        #  - The class gave up the upper-case rule, and a base or the
        #    metaclass holds the name, as 'space', 'members' or a method
        raise ReservedName(key)
      self.space.addNum(key, val)
      return True
    if self.space.hasNum(key):
      raise KeeMemberNameError(self.space.getClassName(), key)
    return False
