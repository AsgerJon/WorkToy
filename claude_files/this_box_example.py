"""
ThisBoxExample exemplifies the use of AttriBox and how it leverages both
the 'THIS' and 'OWNER' sentinels.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

import sys
import os
from typing import TYPE_CHECKING

here = os.path.dirname(os.path.abspath(__file__))
src = os.path.normpath(os.path.join(here, '..', 'src'))
sys.path.append(src)

from worktoy.desc import AttriBox
from worktoy.core.sentinels import THIS, OWNER
from worktoy.mcls import BaseObject
from worktoy.utilities import textFmt

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any


class Value(BaseObject):
  """
  Value provides a very simple class collecting the arguments passed to
  the constructor.
  """


class ThisBoxExample(BaseObject):
  """
  ThisBoxExample exemplifies the use of AttriBox and how it leverages both
  the 'THIS' and 'OWNER' sentinels.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Public Variables
  thisBox = AttriBox[Value](THIS)
  ownerBox = AttriBox[Value](OWNER)


def main(*args, ) -> int:
  """
  Main tester script for ThisBoxExample.
  """

  example = ThisBoxExample()
  thisBoxArgs = example.thisBox.getPosArgs()
  ownerBoxArgs = example.ownerBox.getPosArgs()
  for arg in thisBoxArgs:
    if arg is example:  # success!
      break
  else:
    print("""ERROR!""")
    return 1
  for arg in ownerBoxArgs:
    if arg is ThisBoxExample:  # success!
      break
  else:
    print("""ERROR!""")
    return 1
  infoSpec = """The 'THIS' sentinel provides a placeholder for the 
  'instance' passed to the '__get__' method and 'OWNER' provides a 
  placeholder for the 'owner' passed to '__get__'."""
  print(textFmt(infoSpec))
  return 0


if __name__ == '__main__':
  sys.exit(main())
