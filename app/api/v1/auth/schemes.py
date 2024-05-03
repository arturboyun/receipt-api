from pydantic import BaseModel, field_validator, Field


class TokenDataSchema(BaseModel):
    username: str | None = None


class TokenPairSchema(BaseModel):
    access_token: str
    refresh_token: str


class AccessTokenSchema(BaseModel):
    access_token: str


class UserCreateSchema(BaseModel):
    username: str
    password: str = Field(min_length=8, max_length=32)
    name: str

    @field_validator("username")
    def username_validation(cls, v):
        """Check if username contains only symbols and _- symbols"""
        if not v.isalnum():
            raise ValueError("Username should contain only letters and digits")
        if not v.isascii():
            raise ValueError("Username should contain only ascii symbols")
        if not v.islower():
            raise ValueError("Username should contain only lowercase symbols")
        return v

    @field_validator("password")
    def password_validation(cls, v):
        """Check if password contains at least one lowercase, uppercase letter and digit"""
        if not any(char.islower() for char in v):
            raise ValueError("Password should contain at least one lowercase letter")
        if not any(char.isupper() for char in v):
            raise ValueError("Password should contain at least one uppercase letter")
        if not any(char.isdigit() for char in v):
            raise ValueError("Password should contain at least one digit")
        return v

    @field_validator("name")
    def name_validation(cls, v):
        """Check if name contains only letters and spaces"""
        if not v.replace(" ", "").isalpha():
            raise ValueError("Name should contain only letters and spaces")
        return v


class UserSchema(BaseModel):
    username: str
    name: str
