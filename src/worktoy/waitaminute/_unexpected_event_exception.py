"""WorkToy - Wait A Minute! - UnexpectedEventException
Raised when receiving a QEvent of the wrong Type."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from worktoy.waitaminute import MetaXcept
from PySide6.QtCore import QEvent

TYPE = QEvent.Type


class UnexpectedEventException(MetaXcept):
  """WorkToy - Wait A Minute! - UnexpectedEventException
  Raised when receiving a QEvent of the wrong Type."""

  def __init__(self, expEvent: TYPE, actEvent: QEvent, argName: str,
               *args, **kwargs) -> None:
    MetaXcept.__init__(self, *args, **kwargs)
    self._expectedType = self.pretty(expEvent)
    self._actualEvent = self.pretty(actEvent)
    self._actualType = self.pretty(actEvent.Type)
    self._argName = self.pretty(argName)

  def __str__(self, ) -> str:
    header = MetaXcept.__str__(self)
    expType = self._expectedType
    actType = self._actualType
    argName = self._argName
    funcName = self.getSourceFunctionName()
    body = """Function '%s' expected event '%s' to be of event type: '%s', 
    but received event of type: '%s'. """
    msg = body % (funcName, argName, expType, actType)
    return '%s\n%s' % (header, self.justify(msg))
