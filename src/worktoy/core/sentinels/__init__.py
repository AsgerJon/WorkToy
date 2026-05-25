"""
Sentinels represent special situations. The sentinel itself provides no
information about its meaning or function. It is merely a stateless unique
object equal only to itself.

Contents:

  - Sentinel: Base class for all sentinels. It derives from a custom
  metaclass providing functionality preventing instantiation and
  duplication.
  - DELETED: Sentinel used to indicate that an element has been deleted.
  Used by custom descriptors to implement deletion semantics: to 'delete'
  a custom descriptor from an instance, the descriptor 'sets' the value
  for the instance to 'DELETED'. The same descriptor then raises the
  appropriate 'AttributeError' when '__get__' would return 'DELETED'.
  - THIS: Placeholder for the enclosing class, used from within a class
  body. In a deferred 'AttriBox' argument it is replaced by the
  'instance' passed to '__get__'; in an '@overload' signature it stands
  for the class itself, matching instances of it (like 'typing.Self').
  - OWNER: Placeholder for the 'owner' class passed to '__get__'. Used
  in deferred 'AttriBox' arguments. Unlike THIS, it has no role in
  overload signatures.
  - DESC: Used by 'AttriBox' along with THIS and OWNER, specifying the
  present descriptor.
  - METACALL: Marker used on a class to defer a given dunder hook to the
  metaclass implementation.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from ._sentinel import Sentinel, _Sentinel
from ._deleted import DELETED
from ._owner import OWNER
from ._this import THIS
from ._desc import DESC
from ._meta_call import METACALL
from ._args import ARGS

__all__ = [
  'Sentinel',
  'DELETED',
  'OWNER',
  'THIS',
  'DESC',
  'METACALL',
  'ARGS',
]
