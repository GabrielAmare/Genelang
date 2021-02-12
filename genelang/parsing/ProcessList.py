from typing import Tuple
from .Process import Process
from genelang.bricks import BrickList


class ProcessList(BrickList, Process):
    items: Tuple[Process]
