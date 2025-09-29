from fastapi import APIRouter, Depends, HTTPException, status, Request, Header
from modules.items.schema.schemas import UserUpdate, UserOut
from typing import Optional
from datetime import datetime, timezone

router = APIRouter(prefix="/users", tags=["users"])

def _get_store(request: Request):
    return request.app.state.users

class Identity:
    def __init__(self, user_id: Optional[str], role: Optional[str]):
        self.user_id = user_id
        self.role = role

async def get_identity(
    x_user_id: Optional[str] = Header(None, alias="X-User-Id"),
    x_role: Optional[str] = Header(None, alias="X-Role"),
) -> Identity:
    return Identity(user_id=x_user_id, role=x_role)

def require_admin(identity: Identity = Depends(get_identity)) -> Identity:
    if identity.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="admin only")
    return identity

@router.patch("/{user_id}", response_model=UserOut)
def update_user(user_id: str, payload: UserUpdate, request: Request, _=Depends(require_admin)):
    store = _get_store(request)
    u = store.get(user_id)
    if not u:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")

    for field in ("username", "email", "role", "password"):
        val = getattr(payload, field)
        if val is not None:
            u[field] = val

    u["updated_at"] = datetime.now(timezone.utc)
    return {k: v for k, v in u.items() if k != "password"}