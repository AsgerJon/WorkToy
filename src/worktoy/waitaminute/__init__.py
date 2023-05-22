"""A collection of custom exception using the 'inspect' module to collect
contextual information. This is achieved by the 'ExceptionCore' class. A
few subclasses are included, but users are invited to subclass
'ExceptionCore' as needed. On its own, ExceptionCore does nothing more
than the builtin Exception, but it collects the following information as
properties:
  'instance': the class instance which raised the exception
  'insClass': the class of that instance
  'meth': the method which raised the exception
  'func': the outer function
The custom exception 'InstantiationError' is raised if an attempt is made to
instantiate a class illegally. For example to create new instances of a
singleton class. It then makes use of the 'insClass' property to inform
the user, which class contained the error.
"""
#  MIT License
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from ._exceptioncoreproperties import _ExceptionCoreProperties
from ._exceptioncore import ExceptionCore
from ._instantiationerror import InstantiationError
from ._proceduralerror import ProceduralError
from ._readonlyerror import ReadOnlyError
