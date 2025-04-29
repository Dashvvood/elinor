import os
import sys
from typing import List
from dotenv import load_dotenv

def fast_loadenv_then_append_path(vars:List[str] = ["PROJECT_ROOT"]):
    load_dotenv()
    for var in vars:
        if var in os.environ:
            path = os.environ[var]
            if os.path.exists(path):
                sys.path.append(path)
            else:
                raise FileNotFoundError(f"Path {path} does not exist.")
        else:
            raise KeyError(f"Environment variable {var} not found.")

