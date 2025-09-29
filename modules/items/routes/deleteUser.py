from fastapi import APIRouter, Depends, HTTPException, status, Request, Header
from typing import Optional

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

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: str, request: Request, _=Depends(require_admin)):
    store = _get_store(request)
    if user_id not in store:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")
    del store[user_id]
    return None