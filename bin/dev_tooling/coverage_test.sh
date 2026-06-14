#!/usr/bin/env sh
#
# Apache-2.0 license
# Copyright (c) 2025-2026 Asger Jon Vistisen
#

set -eu

#  Anchor the working directory so relative paths resolve
#  no matter where the script is invoked from.
cd "$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)"

export DEVELOPMENT_ENVIRONMENT=1
export PYTHONDONTWRITEBYTECODE=1
export MARKWORK_ETC_DIR="$(pwd)/etc"

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
