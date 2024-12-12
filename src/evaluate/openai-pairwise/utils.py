from typing import Union
from dataclasses import dataclass

@dataclass(frozen=True)
class Paragraph:
    order: int
    data: Union[str, list[float]]
