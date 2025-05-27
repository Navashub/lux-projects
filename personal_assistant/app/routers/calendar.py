from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
import json
import datetime as dt
from ..database import get_db
from ..models import CalendarEvent
from ..schemas import VapiRequest, CalendarEventResponse

router = APIRouter()

@router.post('/add_calendar_entry/')
def add_calendar_entry(request: VapiRequest, db: Session = Depends(get_db)):
    for tool_call in request.message.toolCalls:
        if tool_call.function.name == 'addCalendarEntry':
            args = tool_call.function.arguments
            if isinstance(args, str):
                args = json.loads(args)
            title = args.get('title', '')
            description = args.get('description', '')
            event_from_str = args.get('event_from', '')
            event_to_str = args.get('event_to', '')
            
            if not title or not event_from_str or not event_to_str:
                raise HTTPException(status_code=400, detail="Missing required fields")
            
            try:
                event_from = dt.datetime.fromisoformat(event_from_str)
                event_to = dt.datetime.fromisoformat(event_to_str)
            except ValueError:
                raise HTTPException(status_code=400, detail="Invalid date format. Use ISO format.")
            
            calendar_event = CalendarEvent(
                title=title,
                description=description,
                event_from=event_from,
                event_to=event_to
            )
            db.add(calendar_event)
            db.commit()
            db.refresh(calendar_event)
            return {
                'results': [{
                    'toolCallId': tool_call.id,
                    'result': CalendarEventResponse.from_orm(calendar_event).dict()
                }]
            }
    raise HTTPException(status_code=400, detail="Invalid request")

@router.post('/get_calendar_entries/')
def get_calendar_entries(request: VapiRequest, db: Session = Depends(get_db)):
    for tool_call in request.message.toolCalls:
        if tool_call.function.name == 'getCalendarEntries':
            events = db.query(CalendarEvent).all()
            return {
                'results': [{
                    'toolCallId': tool_call.id,
                    'result': [CalendarEventResponse.from_orm(event).dict() for event in events]
                }]
            }
    raise HTTPException(status_code=400, detail="Invalid request")

@router.post('/delete_calendar_entry/')
def delete_calendar_entry(request: VapiRequest, db: Session = Depends(get_db)):
    for tool_call in request.message.toolCalls:
        if tool_call.function.name == 'deleteCalendarEntry':
            args = tool_call.function.arguments
            if isinstance(args, str):
                args = json.loads(args)
            event_id = args.get('id')
            if not event_id:
                raise HTTPException(status_code=400, detail="Missing event ID")
            event = db.query(CalendarEvent).filter(CalendarEvent.id == event_id).first()
            if not event:
                raise HTTPException(status_code=404, detail="Calendar event not found")
            db.delete(event)
            db.commit()
            return {
                'results': [{
                    'toolCallId': tool_call.id,
                    'result': {'id': event_id, 'deleted': True}
                }]
            }
    raise HTTPException(status_code=400, detail="Invalid request")