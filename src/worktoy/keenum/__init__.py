"""
The 'worktoy.keenum' package builds two enumeration systems on the
metaclass and descriptor machinery from 'worktoy.mcls' and
'worktoy.desc'. 'KeeNum' is the value enumeration: 'Kee' members declared
in the class body are collected by a space hook and frozen into typed
members by 'KeeMeta'. 'KeeFlags' is the bitmask-flag enumeration: each
'KeeFlag' is one bit, and 'KeeFlagsMeta' materializes every combination as
a member. 'KeeBox' adapts either system for use as an 'AttriBox' field
type.

KeeNum machinery:

- Kee
- KeeBase
- KeeSpaceHook
- KeeSpace
- KeeMetaMeta
- KeeMeta
- KeeNum

KeeFlags machinery:

- KeeFlag
- KeeFlagsHook
- KeeFlagsSpace
- KeeFlagsMeta
- KeeFlags

Shared:

- KeeBox
- AccessNum
"""
#  Apache-2.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from ._kee_member import Kee
from ._kee_num import KeeBase
from ._kee_flag import KeeFlag
from ._kee_space_hook import KeeSpaceHook
from ._kee_flags_hook import KeeFlagsHook
from ._kee_space import KeeSpace
from ._kee_meta_meta import KeeMetaMeta
from ._kee_meta import KeeMeta, KeeNum
from ._kee_flags_space import KeeFlagsSpace
from ._kee_flags_meta import KeeFlagsMeta
from ._kee_flags import KeeFlags
from ._kee_box import KeeBox
from ._access_num import AccessNum

__all__ = (
  'Kee',
  'KeeBase',
  'KeeFlag',
  'KeeSpaceHook',
  'KeeFlagsHook',
  'KeeSpace',
  'KeeMetaMeta',
  'KeeMeta',
  'KeeNum',
  'KeeFlagsSpace',
  'KeeFlagsMeta',
  'KeeFlags',
  'KeeBox',
  'AccessNum',
)
