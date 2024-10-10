"""The 'layer' module provides functionality relating to loading data and
environment variables."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from ._double_dollar_exception import DoubleDollarException
from ._validate_file import validateFile
from ._apply_existing_env import applyExistingEnv
from ._find_env_names import findEnvNames
from ._load_env import loadEnv
from ._apply_env import applyEnv
