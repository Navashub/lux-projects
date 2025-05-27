from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
import json
from ..database import get_db
from ..models import Reminder
from ..schemas import VapiRequest, ReminderResponse

router = APIRouter()

@router.post('/add_reminder/')
def add_reminder(request: VapiRequest, db: Session = Depends(get_db)):
    for tool_call in request.message.toolCalls:
        if tool_call.function.name == 'addReminder':
            args = tool_call.function.arguments
            if isinstance(args, str):
                args = json.loads(args)
            reminder_text = args.get('reminder_text')
            importance = args.get('importance')
            if not reminder_text or not importance:
                raise HTTPException(status_code=400, detail="Missing required fields")
            reminder = Reminder(reminder_text=reminder_text, importance=importance)
            db.add(reminder)
            db.commit()
            db.refresh(reminder)
            return {
                'results': [{
                    'toolCallId': tool_call.id,
                    'result': ReminderResponse.from_orm(reminder).dict()
                }]
            }
    raise HTTPException(status_code=400, detail="Invalid request")

@router.post('/get_reminders/')
def get_reminders(request: VapiRequest, db: Session = Depends(get_db)):
    for tool_call in request.message.toolCalls:
        if tool_call.function.name == 'getReminders':
            reminders = db.query(Reminder).all()
            return {
                'results': [{
                    'toolCallId': tool_call.id,
                    'result': [ReminderResponse.from_orm(reminder).dict() for reminder in reminders]
                }]
            }
    raise HTTPException(status_code=400, detail="Invalid request")

@router.post('/delete_reminder/')
def delete_reminder(request: VapiRequest, db: Session = Depends(get_db)):
    for tool_call in request.message.toolCalls:
        if tool_call.function.name == 'deleteReminder':
            args = tool_call.function.arguments
            if isinstance(args, str):
                args = json.loads(args)
            reminder_id = args.get('id')
            if not reminder_id:
                raise HTTPException(status_code=400, detail="Missing reminder ID")
            reminder = db.query(Reminder).filter(Reminder.id == reminder_id).first()
            if not reminder:
                raise HTTPException(status_code=404, detail="Reminder not found")
            db.delete(reminder)
            db.commit()
            return {
                'results': [{
                    'toolCallId': tool_call.id,
                    'result': {'id': reminder_id, 'deleted': True}
                }]
            }
    raise HTTPException(status_code=400, detail="Invalid request")