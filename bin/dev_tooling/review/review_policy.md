# Review Policy

This document outlines how AI-reviews are to be conducted. AI help are
split into the following:

- Research
- Review
- Development
- Ad hoc

Research loads the source code into the context window. Review studies
the loaded source code for particular tasks given, typically finding bugs
and inconsistencies. Development fixes the issues found in review. Ad hoc
is for user requests.

The prompts of the first two stand beside this file:
`research_prompt.txt` and `final_review_rc_prompt.txt`. The reports of
earlier reviews are under `archive`.

