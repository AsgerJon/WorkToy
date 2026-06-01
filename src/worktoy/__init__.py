"""The 'worktoy' package adds runtime type enforcement, declarative
attributes, function overloading, and custom-metaclass infrastructure on
top of stock Python. It targets Python 3.7 through 3.14.

The package is layered: each package depends only on the packages listed
before it, and the import order below is the canonical dependency order.
Code added to a package should import only from earlier packages in this
chain.

- utilities: Leaf-level helpers with no other 'worktoy' dependencies,
  such as 'maybe', 'textFmt', 'unpack', 'typeCast', and the
  'combinatorics' subpackage.
- waitaminute: Every custom exception in the library, grouped into
  subpackages by the layer that raises it. The philosophy is fail-fast:
  a silent fallback is treated as a bug.
- core: The most primitive runtime types, including 'Object' (the
  contextual descriptor base), 'MetaType', and the 'sentinels' such as
  'THIS', 'OWNER', and 'DESC'.
- dispatch: The '@overload' decorator and its supporting machinery
  ('Dispatcher', 'TypeSig', 'Permuter', 'flexCall') providing
  type-signature based function overloading.
- desc: The descriptor protocol layer, providing 'BaseDescriptor',
  'Field', 'AttriBox', 'FixBox', 'FastBox', 'Alias', and
  'SymbolicName'.
- mcls: The metaclass framework, providing 'AbstractMetaclass',
  'BaseMeta', and 'BaseObject', the common base class that enables
  overloading and 'AttriBox' support.
- lorem_ipsum: Stochastic placeholder-text generation ('Paragraph',
  'Sentence', 'Clause', 'StochasticWord').
- keenum: The enumeration framework, providing 'KeeNum', the 'Kee'
  member descriptor, and the bitmask-flag 'KeeFlags'.
- ezdata: The 'EZData' dataclass, built on its own metaclass and field
  descriptors.
- work_test: Testing support, providing 'BaseTest' and the random-data
  samplers used across the test suite.
"""
#  Apache-2.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

__version__ = '1.0.0-rc9'

from . import utilities
from . import waitaminute
from . import core
from . import dispatch
from . import desc
from . import mcls
from . import lorem_ipsum
from . import keenum
from . import ezdata
from . import work_test

__all__ = [
  'utilities',
  'waitaminute',
  'core',
  'dispatch',
  'desc',
  'mcls',
  'lorem_ipsum',
  'keenum',
  'ezdata',
  'work_test',
]
