#!/bin/bash
#
# AGPL-3.0 license
# Copyright (c) 2025 Asger Jon Vistisen
#

export RUNNING_TESTS=1
export PYTHONDONTWRITEBYTECODE=1  # Prevent __pycache__

# Run pytest with HTML report
python -OO -m pytest --cov-report=html

if [ $? -ne 0 ]; then
  echo "Tests failed — not opening HTML report."
  exit 1
fi

xdg-open htmlcov/index.html