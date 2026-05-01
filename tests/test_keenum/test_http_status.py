"""
TestHTTPStatusResolve tests the '__class_resolve__' method of the
'HTTPStatus' enumeration.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.waitaminute.keenum import KeeResolveError
from . import KeeTest
from .examples import HTTPStatus

if TYPE_CHECKING:  # pragma: no cover
  pass


class TestHTTPStatusResolve(KeeTest):
  """
  TestHTTPStatusResolve tests the '__class_resolve__' method of the
  'HTTPStatus' enumeration.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  PUBLIC METHODS   # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def test_resolveByValueCommon(self) -> None:
    """Common status codes resolve to the correct member by value."""
    self.assertIs(HTTPStatus(200), HTTPStatus.OK)
    self.assertIs(HTTPStatus(404), HTTPStatus.NOT_FOUND)
    self.assertIs(HTTPStatus(500), HTTPStatus.INTERNAL_SERVER_ERROR)

  def test_resolveByValueAllRanges(self) -> None:
    """At least one member from each status range resolves correctly."""
    self.assertIs(HTTPStatus(100), HTTPStatus.CONTINUE)
    self.assertIs(HTTPStatus(201), HTTPStatus.CREATED)
    self.assertIs(HTTPStatus(301), HTTPStatus.MOVED_PERMANENTLY)
    self.assertIs(HTTPStatus(418), HTTPStatus.IM_A_TEAPOT)
    self.assertIs(HTTPStatus(503), HTTPStatus.SERVICE_UNAVAILABLE)

  def test_indexRangeNotMistakenForValue(self) -> None:
    """
    Integers in the index range but not matching any value raise.

    Without '__class_resolve__', 'HTTPStatus(0)' would return the
    member at index 0 (CONTINUE). The custom resolver prevents this.
    """
    with self.assertRaises(KeeResolveError):
      _ = HTTPStatus(0)
    with self.assertRaises(KeeResolveError):
      _ = HTTPStatus(1)
    with self.assertRaises(KeeResolveError):
      _ = HTTPStatus(5)

  def test_unknownStatusCodeRaises(self) -> None:
    """Integers outside any status range raise 'KeeResolveError'."""
    with self.assertRaises(KeeResolveError):
      _ = HTTPStatus(999)
    with self.assertRaises(KeeResolveError):
      _ = HTTPStatus(-1)
    with self.assertRaises(KeeResolveError):
      _ = HTTPStatus(200000)

  def test_byNameStillWorks(self) -> None:
    """
    String identifiers still resolve by name.

    The custom resolver does not interfere with the default
    name-based resolution path.
    """
    self.assertIs(HTTPStatus('OK'), HTTPStatus.OK)
    self.assertIs(HTTPStatus('not_found'), HTTPStatus.NOT_FOUND)
    self.assertIs(HTTPStatus('IM_A_TEAPOT'), HTTPStatus.IM_A_TEAPOT)

  def test_attributeAccessUnaffected(self) -> None:
    """Attribute access bypasses the custom resolver entirely."""
    self.assertEqual(HTTPStatus.OK.value, 200)
    self.assertEqual(HTTPStatus.NOT_FOUND.value, 404)
    self.assertEqual(HTTPStatus.IM_A_TEAPOT.value, 418)

  def test_memberPassthrough(self) -> None:
    """Passing an existing member returns the same member."""
    self.assertIs(HTTPStatus(HTTPStatus.OK), HTTPStatus.OK)
    self.assertIs(HTTPStatus(HTTPStatus.NOT_FOUND), HTTPStatus.NOT_FOUND)

  def test_boolRejected(self) -> None:
    """
    Bool identifiers are rejected by the top-level dispatch.

    'HTTPStatus' has 'valueType' of 'int', not 'bool', so 'True' and
    'False' must not resolve to members at index 0 or 1, nor to
    members with values 0 or 1.
    """
    with self.assertRaises(KeeResolveError):
      _ = HTTPStatus(True)
    with self.assertRaises(KeeResolveError):
      _ = HTTPStatus(False)

  def test_unsupportedTypeRaises(self) -> None:
    """Identifiers of unrelated types raise 'KeeResolveError'."""
    with self.assertRaises(KeeResolveError):
      _ = HTTPStatus(2.5)
    with self.assertRaises(KeeResolveError):
      _ = HTTPStatus(None)
    with self.assertRaises(KeeResolveError):
      _ = HTTPStatus([])

  def test_bad_value(self, ) -> None:
    """
    Test that passing a member with a value of an unsupported type raises
    a KeeTypeException.
    """
    with self.assertRaises(KeeResolveError) as context:
      _ = HTTPStatus(69420)
    e = context.exception
    self.assertIs(e.keeNum, HTTPStatus)
    self.assertEqual(e.identifier, 69420)
    self.assertEqual(str(e), repr(e))
