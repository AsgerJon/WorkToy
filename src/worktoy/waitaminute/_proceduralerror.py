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

from worktoy import searchKeys, maybe


class ProceduralError(Exception):
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
    instanceKwarg = searchKeys('instance') >> kwargs
    self.__name__ = 'ProceduralError'
    args = [*args, None, None]
    instanceArg = None
    if instanceKwarg is None:
      instanceArg = args[0]
      variableName = args[1]
      msg = args[2]
    else:
      variableName = args[0]
      msg = args[1]
    instance = maybe(instanceKwarg, instanceArg, )
    if instance is None:
      super().__init__('Could not determine source of error!')
    class_name = getattr(getattr(instance, '__class__'), '__name__')
    error_message = (
        "'%s.%s' is missing or empty for instance '%s'."
        % (class_name, variableName, instance)
    )
    if msg is None:
      super().__init__(error_message)
    super().__init__('\n'.join([error_message, maybe(msg, '')]))

  def __repr__(self) -> str:
    """String representation"""
    return 'ProceduralError'
