"""
The 'tests.test_core' package tests 'worktoy.core': 'MetaType' and its
helpers, 'Object' and its two context descriptors, the sentinels and the
control-flow signals. Every test class is based on 'CoreTest', the local
base of the folder, and the fixtures the tests share are small classes
of their own.

- CoreTest

Private, importable but not intended for public use:

- Counted
- Noisy
- Quiet
- Skipper
- SelfReader
- EarlyReader
- PartnerReader
- Liar
- RecordingMeta
- NoReference
- Grand
- Parent
- Hooked
- Boxed
- Item
- Holder
- Nudge
- FamilyMeta
- Agreeable
- SlowInstance
- SlowHook

'_this_sugar_helpers.py' holds the class statements written with the
decorator spelling '@THIS[Parent].x.onGet', syntax from Python 3.9 on;
the package never imports it, the two test modules of 'THIS' do, behind
a version guard, and skip the tests calling into it below 3.9.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from ._core_test import CoreTest
from ._counted import Counted
from ._noisy import Noisy
from ._quiet import Quiet
from ._skipper import Skipper
from ._self_reader import SelfReader
from ._early_reader import EarlyReader
from ._partner_reader import PartnerReader
from ._liar import Liar
from ._recording_meta import RecordingMeta
from ._no_reference import NoReference
from ._grand import Grand
from ._parent import Parent
from ._hooked import Hooked
from ._boxed import Boxed
from ._item import Item
from ._holder import Holder
from ._nudge import Nudge
from ._family_meta import FamilyMeta
from ._agreeable import Agreeable
from ._slow_instance import SlowInstance
from ._slow_hook import SlowHook

__all__ = [
  'CoreTest',
]
