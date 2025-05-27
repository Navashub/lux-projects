from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
import json
from ..database import get_db
from ..models import Todo
from ..schemas import VapiRequest, TodoResponse

router = APIRouter()

@router.post('/create_todo/')
def create_todo(request: VapiRequest, db: Session = Depends(get_db)):
    for tool_call in request.message.toolCalls:
        if tool_call.function.name == 'createTodo':
            args = tool_call.function.arguments
            break
    else:
        raise HTTPException(status_code=400, detail='Invalid Request')

    if isinstance(args, str):
        args = json.loads(args)

    title = args.get('title', '')
    description = args.get('description', '')

    todo = Todo(title=title, description=description)

    db.add(todo)
    db.commit()
    db.refresh(todo)

    return {
        'results': [
            {
                'toolCallId': tool_call.id,
                'result': 'success'
            }
        ]
    }

@router.post('/get_todos/')
def get_todos(request: VapiRequest, db: Session = Depends(get_db)):
    for tool_call in request.message.toolCalls:
        if tool_call.function.name == 'getTodos':
            todos = db.query(Todo).all()

            return {
                'results': [
                    {
                        'toolCallId': tool_call.id,
                        'result': [TodoResponse.from_orm(todo).dict() for todo in todos]
                    }
                ]
            }
    else:
        raise HTTPException(status_code=400, detail='Invalid Request')

@router.post('/complete_todo/')
def complete_todo(request: VapiRequest, db: Session = Depends(get_db)):
    for tool_call in request.message.toolCalls:
        if tool_call.function.name == 'completeTodo':
            args = tool_call.function.arguments
            break
    else:
        raise HTTPException(status_code=400, detail='Invalid Request')

    if isinstance(args, str):
        args = json.loads(args)

    todo_id = args.get('id')

    if not todo_id:
        raise HTTPException(status_code=400, detail='Missing To-Do ID')

    todo = db.query(Todo).filter(Todo.id == todo_id).first()

    if not todo:
        raise HTTPException(status_code=404, detail='Todo not found')

    todo.completed = True

    db.commit()
    db.refresh(todo)

    return {
        'results': [
            {
                'toolCallId': tool_call.id,
                'result': 'success'
            }
        ]
    }

@router.post('/delete_todo/')
def delete_todo(request: VapiRequest, db: Session = Depends(get_db)):
    for tool_call in request.message.toolCalls:
        if tool_call.function.name == 'deleteTodo':
            args = tool_call.function.arguments
            break
    else:
        raise HTTPException(status_code=400, detail='Invalid Request')

    if isinstance(args, str):
        args = json.loads(args)

    todo_id = args.get('id')

    if not todo_id:
        raise HTTPException(status_code=400, detail='Missing To-Do ID')

    todo = db.query(Todo).filter(Todo.id == todo_id).first()

    if not todo:
        raise HTTPException(status_code=404, detail='Todo not found')

    db.delete(todo)
    db.commit()

    return {
        'results': [
            {
                'toolCallId': tool_call.id,
                'result': 'success'
            }
        ]
    }