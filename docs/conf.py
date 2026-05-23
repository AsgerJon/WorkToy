"""Sphinx configuration: render the worktoy source verbatim.

This build does NOT import worktoy, does NOT introspect it, and does
NOT parse docstrings as markup. Every page is one source file
rendered by docs/_gen.py: it highlights the file with Pygments into
an HTML fragment and embeds that via a `.. raw:: html` directive,
then wires the page into a navigation tree.

Sphinx is used only for the parts it is genuinely good at: building
the multi-page navigable, searchable, themed site and hosting it on
Read the Docs / GitHub Pages. None of the autodoc machinery is loaded.
"""
from __future__ import annotations

import sys
from pathlib import Path

#  Put this docs/ directory on sys.path so conf.py can import the
#  generator module (_gen) that lives beside it.
sys.path.insert(0, str(Path(__file__).parent))

from sphinx.application import Sphinx
from _gen import generate

# ============================================================
# Project metadata
# ============================================================
project = "worktoy"
author = "Asger Jon Vistisen"
copyright = "2026, Asger Jon Vistisen"
release = "0.99.137"

# ============================================================
# General configuration
# ============================================================
#
# No extensions are needed. The 'raw' and 'toctree' directives that
# the generated pages use are part of Sphinx / docutils core. We
# deliberately do NOT load autodoc, autosummary, or napoleon.
extensions = []

#  rst.txt is Asger's plain-text cheat sheet, not a doc page. The
#  generated _source/ pages ARE read (they are the site); _build is
#  the output directory.
exclude_patterns = ["_build", "rst.txt"]

# ============================================================
# HTML output
# ============================================================
html_theme = "furo"

#  Custom CSS / JS.
#    custom.css  : highlights the source line a '#line-N' link jumped
#                  to, and styles the version switcher box.
#    versions.js : the version switcher. On the multi-version GitHub
#                  Pages build it reads versions.json and shows a
#                  dropdown; on a local single-version build it finds
#                  no versions.json and stays silent.
html_static_path = ["_static"]
html_css_files = ["custom.css"]
html_js_files = ["versions.js"]


def setup(app: Sphinx) -> None:
  """Wire the source-page generator to run before Sphinx reads
  sources, so a plain `sphinx-build` regenerates docs/_source/ each
  time. This mirrors how sphinx.ext.autosummary generates its own
  stub files at builder-inited."""
  app.connect("builder-inited", generate)
