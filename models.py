from dataclasses import dataclass
from datetime import date
from enum import Enum
from typing import Optional

class Status(Enum):
    TODO = "todo"
    DOING = "doing"
    DONE = "done"

@dataclass
class Task:
    id: int
    title: str
    description: str
    status: Status
    deadline: Optional[date] = None

@dataclass
class Project:
    id: int
    name: str
    description: str
    tasks: list[Task]
    task_id_counter: int = 1

