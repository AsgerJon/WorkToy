"""TestClassInitArgs verifies the metaclass-driven '__class_init__'
hook fires with the expected positional and keyword arguments after
the class body has finished executing."""
#  Apache-2.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.mcls import (
  AbstractMetaclass, AbstractNamespace, BaseObject,
)
from .. import MCLSTest


class Recorder(BaseObject, metaclass=AbstractMetaclass, sentinel='received'):
  """Fixture that records the arguments its '__class_init__' was
  called with so the test can inspect them."""

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Class Variables
  __recorded_cls__ = None
  __recorded_name__ = None
  __recorded_bases__ = None
  __recorded_space__ = None
  __recorded_kwargs__ = None

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @classmethod
  def __class_init__(cls, name, bases, space, **kwargs) -> None:
    """Record the arguments for later inspection."""
    type.__setattr__(cls, '__recorded_cls__', cls)
    type.__setattr__(cls, '__recorded_name__', name)
    type.__setattr__(cls, '__recorded_bases__', bases)
    type.__setattr__(cls, '__recorded_space__', space)
    type.__setattr__(cls, '__recorded_kwargs__', dict(kwargs))


class TestClassInitArgs(MCLSTest):
  """TestClassInitArgs verifies the metaclass-driven '__class_init__'
  hook fires with the expected arguments after class creation."""

  def test_cls_is_the_new_class(self) -> None:
    """The 'cls' argument is the class being created."""
    self.assertIs(Recorder.__recorded_cls__, Recorder)

  def test_name_is_recorded(self) -> None:
    """The class name reaches '__class_init__' as the 'name' arg."""
    self.assertEqual(Recorder.__recorded_name__, 'Recorder')

  def test_bases_include_base_object(self) -> None:
    """The bases tuple reaches '__class_init__' as the 'bases' arg."""
    self.assertIn(BaseObject, Recorder.__recorded_bases__)

  def test_space_is_a_namespace(self) -> None:
    """The namespace reaches '__class_init__' as the 'space' arg."""
    self.assertIsInstance(
      Recorder.__recorded_space__, AbstractNamespace
    )

  def test_class_kwargs_forwarded(self) -> None:
    """Keyword arguments on the class definition flow through to
    '__class_init__'."""
    self.assertEqual(
      Recorder.__recorded_kwargs__, {'sentinel': 'received'}
    )
