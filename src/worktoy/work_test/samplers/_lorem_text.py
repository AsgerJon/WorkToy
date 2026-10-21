"""
The 'LOREM_WORDS' vocabulary, the 'randomWord' function and the
'loremSentence' function give the samplers of 'worktoy.work_test' their
text without the 'lorem_ipsum' package.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

import random

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


def randomWord() -> str:
  """
  The 'randomWord' function returns one word drawn uniformly from
  'LOREM_WORDS'.
  """
  return random.choice(LOREM_WORDS)


def _fittingWord(room: int) -> str:
  """
  The '_fittingWord' function returns a word that keeps a sentence
  closable within 'room' characters: a word of exactly 'room' letters
  when the vocabulary has one, which closes the body, and otherwise a
  word short enough to leave a space and at least one letter of room
  after it.
  """
  if room <= _LONGEST:
    return random.choice(_OF_LENGTH[room])
  return random.choice(_UP_TO_LENGTH[min(room - 2, _LONGEST)])


def loremSentence(charCount: int) -> str:
  """
  The 'loremSentence' function returns a sentence of exactly 'charCount'
  characters: words from 'LOREM_WORDS' joined by single spaces, the first
  letter capitalised and a period closing it. A count of one gives the
  period alone. A count below one is refused with 'ValueError'.
  """
  if charCount < 1:
    infoSpec = """A sentence needs at least one character, but %d were
    asked for!"""
    raise ValueError(' '.join(infoSpec.split()) % charCount)
  words = []
  need = charCount - 1  # the body, before the closing period
  while need > 0:
    space = 1 if words else 0
    word = _fittingWord(need - space)
    words.append(word)
    need -= len(word) + space
  body = ' '.join(words)
  return '%s%s.' % (body[:1].upper(), body[1:])
