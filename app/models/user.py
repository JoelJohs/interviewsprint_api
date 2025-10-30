from pydantic import BaseModel, Field, EmailStr


class UserBase(BaseModel):
    username: str = Field(..., title='Nombre de usuario', max_length=50)
    email: EmailStr = Field(..., title='Correo electrónico del usuario')
    is_active: bool = Field(default=True, title='Estado activo del usuario')


class UserCreate(UserBase):
    password: str = Field(..., title='Contraseña del usuario', min_length=8)


class UserResponse(UserBase):
    id: str = Field(..., title='ID del usuario')

    class Config:
        orm_mode = True
