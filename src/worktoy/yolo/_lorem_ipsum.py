"""LoremIpsum class for generating random text."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from random import shuffle, choice, choices


class Paragraph:
  """Static methods"""

  @staticmethod
  def atCharLen(n_: int) -> str:
    """Creates a paragraph of length n containing s sentences."""
    S = []
    n = n_
    while n > 20:
      S.append(int(n * 0.6))
      n -= S[-1]
    S.append(n + 1)
    shuffle(S)
    out = [Sentence.atLen(s) for s in S]
    return ' '.join(out)


class Vocabulary:
  """This class provides access to the words used."""

  @staticmethod
  def getWords() -> list[str]:
    """Returns a list of normal words"""
    return [
        'exercitationem', 'perferendis', 'perspiciatis', 'laborum',
        'eveniet',
        'sunt', 'iure', 'nam', 'nobis', 'eum', 'cum', 'officiis',
        'excepturi',
        'odio', 'consectetur', 'quasi', 'aut', 'quisquam', 'vel', 'eligendi',
        'itaque', 'non', 'odit', 'tempore', 'quaerat', 'dignissimos',
        'facilis', 'neque', 'nihil', 'expedita', 'vitae', 'vero', 'ipsum',
        'nisi', 'animi', 'cumque', 'pariatur', 'velit', 'modi', 'natus',
        'iusto', 'eaque', 'sequi', 'illo', 'sed', 'ex', 'et', 'voluptatibus',
        'tempora', 'veritatis', 'ratione', 'assumenda', 'incidunt',
        'nostrum',
        'placeat', 'aliquid', 'fuga', 'provident', 'praesentium', 'rem',
        'necessitatibus', 'suscipit', 'adipisci', 'quidem', 'possimus',
        'voluptas', 'debitis', 'sint', 'accusantium', 'unde', 'sapiente',
        'voluptate', 'qui', 'aspernatur', 'laudantium', 'soluta', 'amet',
        'quo', 'aliquam', 'saepe', 'culpa', 'libero', 'ipsa', 'dicta',
        'reiciendis', 'nesciunt', 'doloribus', 'autem', 'impedit', 'minima',
        'maiores', 'repudiandae', 'ipsam', 'obcaecati', 'ullam', 'enim',
        'totam', 'delectus', 'ducimus', 'quis', 'voluptates', 'dolores',
        'molestiae', 'harum', 'dolorem', 'quia', 'voluptatem', 'molestias',
        'magni', 'distinctio', 'omnis', 'illum', 'dolorum', 'voluptatum',
        'ea',
        'quas', 'quam', 'corporis', 'quae', 'blanditiis', 'atque',
        'deserunt',
        'laboriosam', 'earum', 'consequuntur', 'hic', 'cupiditate',
        'quibusdam', 'accusamus', 'ut', 'rerum', 'error', 'minus', 'eius',
        'ab', 'ad', 'nemo', 'fugit', 'officia', 'at', 'in', 'id', 'quos',
        'reprehenderit', 'numquam', 'iste', 'fugiat', 'sit', 'inventore',
        'beatae', 'repellendus', 'magnam', 'recusandae', 'quod', 'explicabo',
        'doloremque', 'aperiam', 'consequatur', 'asperiores', 'commodi',
        'optio', 'dolor', 'labore', 'temporibus', 'repellat', 'veniam',
        'architecto', 'est', 'esse', 'mollitia', 'nulla', 'a', 'similique',
        'eos', 'alias', 'dolore', 'tenetur', 'deleniti', 'porro', 'facere',
        'maxime', 'corrupti',
    ]

  @staticmethod
  def getCommonWords() -> list[str]:
    """Returns a list of common words"""
    return [
        'lorem', 'ipsum', 'dolor', 'sit', 'amet', 'consectetur',
        'adipisicing', 'elit', 'sed', 'do', 'eiusmod', 'tempor',
        'incididunt',
        'ut', 'labore', 'et', 'dolore', 'magna', 'aliqua',
    ]


class Sentence:
  """The static methods"""

  @staticmethod
  def wordLen(words: list[str], n: int) -> list[[int, str]]:
    """Given a list of words and an integer, this method returns a list of
    words from the list that has length equal to the integer"""
    words = [word for word in words if word.find(',') < 0]
    words = [word for word in words if word.find('.') < 0]
    words = [word for word in words if word.lower() == word]
    if n < 0:
      return words
    out = [word for word in enumerate(words) if len(word) == n]
    if out:
      return out
    return Sentence.wordLen(words, n - 1)

  @staticmethod
  def adjLen(
      target: list[str],
      source: list[str], d: int = None) -> list[
    str]:
    """Replaces a word in target with a word from source one char shorter."""
    targetN = max([len(word) for word in Sentence.wordLen(target, -1)])
    sourceN = max([len(word) for word in Sentence.wordLen(source, -1)])
    removeWords = []
    insertWords = []
    while not (removeWords and insertWords):
      removeWords = Sentence.wordLen(target, targetN)
      insertWords = Sentence.wordLen(source, sourceN + d)
      targetN -= 1
      sourceN -= 1
    if not (removeWords and insertWords):
      raise ValueError()
    removeWord = choice(removeWords)
    insertWord = choice(insertWords)
    inds = [i for (i, word) in enumerate(target) if word == removeWord[1]]
    target[choice(inds)] = insertWord[1]
    return target

  @staticmethod
  def collectWords():
    """Collects words from the vocabulary"""
    return Vocabulary.getWords() + Vocabulary.getCommonWords() * 9

  @staticmethod
  def atLen(n: int = None) -> str:
    """The strength length is the length of each word increased by 1.
    The expected number of characters between each comma."""
    nCommas = n // 50
    n -= nCommas
    out = []
    words = Sentence.collectWords()
    while sum([len(word) + 1 for word in out]) < n:
      out.append(choice(words))

    while sum([len(word) + 1 for word in out]) > n:
      out = Sentence.adjLen(out, words, -1)

    lots = [i for (i, word) in enumerate(out)]
    for i in range(nCommas):
      ind = choice(lots)
      lots = [i for i in lots if i != ind]
      out[ind] = '%s,' % (out[ind])
    endChars = ['.', '!', '?']
    weights_ = [10, 1, 2]
    out = '%s%s' % (' '.join(out), choices(endChars, weights=weights_, )[0])
    out = '%s%s' % (out[0].upper(), out[1:])
    for char in endChars:
      while out.find(',%s' % (char)) > 0:
        out = out.replace(',%s' % (char), char)
    return out


def loremIpsum(n: int = None) -> str:
  """Main entry point"""
  n = 600 if n is None else n
  return Paragraph.atCharLen(n)
