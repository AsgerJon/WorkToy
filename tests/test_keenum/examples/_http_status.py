"""
HTTPStatus enumerates the standard HTTP response status codes.

This enumeration uses 'int' values that fall outside the index range of
the enumeration itself, which would normally cause the byIndex resolver
to win over the byValue resolver. The '__class_resolve__' method is
implemented to ensure that 'int' identifiers are always interpreted as
status codes, never as indices.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.keenum import KeeNum, Kee
from worktoy.waitaminute.keenum import KeeResolveError

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, Self


class HTTPStatus(KeeNum):
  """
  HTTPStatus enumerates the standard HTTP response status codes.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Enumerations - 1xx Informational
  CONTINUE = Kee[int](100)
  SWITCHING_PROTOCOLS = Kee[int](101)

  #  Enumerations - 2xx Success
  OK = Kee[int](200)
  CREATED = Kee[int](201)
  ACCEPTED = Kee[int](202)
  NO_CONTENT = Kee[int](204)

  #  Enumerations - 3xx Redirection
  MOVED_PERMANENTLY = Kee[int](301)
  FOUND = Kee[int](302)
  NOT_MODIFIED = Kee[int](304)

  #  Enumerations - 4xx Client Error
  BAD_REQUEST = Kee[int](400)
  UNAUTHORIZED = Kee[int](401)
  FORBIDDEN = Kee[int](403)
  NOT_FOUND = Kee[int](404)
  METHOD_NOT_ALLOWED = Kee[int](405)
  IM_A_TEAPOT = Kee[int](418)
  TOO_MANY_REQUESTS = Kee[int](429)

  #  Enumerations - 5xx Server Error
  INTERNAL_SERVER_ERROR = Kee[int](500)
  NOT_IMPLEMENTED = Kee[int](501)
  BAD_GATEWAY = Kee[int](502)
  SERVICE_UNAVAILABLE = Kee[int](503)
  GATEWAY_TIMEOUT = Kee[int](504)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @classmethod
  def __class_resolve__(cls, identifier: Any) -> Self:
    """
    Resolves 'int' identifiers as status codes rather than indices.

    Without this resolver, 'HTTPStatus(0)' would return the member at
    index 0 (CONTINUE), and 'HTTPStatus(1)' would return the member at
    index 1 (SWITCHING_PROTOCOLS). With this resolver, both raise
    'KeeResolveError' because no member has value 0 or 1.

    Parameters
    ----------
    identifier : Any
      The identifier to resolve.

    Returns
    -------
    Self
      The matching HTTPStatus member.

    Raises
    ------
    KeeResolveError
      If 'identifier' is an 'int' with no matching status code.
    """
    if not isinstance(identifier, int):
      raise KeeResolveError(cls, identifier)
    if isinstance(identifier, bool):
      raise KeeResolveError(cls, identifier)
    for member in cls:
      if member.value == identifier:
        return member
    raise KeeResolveError(cls, identifier)
