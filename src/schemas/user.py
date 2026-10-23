from datetime import datetime
from pydantic import BaseModel, EmailStr, ConfigDict


class UserOut(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    user_id: int
    username: str
    email: EmailStr
    role_id: int
