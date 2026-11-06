"""
The 'tests.test_dispatch' package tests 'worktoy.dispatch': the call
helpers 'flexCall' and 'CallMeMaybe', the permuters, 'TypeSig', the
'overload' record and the 'Dispatcher'. Every test class is based on
'DispatchTest', the local base of the folder, and the fixtures the
tests share are small classes of their own.

- DispatchTest

Private, importable but not intended for public use:

- UnhashableMeta
- UncheckableMeta
- Uncheckable
- Label
- Tally
- Counter
- Shape
- Square
- Fallbacked
- Wide
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from ._dispatch_test import DispatchTest
from ._unhashable_meta import UnhashableMeta
from ._uncheckable_meta import UncheckableMeta
from ._uncheckable import Uncheckable
from ._label import Label
from ._tally import Tally
from ._counter import Counter
from ._shape import Shape
from ._square import Square
from ._fallbacked import Fallbacked
from ._wide import Wide

__all__ = [
  'DispatchTest',
]
