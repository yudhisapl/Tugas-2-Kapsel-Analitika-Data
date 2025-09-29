from datetime import datetime, timezone
from typing import Optional, Literal
from pydantic import BaseModel, Field, EmailStr, ConfigDict, field_validator
import re

ROLE = Literal["admin", "staff"]

_username_re = re.compile(r"^[a-z0-9]{6,15}$")
_password_allowed_re = re.compile(r"^[A-Za-z0-9!@]{8,20}$")
_password_has_upper = re.compile(r"[A-Z]")
_password_has_lower = re.compile(r"[a-z]")
_password_has_digit = re.compile(r"[0-9]")
_password_has_special = re.compile(r"[!@]")

class UserBase(BaseModel):
    username: str = Field(..., description="lowercase alphanumeric, 6-15 chars")
    email: EmailStr
    role: ROLE = "staff"

    # request body strict
    model_config = ConfigDict(extra="forbid")

    @field_validator("username")
    @classmethod
    def validate_username(cls, v: str) -> str:
        if not _username_re.fullmatch(v):
            raise ValueError("username must be lowercase alphanumeric, length 6-15")
        return v

class UserCreate(UserBase):
    password: str = Field(
        ..., description="8-20 chars, alnum + !@, with min 1 upper, 1 lower, 1 digit, 1 special"
    )

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        if not _password_allowed_re.fullmatch(v):
            raise ValueError("password must be 8-20 chars and only contain letters, digits, ! or @")
        if not _password_has_upper.search(v):
            raise ValueError("password must include at least one uppercase letter")
        if not _password_has_lower.search(v):
            raise ValueError("password must include at least one lowercase letter")
        if not _password_has_digit.search(v):
            raise ValueError("password must include at least one digit")
        if not _password_has_special.search(v):
            raise ValueError("password must include at least one of: ! or @")
        return v

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[ROLE] = None
    password: Optional[str] = None

    model_config = ConfigDict(extra="forbid")

    @field_validator("username")
    @classmethod
    def validate_username(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        if not _username_re.fullmatch(v):
            raise ValueError("username must be lowercase alphanumeric, length 6-15")
        return v

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        if not _password_allowed_re.fullmatch(v):
            raise ValueError("password must be 8-20 chars and only contain letters, digits, ! or @")
        if not _password_has_upper.search(v):
            raise ValueError("password must include at least one uppercase letter")
        if not _password_has_lower.search(v):
            raise ValueError("password must include at least one lowercase letter")
        if not _password_has_digit.search(v):
            raise ValueError("password must include at least one digit")
        if not _password_has_special.search(v):
            raise ValueError("password must include at least one of: ! or @")
        return v

class UserOut(BaseModel):
    id: str
    username: str
    email: EmailStr
    role: ROLE
    created_at: datetime
    updated_at: datetime