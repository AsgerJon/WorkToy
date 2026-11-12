"""
The 'LOREM_WORDS' vocabulary, the 'randomWord' function and the
'loremSentence' function give the samplers of 'worktoy.work_test' their
text without the 'lorem_ipsum' package.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

import random
from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover, no mutate
  from random import Random
  from typing import Optional

#  A word of every length from one letter to the longest. That coverage is
#  what lets 'loremSentence' close a sentence at exactly the requested
#  number of characters.
LOREM_WORDS: tuple[str, ...] = (
  'a',
  'ad', 'et', 'ex', 'in', 'ut',
  'aut', 'est', 'eum', 'nec', 'non', 'qui', 'quo', 'sed', 'sit',
  'amet', 'elit', 'enim', 'illo', 'nisi', 'odio', 'quia', 'quis', 'vero',
  'autem', 'dolor', 'ipsum', 'lorem', 'magna', 'minim', 'nulla', 'omnis',
  'velit',
  'aliqua', 'fugiat', 'labore', 'minima', 'mollit', 'tempor', 'veniam',
  'aliquam', 'commodo', 'dolores', 'ducimus', 'eiusmod', 'eveniet',
  'laborum', 'nostrud', 'officia', 'quaerat',
  'deserunt', 'incidunt', 'occaecat', 'pariatur', 'suscipit', 'voluptas',
  'accusamus', 'cupidatat', 'doloribus', 'excepteur', 'molestiae',
  'voluptate',
  'adipiscing', 'aspernatur', 'laboriosam', 'voluptatem', 'voluptatum',
)

_LONGEST: int = max(len(word) for word in LOREM_WORDS)
#  The words of exactly each length, and the words of at most each length.
_OF_LENGTH: dict[int, tuple[str, ...]] = {
  n: (*(w for w in LOREM_WORDS if len(w) == n),)
  for n in range(1, _LONGEST + 1)
}
_UP_TO_LENGTH: dict[int, tuple[str, ...]] = {
  n: (*(w for w in LOREM_WORDS if len(w) <= n),)
  for n in range(1, _LONGEST + 1)
}


def _choose(words: tuple[str, ...], generator: Optional[Random]) -> str:
  """
  A sampler draws from a generator of its own, so that its seed repeats
  its words, while a caller with no generator draws as 'random.choice'
  does.

  Implementation
  --------------

  One of 'words' is drawn from 'generator', a 'random.Random', or from
  Python's own 'random' when none is given.
  """
  if generator is None:
    return random.choice(words)
  return generator.choice(words)


def randomWord(generator: Optional[Random] = None) -> str:
  """
  A test that needs a short string wants a real word rather than random
  letters, and a seeded sampler asking for one must get the same word
  again.

  Implementation
  --------------

  One word of 'LOREM_WORDS' is drawn, each as likely as any other, from
  'generator' when one is given and from Python's own 'random'
  otherwise.

  Parameters
  ----------

  generator : random.Random, optional
    The generator to draw from.

  Returns
  -------

  str
    The word.
  """
  return _choose(LOREM_WORDS, generator)


def _fittingWord(room: int, generator: Optional[Random] = None) -> str:
  """
  A sentence of an exact length is built word by word, and each word
  must leave the rest closable: after it either nothing is left, or
  room for a space and at least one more letter.

  Implementation
  --------------

  With room for no more than the longest word, a word of exactly that
  many letters is drawn, which closes the body; the vocabulary holds a
  word of every length for that. With more room, a word of at most two
  letters fewer than the room is drawn.

  Parameters
  ----------

  room : int
    The letters left in the body of the sentence.

  generator : random.Random, optional
    The generator to draw from.

  Returns
  -------

  str
    The word.
  """
  if room <= _LONGEST:
    return _choose(_OF_LENGTH[room], generator)
  return _choose(_UP_TO_LENGTH[min(room - 2, _LONGEST)], generator)


def loremSentence(charCount: int, generator: Optional[Random] = None) -> str:
  """
  A test of anything that lays out, wraps or cuts text wants text of a
  length it chooses to the character, which still reads as a sentence.

  Implementation
  --------------

  Words of 'LOREM_WORDS' are joined by single spaces, each chosen by
  '_fittingWord' so that the last one ends the body one character short
  of the count; the first letter is capitalised and a period closes the
  sentence. A count of one gives the period alone. The words are drawn
  from 'generator' when one is given and from Python's own 'random'
  otherwise.

  Parameters
  ----------

  charCount : int
    The length of the sentence, period included.

  generator : random.Random, optional
    The generator to draw from.

  Returns
  -------

  str
    The sentence.

  Raises
  ------

  ValueError
    'charCount' is below one.
  """
  if charCount < 1:
    infoSpec = """A sentence needs at least one character, but %d were
    asked for!"""
    raise ValueError(' '.join(infoSpec.split()) % charCount)
  words = []
  need = charCount - 1  # the body, before the closing period
  while need > 0:
    space = 1 if words else 0
    word = _fittingWord(need - space, generator)
    words.append(word)
    need -= len(word) + space
  body = ' '.join(words)
  return '%s%s.' % (body[:1].upper(), body[1:])
