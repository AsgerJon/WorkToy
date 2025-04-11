"""AbstractFilter encapsulates object filtering logic for use by the custom
namespace system in the 'worktoy.mcls' module. The namespace classes
provides hooks in the __setitem__ method the triggers each filter assigned
to the namespace class. Each filter is called with the namespace instance,
key and value passed to the __setitem__ method. The filter should raise
FilterException to indicate that it does provide special handling of the
given key and value. In this case, the call falls back to the default
__setitem__ method. If the filter does not raise FilterException,
it is assumed that the filter has handled the key and value and the call
is not passed to the default __setitem__ method."""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations


class AbstractFilter:
  """AbstractFilter encapsulates object filtering logic for use by the custom
  namespace system in the 'worktoy.mcls' module. The namespace classes
  provides hooks in the __setitem__ method the triggers each filter assigned
  to the namespace class. Each filter is called with the namespace instance,
  key and value passed to the __setitem__ method. The filter should raise
  FilterException to indicate that it does provide special handling of the
  given key and value. In this case, the call falls back to the default
  __setitem__ method. If the filter does not raise FilterException,
  it is assumed that the filter has handled the key and value and the call
  is not passed to the default __setitem__ method."""
