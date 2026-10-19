"""
TestMemberInBodyMessage subclasses 'KeeTest' and pins the names in the
refusals a 'KeeNum' member placed in a class body raises when written or
deleted through an instance. The refusals themselves are by design: a
worktoy value in a class body is a shared, read-only class attribute.
The messages used to name the attribute 'Game.None', since a member is
a shared singleton that records no field name for any one placement, so
the name is found by looking the member up in the owner's classes at
the time of the refusal.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.keenum import KeeNum, Kee
from worktoy.waitaminute.desc import ReadOnlyError, ProtectedError
from . import KeeTest


class Piece(KeeNum):
  """Piece is a small enumeration placed in the class bodies below."""

  PAWN = Kee[int](1)
  ROOK = Kee[int](5)


class Game:
  """Game places a member in its class body."""

  piece = Piece.PAWN


class SubGame(Game):
  """SubGame inherits the placement from 'Game'."""

  pass


class Board:
  """Board places the same member under another name."""

  start = Piece.PAWN


class TestMemberInBodyMessage(KeeTest):
  """
  TestMemberInBodyMessage provides tests for the names in the refusals of
  instance writes and deletes of a member placed in a class body.
  """

  def test_write_names_the_placement(self) -> None:
    """A write through an instance names the owner and the attribute."""
    game = Game()
    with self.assertRaises(ReadOnlyError) as context:
      game.piece = Piece.ROOK
    e = context.exception
    self.assertIn("'Game.piece'", str(e))
    self.assertNotIn('None', str(e))
    self.assertIs(e.instance, game)
    self.assertIs(e.desc, Piece.PAWN)
    self.assertIs(e.newVal, Piece.ROOK)

  def test_delete_names_the_placement(self) -> None:
    """A delete through an instance names the owner and the attribute."""
    game = Game()
    with self.assertRaises(ProtectedError) as context:
      del game.piece
    e = context.exception
    self.assertIn("'Game.piece'", str(e))
    self.assertNotIn('None', str(e))
    self.assertIs(e.instance, game)
    self.assertIs(e.desc, Piece.PAWN)

  def test_inherited_placement(self) -> None:
    """A placement found in a base class is named with the class of the
    instance, as the attribute protocol reached it from there."""
    with self.assertRaises(ReadOnlyError) as context:
      SubGame().piece = Piece.ROOK
    self.assertIn("'SubGame.piece'", str(context.exception))

  def test_same_member_other_name(self) -> None:
    """The same member placed under another name in another class is
    named by that placement."""
    with self.assertRaises(ReadOnlyError) as context:
      Board().start = Piece.ROOK
    self.assertIn("'Board.start'", str(context.exception))
    with self.assertRaises(ProtectedError) as context:
      del Board().start
    self.assertIn("'Board.start'", str(context.exception))

  def test_unplaced_member_named_object(self) -> None:
    """A member placed in no class of the instance is named 'object',
    as an unplaced descriptor of any kind is."""
    e = ReadOnlyError(Game(), Piece.ROOK, 1)
    self.assertIn("'Game.object'", str(e))
    e = ProtectedError(Game(), Piece.ROOK, 1)
    self.assertIn("'Game.object'", str(e))

  def test_member_itself_unchanged(self) -> None:
    """The refusals leave the member and the placement untouched."""
    game = Game()
    try:
      game.piece = Piece.ROOK
    except ReadOnlyError:
      pass
    self.assertIs(game.piece, Piece.PAWN)
    self.assertIs(Game.piece, Piece.PAWN)
