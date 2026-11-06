"""
The 'tests.test_mcls' package tests 'worktoy.mcls': the namespace hooks,
the abstract namespace and metaclass, 'BaseSpace', 'BaseMeta' and
'BaseObject'. Every test class is based on 'MclsTest', the local base of
the folder, and the fixtures the tests share are small classes of their
own: hooks, namespace classes and metaclasses built from the abstract
ones, worktoy classes defining the class hooks, and the diamond of
overloads.

- MclsTest

Private, importable but not intended for public use:

- LoggingHook
- ClaimingHook
- RefusingHook
- SwappingHook
- LoggedSpace
- ClaimedSpace
- LoggedMeta
- ClaimedMeta
- FlexSpace
- FlexMeta
- SizedMeta
- LoudMeta
- Roster
- Clock
- Ledger
- Factory
- Branded
- Guarded
- Picky
- Primed
- Figure
- Labelled
- Fixed
- Badge
- Tag
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from ._mcls_test import MclsTest
from ._logging_hook import LoggingHook
from ._claiming_hook import ClaimingHook
from ._refusing_hook import RefusingHook
from ._swapping_hook import SwappingHook
from ._logged_space import LoggedSpace
from ._claimed_space import ClaimedSpace
from ._logged_meta import LoggedMeta
from ._claimed_meta import ClaimedMeta
from ._flex_space import FlexSpace
from ._flex_meta import FlexMeta
from ._sized_meta import SizedMeta
from ._loud_meta import LoudMeta
from ._roster import Roster
from ._clock import Clock
from ._ledger import Ledger
from ._factory import Factory
from ._branded import Branded
from ._guarded import Guarded
from ._picky import Picky
from ._primed import Primed
from ._figure import Figure
from ._labelled import Labelled
from ._fixed import Fixed
from ._badge import Badge
from ._tag import Tag

__all__ = [
  'MclsTest',
]
