from pydantic import BaseModel


class RoleBase(BaseModel):
    name: str


class UserOut(BaseModel):
    username: str
    first_name: str
    last_name: str
    is_active: bool
    role: RoleBase
