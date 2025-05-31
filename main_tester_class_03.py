"""
no annotations, but it's for a test, so chill out
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen

try:
  from typing import TYPE_CHECKING
except ImportError:
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
  annotations = dict(urmom='fat', )


def tester():
  try:
    print(annotations)
  except NameError as nameError:
    print('annotations not here cause: %s' % str(nameError))
  else:
    print("""Here be annotations: '%s'""" % str(annotations))
  finally:
    pass
  return 0


if __name__ != '__main__':
  tester()

exportSomeStuff = 69, 420
