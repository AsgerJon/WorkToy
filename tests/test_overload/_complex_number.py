"""
The ComplexNumber provides an overloaded implementation of the complex
number. The 'test_overload' module bases unit tests on this class and
subclasses of it. The complex number is a convenient subject for testing
overloading functionality due to its multiple representations.

Please note that this class relies on the 'worktoy.attr.Field' class for
descriptors, but does not provide testing for it. The 'test_attr' module
provides unit testing for 'Field' without relying on overloading. This
reflects the dependency chain of the 'worktoy' library:

Orphant modules:
- 'parse': For low-level parsing.
- 'text': For working with text.
- 'waitaminute': Provides custom exception classes.

The following modules depend on previously listed modules:
- 'static' - 'AbstractObject' and the dispatch system
- 'attr' - Although the 'AbstractObject' class does implement the entirety
of the descriptor protocol, this module provides the practical
implementations. 
- 'mcls' -

"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from worktoy.mcls import BaseObject

try:
  from typing import TYPE_CHECKING
except ImportError:
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
  from typing import Any, Optional, Self, TypeAlias


class ComplexNumber(BaseObject):
  """
  The ComplexNumber provides an overloaded implementation of the complex
  number. The 'test_overload' module bases unit tests on this class and
  subclasses of it. The complex number is a convenient subject for testing
  overloading functionality due to its multiple representations.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Fallback variables

  #  Private variables

  #  Public variables

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  PYTHON API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
