import os
import sys
from pathlib import Path

import tomlkit


if getattr(sys, 'frozen', False):
    SCRIPT_DIR = Path(sys.executable).parent
else:
    SCRIPT_DIR = Path(__file__).resolve().parent


SETTINGS_TOML = os.path.normpath(f'{SCRIPT_DIR}/settings.toml')

if not os.path.isfile(SETTINGS_TOML):
    raise FileNotFoundError(f'The following file was not found: "{SETTINGS_TOML}"')

with open(SETTINGS_TOML, 'r') as f:
    SETTINGS = tomlkit.load(f)


def save_settings():
    with open(SETTINGS_TOML, 'w') as fp:
        tomlkit.dump(SETTINGS, fp)
