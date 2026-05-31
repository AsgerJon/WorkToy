# Contributing

Thank you for taking an interest in the development of *worktoy*!

## Setup

*worktoy* has no runtime dependencies. `environment.yml` provides a
convenient development environment that includes commonly used tools.
Install miniforge3 as relevant to your platform and then run:

```
mamba env create -f environment.yml
mamba activate worktoy_env
```

Replace `mamba` with `conda` if you prefer.

## Tests

The whole suite must pass at 100% branch coverage. Run it from the project
root with `./coverage_test.sh`, which runs pytest with branch coverage and
opens the HTML report in the system browser provided the tests pass.

## LICENSE

worktoy is released under Apache-2.0, and contributions are accepted under
the same license.
