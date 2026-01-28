#!/usr/bin/env sh
#
# AGPL-3.0 license
# Copyright (c) 2025 Asger Jon Vistisen
#

set -eu

export DEVELOPMENT_ENVIRONMENT=1

runTests() {
  reportDir="htmlcov"

  pytest \
    tests \
    --cov=worktoy \
    --cov=tests \
    --cov-branch \
    --cov-report=term-missing \
    --cov-report=html:"$reportDir"

  if [ -f "$reportDir/index.html" ]; then
    setsid xdg-open "$reportDir/index.html" >/dev/null 2>&1
  fi
}

runTests
