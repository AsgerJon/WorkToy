"""The 'worktoy.mcls' module provides the base custom metaclass and
namespace uses across the 'worktoy' library. The pattern used is for the
namespace class to implement a method called 'compile' which decides the
actual namespace to be used in the class creation based on the code found
during execution of the class body.

The metaclass instantiates the namespace class and returns the created
namespace object from the '__prepare__' method. Upon completion of the
class body execution this namespace object is passed back to the metaclass
in the '__new__' method. The namespace object is required to implement a
method called 'compile' which returns an instance of 'dict'. Next the
metaclass validates the 'dict' object and finally passes it to the
'__new__' method on type. Before returning the created class,
the metaclass checks each baseclass for the presence of a method called
'__subclasshook__'. If it exists, the method is called with the created
class object allowing the baseclass to modify or even reject the class.
Finally, the metaclass returns the created class object."""
#  AGPL-3.0 license
#  Copyright (c) 2024-2025 Asger Jon Vistisen
from __future__ import annotations

from ._type_names import Bases, Space
from ._abstract_namespace import AbstractNamespace
from ._abstract_metaclass import AbstractMetaclass

try:
  from typing import TYPE_CHECKING
except ImportError:
  TYPE_CHECKING = False

if TYPE_CHECKING:
  try:
    from typing import Callable as CallMeMaybe
  except ImportError:
    CallMeMaybe = object
else:
  from ._call_me_maybe import CallMeMaybe
