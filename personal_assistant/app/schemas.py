import datetime as dt
from typing import Union
from pydantic import BaseModel

class ToolCallFunction(BaseModel):
    name: str
    arguments: str | dict

class ToolCall(BaseModel):
    id: str
    function: ToolCallFunction

class Message(BaseModel):
    toolCalls: list[ToolCall]

class VapiRequest(BaseModel):
    message: Message

class TodoResponse(BaseModel):
    id: int
    title: str
    description: Union[str, None]
    completed: bool
    class Config:
        orm_mode = True

class ReminderResponse(BaseModel):
    id: int
    reminder_text: str
    importance: str
    class Config:
        orm_mode = True

class CalendarEventResponse(BaseModel):
    id: int
    title: str
    description: Union[str, None]
    event_from: dt.datetime
    event_to: dt.datetime
    class Config:
        orm_mode = True