from __future__ import annotations
from typing import List

from API.data.config_class import BaseModel


####### Задачи

class Assignee(BaseModel):
    id: int
    fullName: str
    email: str
    avatarUrl: str


class Datum(BaseModel):
    id: int
    title: str
    description: str
    priority: str
    status: str
    assignee: Assignee
    boardId: int
    boardName: str


class Model(BaseModel):
    data: List[Datum]