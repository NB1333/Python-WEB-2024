from pydantic import BaseModel, Field

class AccountCreate(BaseModel):
    user_id: int

class Account(BaseModel):
    id: int
    balance: float
    class Config:
        orm_mode = True

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    username: str | None = Field(None, description="New username for the user")

class User(UserBase):
    id: int
    is_admin: bool
    accounts: list[Account] = []

    class Config:
        orm_mode = True

class TransactionBase(BaseModel):
    amount: float

class TransactionCreate(TransactionBase):
    account_id: int

class Transaction(TransactionBase):
    id: int
    account: Account

    class Config:
        orm_mode = True
