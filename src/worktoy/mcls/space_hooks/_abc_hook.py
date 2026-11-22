"""
ABCHook holds a class body to the abstract methods its bases declare.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from ...dispatch import overload, abstract
from . import AbstractSpaceHook

if TYPE_CHECKING:  # pragma: no cover, no mutate
  from typing import Any


class ABCHook(AbstractSpaceHook):
  """
  A class built by 'ABCMeta' may declare methods with '@abstract', which
  the classes based on it have to write. A class body writing such a
  method wrongly, as another kind of method or one that cannot receive
  what is declared, must fail at the line that writes it. And once the
  body has ended, the class must know what it still lacks, since making
  an object of it is refused for as long as anything is left.

  Implementation
  --------------

  'setItemPhase' catches each binding at a name a base declares
  abstract, and has the namespace hold a function written there to the
  declaration. A declaration made with '@abstract' is no implementation
  and passes, and the hook sets '__abc_only__' on its record, which
  says that the record is in the body of an abstract class; a record
  without it is refused as its class is created. The signatures of an
  overloaded name are claimed by 'LoadSpaceHook' before this hook sees
  them, so 'ABCSpace' holds each of those to its declaration as it is
  registered, and sets the flag on an abstract one there. 'postCompilePhase'
  has the namespace settle what is left, and writes it into the class
  dictionary under '__missing_implementations__', which 'ABCMeta' reads
  at every call. 'newClassPhase' tells each record of the body the class
  that declared it.
  """

  def setItemPhase(self, key: str, val: Any, old: Any = None, ) -> bool:
    """
    A method written at a name a base declares abstract must be held to
    that declaration at its line.

    Parameters
    ----------

    key : str
      The name bound.

    val : Any
      The value bound.

    old : Any, optional
      The value the name held, or 'None'.

    Returns
    -------

    bool
      'False', so the namespace stores the binding.

    Raises
    ------

    WrongImplementation
      The value cannot stand for what a base declares at the name.
    """
    kinds, inner = overload.peelMethodKinds(val)
    if isinstance(inner, abstract):
      #  This branch is reached by the following:
      #  - The body declares the name abstract itself, anew or for the
      #    first time, which implements nothing
      inner.__abc_only__ = True
      return False
    self.space.screenPlain(key, kinds, inner)
    return False

  def postCompilePhase(self, compiledSpace: dict) -> dict:
    """
    Once the body has ended, what the class still lacks must be on the
    class, where 'ABCMeta' finds it when the class is called.

    Parameters
    ----------

    compiledSpace : dict
      The dictionary being assembled.

    Returns
    -------

    dict
      The dictionary, holding what is not implemented.

    Raises
    ------

    WrongImplementation
      The body overloads a name a base declares plainly, and none of the
      overloads can take what is declared.
    """
    missing = self.space.settleAbstract()
    compiledSpace['__missing_implementations__'] = missing
    return compiledSpace

  def newClassPhase(self, cls: type) -> type:
    """
    A record should know the class whose body declared it, which exists
    only now. Python tells a record bound plainly, through its
    '__set_name__', but not one under '@classmethod' or
    '@staticmethod', nor one a dispatcher holds through '@overload'.

    Implementation
    --------------

    The class is written at '__declaring_class__' on every record the
    body declared, as 'ABCSpace.getDeclaredAbstract' lists them.

    Parameters
    ----------

    cls : type
      The new class.

    Returns
    -------

    type
      The class.
    """
    for requirement in self.space.getDeclaredAbstract():
      requirement[3].__declaring_class__ = cls
    return cls
