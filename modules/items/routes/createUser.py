from fastapi import APIRouter, status, Request
from modules.items.schema.schemas import UserCreate, UserOut
from datetime import datetime, timezone

router = APIRouter(prefix="/users", tags=["users"])

def _get_store(request: Request):
    return request.app.state.users

def _next_id(request: Request) -> str:
    request.app.state._id_seq += 1
    return str(request.app.state._id_seq)

@router.post("", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_user(payload: UserCreate, request: Request):
    store = _get_store(request)
    now = datetime.now(timezone.utc)
    new_id = _next_id(request)
    store[new_id] = {
        "id": new_id,
        "username": payload.username,
        "email": payload.email,
        "role": payload.role,
        "password": payload.password,
        "created_at": now,
        "updated_at": now,
    }
    return {k: v for k, v in store[new_id].items() if k != "password"}