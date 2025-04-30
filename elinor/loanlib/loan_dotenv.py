import os
import sys
from typing import List
from dotenv import load_dotenv
from types import SimpleNamespace

from deprecated import deprecated

@deprecated(reason="this fn cannot get the right env vars")
def fast_loadenv_then_append_path(vars:List[str] = ["PROJECT_ROOT"]):
    load_res = load_dotenv()
    print(f"load env: {load_res}")
    ns = SimpleNamespace(**{k: None for k in vars}) 

    for var in vars:
        path = os.getenv(var)
        ns.__setattr__(var, path)
        sys.path.append(path)
    return ns

