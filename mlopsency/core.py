from __future__ import annotations
import os, sys, asyncio, functools
import importlib.util as libs
from pathlib import Path
from collections import defaultdict
from typing import DefaultDict, TypeVar, Optional, List
from datetime import datetime
import numpy as np
import jax as J

# TODO: development stage, will figuring in seamless way
if not libs.find_spec("mlopsency"): sys.path.append(Path.cwd().as_posix())

# TODO: Here are the Frontend with 2 main classes: Core and Ops
class Core:
  def __init__(self) -> None:
    self.state: DefaultDict = defaultdict()
    self._init_project = "mlopsency"
    self.time = datetime.now()
  
  def __repr__(self) -> str:
    return f"This is your Core info of {self._init_project} project: {self.time} | {self.state}"
  

class Ops:
  def __call__(self, *args: os.Any, **kwds: os.Any) -> os.Any:
    pass

if __name__ == '__main__':
  core = Core(); print(core)