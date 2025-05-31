"""
The 'worktoy.static.zeroton' module provides the 'Zeroton' tokens.

Readers may be familiar with the term 'singleton' as a class restricted to
a single instance. This facilitates the design pattern where the class
provides stateless functionality whilst the instance holds an internal
state.

- Introducing the 'Zeroton'! -

It is just a 'singleton' as described above, but with zero instances,
hence the name. As such, the 'Zeroton' objects found here are entirely
stateless. 'Zeroton' itself is a metaclass facilitating the creation of
these zeroton objects.

- Motivation -
If Python did not already provide the 'super' function, it would have been
a prime candidate for implementation as a zeroton as it refers to an
object that cannot be resolved until runtime. The uses in this module are
similar except used to refer to objects that do not yet exist. As an
example, the 'typing.Self' object refers the current class scope, but with
the limitation that it is not really there. Instead, it is an abstraction
used in the type-hinting system. While this author holds those objects in
very high regard, as is evident across the codebase, 'worktoy' requires
an actual reference to the current scope.

- Introducing 'THIS' -
(Please note, that the 'THIS' object has no connection to the 'this'
module one can import to read about the 'this' statement in Python. The
nomenclature was committed to before this author ever learned about
'this'. The zeroton object is distinguished by being all uppercase.)

Python lacks function overloading as a language feature, but does provide
the most powerful abstraction in computer science: the metaclass. By
exposing nearly the entire class creation process, function overloading
and other advanced features are now only a metaclass away.
'worktoy.mcls.BaseMeta' is such a metaclass.

In the following example, 'ComplexNumber' derives from 'BaseMeta' and uses
function overloading to provide a very streamlined constructor system
supporting multiple type signatures. But what about a type signature
referring to 'ComplexNumber' itself? Since the overload decorator must be
present inside the class body. Resolving the super class is no trivial
matter, but it does exist, but in this case, a reference to an object not
yet existing is required. 'THIS' is that object. For example:


class ComplexNumber(metaclass=worktoy.mcls.BaseMeta):
  #  ComplexNumber defines its metaclass on the metaclass keyword. By
  #  default, this value is 'type', and unless a class uses a custom
  #  metaclass, 'type(SomeClass)' is always 'type'. Leading to the
  #  amusing fact: 'type(type) is type'.
  #  Please note the nomenclature: When a class uses a custom metaclass,
  #  it is said to 'be derived from' from that metaclass. To distinguish
  #  from 'normal' class inheritance, this author proposes that a subclass
  #  be said to 'be based on' the base class. The relationship between a
  #  subclass and a baseclass is entirely different from between a class
  #  and its metaclass.

  __slots__ = ('realPart', 'imagPart')

  @overload(float, float)  # Decorates the float-float constructor
  def __init__(self, x: float, y: float) -> None:
    self.realPart = x
    self.imagPart = y

  @overload(complex)  # Decorates the complex constructor
  def __init__(self, z: complex) -> None:
    self.__init__(z.real, z.imag)  # Recursively calls the float-float

  #  And now the type signature referring to the class under construction:
  @overload(THIS)  # Decorates the 'ComplexNumber' constructor
  def __init__(self, other: Self) -> None:
    #  Note the type-hinting to 'typing.Self'. 'THIS' implements the same
    #  but at runtime. As such, when instantiating 'ComplexNumber' by
    #  passing another instance of it, the function overloading system
    #  uses 'THIS' as a temporary token for the class that will be
    #  available later.
    self.__init__(other.realPart, other.imagPart)
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

#  Private list of disallowed names
from ._reserved_names import _reservedNames

#  The Zeroton namespace
from ._zero_space import ZeroSpace

#  The Zeroton metaclass
from ._zeroton import Zeroton

#  The objects derived from Zeroton
from ._deleted import DELETED
from ._this import THIS
from ._owner import OWNER
from ._desc import DESC

__all__ = [
    'Zeroton',
    'THIS',
    'OWNER',
    'DELETED',
    'DESC',
]
