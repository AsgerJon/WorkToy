"""The 'worktoy' package provides a collection of utilities leveraging
advanced python features including custom metaclasses and the descriptor
protocol. The readme file included provides detailed documentation on the
included features. The modules provided depend on each other in
implementation, but can be used independently.

The package consists of thr following modules:
- 'text': For working with text.
- 'waitaminute': Provides custom exception classes.
- 'static': For parsing of objects.
- 'meta': Provides custom metaclasses.
- 'desc': Provides custom descriptors.
- 'ezdata': Provides the 'EZData' class for creating data classes.
- 'keenum': Provides the 'KeeNum' class for creating enums.

All features are implemented in one of the above modules, but the
essential features are present directly in the package namespace. These
are listed below:

- 'maybe': Returns the first value that is not 'None'.
- 'typeCast': Casts the value to the specified type.
- 'overload': Decorator for overloading methods.
- 'BaseObject': Base class for custom objects.
- 'AttriBox': Descriptor with automatic accessor functions.
- 'Field': Descriptor requiring custom accessor functions.
- 'EZData': Base class for data classes.
- 'KeeNum': Base class for enumerations."""
#  AGPL-3.0 license
#  Copyright (c) 2024-2025 Asger Jon Vistisen
from __future__ import annotations

from . import text
from . import waitaminute
from . import static
from . import ezdata
from . import keenum
# from worktoy.static import maybe, typeCast, overload
# from worktoy.meta import BaseObject
# from worktoy.desc import AttriBox, Field, THIS
# from worktoy.ezdata import EZData
# from worktoy.keenum import KeeNum

# __all__ = [
#     'text', 'waitaminute', 'static', 'meta', 'desc', 'ezdata',
#     'keenum', 'maybe', 'typeCast', 'overload', 'BaseObject',
#     'AttriBox', 'Field', 'THIS', 'EZData', 'KeeNum']
