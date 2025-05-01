import os
import sys
from typing import List
from dotenv import load_dotenv, find_dotenv, dotenv_values
from types import SimpleNamespace

from deprecated import deprecated

# @deprecated(reason="this fn cannot get the right env vars")
def fast_loadenv_then_append_path(append=True) -> SimpleNamespace:
    env_path = find_dotenv(usecwd=True)
    load_res = load_dotenv(dotenv_path=env_path)
    env_values = dotenv_values(dotenv_path=env_path)
    if append:
        for _, value in env_values.items():
            if os.path.exists(value) and os.path.isdir(value):
                sys.path.append(value)
    ns = SimpleNamespace(**env_values)
    return ns

