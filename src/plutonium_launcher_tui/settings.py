import os
import sys
from pathlib import Path

import tomlkit

SCRIPT_DIR = Path(sys.executable).parent if getattr(sys, "frozen", False) else Path(__file__).resolve().parent

SETTINGS_TOML = os.path.normpath(f"{SCRIPT_DIR}/settings.toml")


if not os.path.isfile(SETTINGS_TOML):
    error_message = f'The following file was not found: "{SETTINGS_TOML}"'
    raise FileNotFoundError(error_message)

with open(SETTINGS_TOML) as f:
    SETTINGS = tomlkit.load(f)


def save_settings():
    with open(SETTINGS_TOML, "w") as fp:
        tomlkit.dump(SETTINGS, fp)
