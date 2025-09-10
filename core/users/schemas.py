import re
from datetime import datetime
from pydantic import (
    BaseModel,
    Field,
    field_validator,
    model_validator
)


class UserBaseSchema(BaseModel):
    username: str = Field(
        ...,
        max_length=255,
        min_length=5,
        description="Username of the user"
    )
    password: str = Field(
        ...,
        max_length=50,
        min_length=8,
        description="Password of the user"
    )
    
class UserLoginSchema(UserBaseSchema):
    pass


class UserRegisterSchema(UserBaseSchema):
    password_confirm: str = Field(
        ...,
        max_length=50,
        min_length=8,
        description="Password confirmation of the user"
    )
    
    @field_validator("username")
    def no_spaces(cls, value):
        if " " in value:
            raise ValueError("Username cannot contain spaces")
        return value
    
    @field_validator("password")
    def strong_password(cls, value):

        # At least one lowercase letter in password
        if not re.search(r"[a-z]", value):
            raise ValueError("Password must contain at least one lowercase letter")

        # At least one uppercase letter in password
        if not re.search(r"[A-Z]", value):
            raise ValueError("Password must contain at least one uppercase letter")

        # At least one digit in password
        if not re.search(r"\d", value):
            raise ValueError("Password must contain at least one digit")

        # At least one special letter in password
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", value):
            raise ValueError("Password must contain at least one special character")
        return value
    
    @model_validator(mode="after")
    def check_passwords_match(self):
        if self.password != self.password_confirm:
            raise ValueError("Passwords do not match")
        return self
    