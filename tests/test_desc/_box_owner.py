"""
BoxOwner uses AttriBox descriptors containing BoxedObject and BoxedFloat
instances to test the forwarding of the information retrieved during the
'__set_name__' on the AttriBox instance. This forwarding means that the
field objects created by AttriBox instances, are aware of their field name
and field owner.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.desc import AttriBox
from . import BoxedFloat, BoxedObject


class BoxOwner:
  """
  BoxOwner uses AttriBox descriptors containing BoxedObject and BoxedFloat
  instances to test the forwarding of the information retrieved during the
  '__set_name__' on the AttriBox instance. This forwarding means that the
  field objects created by AttriBox instances, are aware of their field name
  and field owner.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Public Variables
  name = AttriBox[BoxedObject]()
  value = AttriBox[BoxedFloat](69.0)
