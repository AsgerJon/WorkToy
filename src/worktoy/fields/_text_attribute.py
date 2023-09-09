"""WorkToy - Fields - TextAttribute
Implements multiline text attributes. """
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from worktoy.fields import AbstractField, IntAttribute


class TextAttribute(AbstractField):
  """WorkToy - Fields - TextAttribute
  Implements multiline text attributes. """

  lineLength = 72

  def __init__(self, *args, **kwargs) -> None:
    AbstractField.__init__(self, *args, **kwargs)
    self._left = '  # |'
    self._right = '| #  '
    self._sectionHeaderTop = '¨'
    self._sectionHeaderBottom = '_'
    self._sectionHeaderTopLeft = '  # /¨'
    self._sectionHeaderTopRight = '¨\\ #  '
    self._sectionHeaderMidLeft = self._left
    self._sectionHeaderMidRight = self._right
    self._sectionHeaderBottomLeft = '  # \\_'
    self._sectionHeaderBottomRight = '_/ #  '
    self._contents = """
    
    Descriptor implementation of widget values from events.
    
    In the class body of a subclass of CoreWidget, set an instance of
    EventField on an event method. Then instances of the subclass will have
    access to that value directly.
    
    For example:
    
      class Widget(CoreWidget):
        #  Subclass of CoreWidget
    
        localMouse = EventField(QMouseEvent.position, QMouseEvent)
        globalMouse = EventField(globalPosition, QEvent.Type.MouseMove)
    
    The EventField constructor supports the following signatures:
      - (event: QEvent) -> (value), (QEvent.Type=Any)
      - (event: QEvent) -> (value)
    The second argument should be used to restrict value updates to only the
    indicated type. Please note that the 'Type' referred the Enum, not the
    class. Two events of the same 'type' may have different 'Type'. The
    explicit setter function inherited from AbstractField is invoked on the
    value returned by the indicated method."""

  def showHeader(self, header: str) -> str:
    """Shows the header"""

    # self._sectionHeaderTop = '¨'
    # self._sectionHeaderBottom = '_'
    # self._sectionHeaderTopLeft = '  # /¨'
    # self._sectionHeaderTopRight = '¨\\ #  '
    # self._sectionHeaderMidLeft = self._left
    # self._sectionHeaderMidRight = self._right
    # self._sectionHeaderBottomLeft = '  # \\_'
    # self._sectionHeaderBottomRight = '_/ #  '

    topLeft = self._sectionHeaderTopLeft
    topRight = self._sectionHeaderTopRight
    topN = self.lineLength - len(topLeft) - len(topRight)
    topMid = topN * self._sectionHeaderTop
    top = '%s%s%s' % (topLeft, topMid, topRight)

    bottomLeft = self._sectionHeaderBottomLeft
    bottomRight = self._sectionHeaderBottomRight
    bottomN = self.lineLength - len(bottomLeft) - len(bottomRight)
    bottomMid = bottomN * self._sectionHeaderBottom
    bottom = '%s%s%s' % (bottomLeft, bottomMid, bottomRight)

    n = self.lineLength - len(self._left) - len(self._right)
    n -= len(header)
    left, right = int(n / 2) + n % 2, int(n / 2)
    L = left * ' '
    R = right * ' '
    mid = '%s%s%s%s%s' % (self._left, L, header, R, self._right)

    return '\n'.join([top, mid, bottom])
