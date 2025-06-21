"""
MetaclassException provides a vastly improved exception to replace the
default 'all your base are belong to us' exception raised by metaclass
incompatibility.

For example, let MetaFoo and MetaBar both be metaclasses based on type.
Let Bar be derived from MetaBar. Then when trying to derive Foo from
MetaFoo whilst also based on Bar, we have the incompatibility:

class MetaFoo(type): pass

class MetaBar(type): pass

class Bar(metaclass=MetaBar): pass

class Foo(Bar, metaclass=MetaFoo): pass  # raises

When trying to create the class Foo, we get this bit of syntactic broccoli:
'TypeError: metaclass conflict: the metaclass of a derived class must be a
(non-strict) subclass of the metaclasses of all its bases'

What this is trying to communicate is that baseclasses must be derived
from the same metaclass or subclass as the new class. MetaclassException
will instead provide a much clearer message that also references
specifically which base class and metaclass is causing the issue.

Metaclass conflict while defining class 'Foo':

- Foo derives from metaclass 'MetaFoo'
- While also based on class 'Bar' derived from 'MetaBar'
- But 'MetaBar' is not 'MetaFoo' nor a subclass of 'MetaFoo'.

Classes must be based on baseclasses derived from the same metaclass or
subclass of it.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from . import _Attribute
from ..text import joinWords, monoSpace

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
  from typing import Self


class MetaclassException(TypeError):
  """
  Vastly improved exception for metaclass incompatibility.
  """

  name = _Attribute()
  meta = _Attribute()
  badBase = _Attribute()
  badMeta = _Attribute()

  def __init__(self, mcls: type, name: str, base: type) -> None:
    """Initialize the MetaclassException object."""
    self.name = name
    self.meta = mcls
    self.badBase = base
    self.badMeta = type(base)

    infoSpec = """Metaclass conflict while deriving class: '%s' from 
    metaclass: '%s', because the base class: '%s' is derived from the 
    different metaclass: '%s' which is not a subclass of '%s'."""
    names = [
        name,
        mcls.__name__,
        base.__name__,
        self.badMeta.__name__,
        mcls.__name__
    ]
    info = infoSpec % (*names,)
    TypeError.__init__(self, info)
