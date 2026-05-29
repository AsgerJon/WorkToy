"""
PlayerScore demonstrates how 'FidGen' organises the provision of
unique JSON file names for persisting instance state. Each call to
'save' writes a fresh '.json' file in the configured directory;
'load' reconstructs an instance from a previously written file.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from io import TextIOWrapper
import json
import os
from typing import TYPE_CHECKING

from worktoy.core.sentinels import THIS
from worktoy.desc import AttriBox
from worktoy.dispatch import overload
from worktoy.mcls import BaseObject
from worktoy.work_io import FidGen

if TYPE_CHECKING:  # pragma: no cover
  from typing import Self, Optional

_HERE = os.path.abspath(os.path.dirname(__file__))


class PlayerScore(BaseObject):
  """
  Demonstration class persisting its state to a JSON file. The path
  is supplied by a class-level 'FidGen' descriptor that allocates the
  next unused 'score_<n>.json' name in the configured directory.

  Construction overloads:
  - PlayerScore() -- defaults from AttriBox.
  - PlayerScore(name) -- name only, score and level default.
  - PlayerScore(name, score) -- name and score, level defaults.
  - PlayerScore(name, score, level) -- all three explicit.
  - PlayerScore(other) -- copy from another 'PlayerScore'.
  - PlayerScore(payload) -- inflate from a dict matching the JSON
    payload written by 'save'.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Class Variables
  fidGen = FidGen(dir=_HERE, ext='json', name='score')

  #  Public Variables
  name = AttriBox[str]('')
  score = AttriBox[int](0)
  level = AttriBox[int](0)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @overload()
  def __init__(self) -> None:
    """Default constructor; AttriBox supplies the field defaults."""

  @overload(str)
  def __init__(self, name: str) -> None:
    self.name = name

  @overload(str, int)
  def __init__(self, name: str, score: int) -> None:
    self.name = name
    self.score = score

  @overload(str, int, int)
  def __init__(self, name: str, score: int, level: int) -> None:
    self.name = name
    self.score = score
    self.level = level

  @overload(THIS)
  def __init__(self, other: Self) -> None:
    self.name = other.name
    self.score = other.score
    self.level = other.level

  @overload(dict)
  def __init__(self, payload: dict) -> None:
    self.name = payload['name']
    self.score = payload['score']
    self.level = payload['level']

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def save(self) -> str:
    """Write this score to a fresh JSON file.

    Returns
    -------
    str
      The path written to.
    """
    filePath = self.fidGen.nextName
    payload = dict(
      name=self.name,
      score=self.score,
      level=self.level,
    )
    f = None
    try:
      f = open(filePath, 'w')
    except Exception as exception:
      raise exception
    else:
      json.dump(payload, f)
    finally:
      try:
        # noinspection PyUnresolvedReferences
        f.close()
      except AttributeError:  # pragma: no cover
        pass
    return filePath

  @classmethod
  def load(cls, filePath: str) -> Self:
    """Reconstruct a 'PlayerScore' from a previously saved file.

    Parameters
    ----------
    filePath : str
      Path to a JSON file previously written by 'save'.

    Returns
    -------
    Self
      Fresh 'PlayerScore' populated from the file.
    """
    f: Optional[TextIOWrapper] = None
    payload = None
    try:
      f = open(filePath, 'r')
    except Exception as exception:
      raise exception
    else:
      if TYPE_CHECKING:  # pragma: no cover
        assert f is not None
      payload = json.loads(f.read())
    finally:
      try:
        # noinspection PyUnresolvedReferences
        f.close()
      except AttributeError:
        pass
    return cls(payload)
