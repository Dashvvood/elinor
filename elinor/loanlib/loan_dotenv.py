import os
import sys
from typing import List
from dotenv import load_dotenv
from types import SimpleNamespace

def fast_loadenv_then_append_path(vars:List[str] = ["PROJECT_ROOT"]):
    load_dotenv()
    ns = SimpleNamespace(**{k: None for k in vars}) 

    for var in vars:
        if var in os.environ:
            path = os.environ[var]
            ns.__setattr__(var, path)
            if os.path.exists(path):
                sys.path.append(path)
            else:
                raise FileNotFoundError(f"Path {path} does not exist.")
        else:
            raise KeyError(f"Environment variable {var} not found.")
        
    return ns

