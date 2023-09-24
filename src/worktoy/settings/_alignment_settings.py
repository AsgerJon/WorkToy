"""WorkSide - Settings - Alignment Flags
Names and settings relating to alignment flags."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import Optional

from PySide6.QtCore import Qt

from PySide6.QtWidgets import QSizePolicy

tabIndent = '  '  # Default is to use two spaces.
maxLineLen = 77
maxPageHeight = 50

AlignFlag = Qt.AlignmentFlag
AlignLeft = Qt.AlignmentFlag.AlignLeft
AlignHCenter = Qt.AlignmentFlag.AlignHCenter
AlignRight = Qt.AlignmentFlag.AlignRight
AlignTop = Qt.AlignmentFlag.AlignTop
AlignVCenter = Qt.AlignmentFlag.AlignVCenter
AlignBottom = Qt.AlignmentFlag.AlignBottom
AlignCenter = Qt.AlignmentFlag.AlignCenter
AlignJustify = Qt.AlignmentFlag.AlignJustify

FrameLess = Qt.WindowType.FramelessWindowHint
OnTop = Qt.WindowType.WindowStaysOnTopHint
Translucent = Qt.WidgetAttribute.WA_TranslucentBackground
OutputOnly = Qt.WindowType.WindowTransparentForInput

MinExpand = QSizePolicy.Policy.MinimumExpanding
Contract = QSizePolicy.Policy.Maximum
Pref = QSizePolicy.Policy.Preferred

verticalNames = ['top', 'bottom', ]
verticalFlags = [AlignTop, AlignBottom]
verticalMap = {k: v for k, v in zip(verticalNames, verticalFlags)}
horizontalNames = ['left', 'right', ]
horizontalFlags = [AlignLeft, AlignRight]
horizontalMap = {k: v for k, v in zip(horizontalNames, horizontalFlags)}
alignMap = {**horizontalMap, **verticalMap}


def getNamedAlignment(*alignments: str) -> AlignFlag:
  """Getter-function for the alignment flag for the named alignments. """
  if all([i in alignments for i in verticalNames]):
    raise ValueError
  if all([i in alignments for i in horizontalNames]):
    raise ValueError
  flags = []
  for arg in alignments:
    flag = alignMap.get(arg, None)
    if isinstance(flag, AlignFlag):
      flags.append(flag)
  align = 0
  for f in flags:
    align |= f
  return Qt.AlignmentFlag(align)


def getHorizontal(alignFlag: AlignFlag) -> AlignFlag:
  """Getter-function for the horizontal part of the given flag."""
  for flag in [AlignLeft, AlignHCenter, AlignRight]:
    if flag in alignFlag:
      return flag


def getVertical(alignFlag: AlignFlag) -> AlignFlag:
  """Getter-function for the vertical part of the given flag."""
  for flag in [AlignTop, AlignVCenter, AlignBottom]:
    if flag in alignFlag:
      return flag


def getPolicy(horizontal: Optional[bool],
              vertical: bool = None) -> QSizePolicy:
  """Getter-function for size policy. 'True' means minimum expanding,
  and 'False' means maximum. 'None' means preferred."""
  if horizontal is None:
    horizontalPolicy = Pref
  elif horizontal:
    horizontalPolicy = MinExpand
  else:
    horizontalPolicy = Contract

  if vertical is None:
    verticalPolicy = Pref
  elif vertical:
    verticalPolicy = MinExpand
  else:
    verticalPolicy = Contract
  policy = QSizePolicy()
  policy.setVerticalPolicy(verticalPolicy)
  policy.setHorizontalPolicy(horizontalPolicy)
  return policy
