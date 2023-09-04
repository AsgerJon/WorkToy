"""WorkToy - SYM - FontFamily
Symbolic class representing text families for use by QFont."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from icecream import ic

from worktoy.fields import IntField
from worktoy.sym import BaseSym, SYM

ic.configureOutput(includeContext=True)


class FontFamilySym(BaseSym, ):
  """WorkToy - SYM - FontFamily
  Symbolic class representing text families for use by QFont."""

  value = IntField(0)

  Arial = SYM.auto()
  Arial.value = 0
  Times_New_Roman = SYM.auto()
  Times_New_Roman.value = 1
  Courier_New = SYM.auto()
  Courier_New.value = 2
  Verdana = SYM.auto()
  Verdana.value = 3
  Cambria = SYM.auto()
  Cambria.value = 4
  Tahoma = SYM.auto()
  Tahoma.value = 5
  Calibri = SYM.auto()
  Calibri.value = 6
  Comic_Sans_MS = SYM.auto()
  Comic_Sans_MS.value = 7
  Helvetica = SYM.auto()
  Helvetica.value = 8
  Geneva = SYM.auto()
  Geneva.value = 9
  Lucida_Grande = SYM.auto()
  Lucida_Grande.value = 10
  DejaVu_Sans = SYM.auto()
  DejaVu_Sans.value = 11
  DejaVu_Serif = SYM.auto()
  DejaVu_Serif.value = 12
  DejaVu_Sans_Mono = SYM.auto()
  DejaVu_Sans_Mono.value = 13
  Liberation_Sans = SYM.auto()
  Liberation_Sans.value = 14
  Liberation_Serif = SYM.auto()
  Liberation_Serif.value = 15
  Liberation_Mono = SYM.auto()
  Liberation_Mono.value = 16
  Ubuntu = SYM.auto()
  Ubuntu.value = 17
  Cantarell = SYM.auto()
  Cantarell.value = 18
  Droid_Sans = SYM.auto()
  Droid_Sans.value = 19
  Droid_Serif = SYM.auto()
  Droid_Serif.value = 20
  Roboto = SYM.auto()
  Roboto.value = 21
  Roboto_Condensed = SYM.auto()
  Roboto_Condensed.value = 22
  Roboto_Mono = SYM.auto()
  Roboto_Mono.value = 23
  Noto_Sans = SYM.auto()
  Noto_Sans.value = 24
  Noto_Serif = SYM.auto()
  Noto_Serif.value = 25
  Noto_Sans_Mono = SYM.auto()
  Noto_Sans_Mono.value = 26
  Source_Sans_Pro = SYM.auto()
  Source_Sans_Pro.value = 27
  Source_Serif_Pro = SYM.auto()
  Source_Serif_Pro.value = 28
  Source_Code_Pro = SYM.auto()
  Source_Code_Pro.value = 29
  Modern_No_20 = SYM.auto()
  Modern_No_20.value = 30
