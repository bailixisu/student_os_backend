from pydantic import BaseModel
from sqlalchemy import null


class Memo(BaseModel):
    id: int
    content: str
    start_time: str
    deadline: str
    complete_time: str
    note: str
    sort: str
    color: int
    status: int
    like: int
    circulate: int


class SortMemo(BaseModel):
    sortText: str
    sort_icon_color: int
    sort_background_color: int
