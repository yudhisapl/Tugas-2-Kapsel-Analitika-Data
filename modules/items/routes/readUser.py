from fastapi import APIRouter, Depends, HTTPException, status, Request, Header
from typing import List, Optional
from modules.items.schema.schemas import UserOut

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

def require_self_or_admin(user_id: str, identity: Identity = Depends(get_identity)) -> Identity:
    if identity.role == "admin":
        return identity
    if identity.role == "staff" and identity.user_id == user_id:
        return identity
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="forbidden")

@router.get("", response_model=List[UserOut])
def list_users(request: Request, _=Depends(require_admin)):
    store = _get_store(request)
    return [{k: v for k, v in u.items() if k != "password"} for u in store.values()]

@router.get("/{user_id}", response_model=UserOut)
def get_user(user_id: str, request: Request, _=Depends(require_self_or_admin)):
    store = _get_store(request)
    u = store.get(user_id)
    if not u:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")
    return {k: v for k, v in u.items() if k != "password"}