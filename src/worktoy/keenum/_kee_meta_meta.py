"""
KeeMetaMeta provides the meta-metaclass for the 'worktoy.keenum' package.
"""
#  Apache-2.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING, cast

from ..core import MetaType
from ..desc import Field
from . import KeeSpace as KSpace
from . import KeeBase

if TYPE_CHECKING:  # pragma: no cover
  from typing import Optional
  from . import KeeMeta
else:
  KeeMeta = object


class KeeMetaMeta(MetaType):
  """
  KeeMetaMeta hosts the 'keeNum' descriptor: the answer to the
  question "what root class should an enumeration of this metaclass
  inherit from?" 'KeeMeta' is the only metaclass the library ships,
  and 'worktoy.keenum.KeeNum' is exactly 'KeeMeta.keeNum', cached.
  The descriptor sits on the meta-metaclass rather than on
  'KeeMeta' itself so that any subclass of 'KeeMeta' gets its own
  distinct root class, built through its own machinery rather than
  through the vanilla 'KeeMeta'.

  Recommended path: declaring an enumeration
  ------------------------------------------
  Subclass 'KeeNum' and place 'Kee' members in the class body.
  This is what every example in the documentation does, and it
  does not require knowing that 'keeNum' or 'KeeMetaMeta' exist
  at all.

    from worktoy.keenum import KeeNum, Kee

    class WeekDay(KeeNum):
      MONDAY = Kee[str]('Mandag')
      ... etc.

  'KeeNum' is the cached value of 'KeeMeta.keeNum'; no other
  ceremony is required.

  Advanced path: customising 'KeeMeta'
  ------------------------------------
  A user who writes a subclass of 'KeeMeta' to extend the
  metaclass-level behavior cannot inherit from 'KeeNum' for their
  enumerations. 'KeeNum' was constructed through 'KeeMeta', not
  through the subclass, so any customization the subclass adds at
  '__new__' / '__init__' / '__call__' / etc. would not reach an
  enumeration whose root is 'KeeNum'. The subclass must instead
  use its own root class, which the 'keeNum' descriptor builds on
  demand:

    from worktoy.keenum import KeeMeta, Kee

    class FontMeta(KeeMeta):
      pass  # whatever customization you add lives here

    class FontFamilyNum(FontMeta.keeNum):
      ARIAL = Kee[int](1)
      TIMES_NEW_ROMAN = Kee[int](2)
      CALIBRI = Kee[int](3)
      ... etc.

  'FontMeta.keeNum' triggers '_getKeeNum' on 'FontMeta', which
  calls 'FontMeta.__new__(FontMeta, ...)' to build a fresh root
  class through 'FontMeta' (carrying every customization
  'FontMeta' introduced) and caches the result. 'FontFamilyNum'
  then inherits that root and benefits from the customizations.

  Forgetting this and writing 'class FontFamilyNum(KeeNum):'
  instead silently bypasses 'FontMeta' entirely: the enumeration
  is constructed by plain 'KeeMeta', and the customizations are
  simply absent at runtime. There is no error message because no
  rule is violated, which is precisely why this distinction needs
  to be written down rather than discovered.

  Lifecycle
  ---------
  'keeNum' is a 'Field' descriptor with a single getter that
  builds the root class on first access and caches it on the
  metaclass at '__kee_num__'. Subsequent accesses return the
  cache. The 'KeeMeta.__init_subclass__' implementation resets
  '__kee_num__' to None on each subclass, so the construction
  fires exactly once per metaclass over the program's lifetime.
  """

  __kee_num__: Optional[KeeMeta] = None
  keeNum: Field[KeeMeta] = Field()

  @keeNum.GET
  def _getKeeNum(mcls, **kwargs) -> KeeMeta:  # noqa N805
    if mcls.__kee_num__ is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      num = """%sNum""" % (mcls.__name__,)
      name = 'KeeNum' if mcls.__name__ == 'KeeMeta' else num
      numSpace = KSpace(mcls, name, (KeeBase,), _root=True)
      numSpace['__root_class__'] = True
      numSpace['__doc__'] = KeeBase.__doc__
      # noinspection PyTypeChecker
      num = mcls.__new__(mcls, name, (KeeBase,), numSpace, _root=True)
      mcls.__kee_num__ = cast(KeeMeta, num)
      return mcls._getKeeNum(_recursion=True, )
    return mcls.__kee_num__
