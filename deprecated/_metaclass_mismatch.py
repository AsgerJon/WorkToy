"""MetaclassMismatch is raised to indicate that a baseclass is not derived
from the expected metaclass. The 'object' class is exempt from this. """
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from worktoy.text import monoSpace


class MetaclassMismatch(Exception):
  """MetaclassMismatch is raised to indicate that a baseclass is not derived
  from the expected metaclass. The 'object' class is exempt from this. """

  __base_class__ = None
  __expected_meta__ = None

  def __init__(self, base: type, mcls: type) -> None:
    """Initialize the MetaclassMismatch exception."""
    self.__base_class__ = base
    self.__expected_meta__ = mcls
    info = """Baseclass '%s' is not derived from the expected metaclass 
    '%s'!"""
    baseName = base.__name__
    mclsName = mcls.__name__
    Exception.__init__(self, monoSpace(info % (baseName, mclsName)))
