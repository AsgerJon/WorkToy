"""ProceduralError is raised when a series of operations happen in an
ordering that is not supported. A class may create instances in step one,
then apply data in step two, before being able to handle requests in step
three and beyond. So if another process requests data from an instance in
between step one and step two, a ProceduralError should be raised. If the
request was sent even before instance creation time, but the instance is
named in the namespace but assigned value None, a ProceduralError should
also be raised. If a process sends requests to a name not yet in the
namespace, a builtin NameError is the appropriate error."""
#  Copyright (c) 2023 Asger Jon Vistisen
#  MIT Licence
from __future__ import annotations

from typing import NoReturn

from worktoy.waitaminute import ExceptionCore


class ProceduralError(ExceptionCore):
  """ProceduralError is raised when a series of operations happen in an
  ordering that is not supported. A class may create instances in step one,
  then apply data in step two, before being able to handle requests in step
  three and beyond. So if another process requests data from an instance in
  between step one and step two, a ProceduralError should be raised. If the
  request was sent even before instance creation time, but the instance is
  named in the namespace but assigned value None, a ProceduralError should
  also be raised. If a process sends requests to a name not yet in the
  namespace, a builtin NameError is the appropriate error.
  #  Copyright (c) 2023 Asger Jon Vistisen
  #  MIT Licence"""

  def __init__(self, *args, **kwargs) -> None:
    ExceptionCore.__init__(self, *args, **kwargs)

  def _getMsg(self, ) -> NoReturn:
    """Procedural error indicates out of order operation"""
    from worktoy.stringtools import justify
    self._msg = justify("""This exception is caused by a process trying 
    to access a process not yet ready.""")
