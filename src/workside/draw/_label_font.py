"""WorkSide - Draw - LabelFont
Contains instances of QFont"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QPen, QColor, QBrush

labelFont = QFont()
labelFont.setFamily('Modern No. 20')
labelFont.setPointSize(16)
labelFont.setWeight(QFont.Weight.Normal)

labelFontPen = QPen()
labelFontPen.setStyle(Qt.PenStyle.SolidLine)
labelFontPen.setWidth(1)
labelFontPen.setColor(QColor(0, 0, 0, 255))

labelBrush = QBrush()
labelBrush.setStyle(Qt.BrushStyle.SolidPattern)
labelBrush.setColor(QColor(127, 255, 0, 255))

labelBoxPen = QPen()
labelBoxPen.setStyle(Qt.PenStyle.SolidLine)
labelBoxPen.setWidth(1)
labelBoxPen.setColor(QColor(0, 0, 0, 255))

#  Header

headerFont = QFont()
headerFont.setFamily('Modern No. 20')
headerFont.setPointSize(24)
headerFont.setWeight(QFont.Weight.Medium)

headerFontPen = QPen()
headerFontPen.setStyle(Qt.PenStyle.SolidLine)
headerFontPen.setWidth(1)
headerFontPen.setColor(QColor(0, 0, 0, 255))

headerBrush = QBrush()
headerBrush.setStyle(Qt.BrushStyle.SolidPattern)
headerBrush.setColor(QColor(127, 255, 0, 255))

headerBoxPen = QPen()
headerBoxPen.setStyle(Qt.PenStyle.SolidLine)
headerBoxPen.setWidth(1)
headerBoxPen.setColor(QColor(0, 0, 0, 255))

# Sub header

subHeaderFont = QFont()
subHeaderFont.setFamily('Modern No. 20')
subHeaderFont.setPointSize(20)
subHeaderFont.setWeight(QFont.Weight.Medium)

subHeaderFontPen = QPen()
subHeaderFontPen.setStyle(Qt.PenStyle.SolidLine)
subHeaderFontPen.setWidth(1)
subHeaderFontPen.setColor(QColor(0, 0, 0, 255))

subHeaderBrush = QBrush()
subHeaderBrush.setStyle(Qt.BrushStyle.SolidPattern)
subHeaderBrush.setColor(QColor(127, 255, 0, 255))

subHeaderBoxPen = QPen()
subHeaderBoxPen.setStyle(Qt.PenStyle.SolidLine)
subHeaderBoxPen.setWidth(1)
subHeaderBoxPen.setColor(QColor(0, 0, 255, 255))
