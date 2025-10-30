from pydantic import BaseModel, Field
from datetime import datetime


class ProgressBase(BaseModel):
    user_id: str = Field(..., title='ID del usuario', max_length=100)
    topic_id: str = Field(..., title='ID del tema', max_length=100)
    status: str = Field(..., title='Estado del progreso', max_length=50)
    notes: str = Field(default='', title='Notas adicionales', max_length=500)


class ProgressCreate(ProgressBase):
    pass


class ProgressUpdate(BaseModel):
    status: str | None = Field(
        None, title='Estado del progreso', max_length=50)
    notes: str | None = Field(None, title='Notas adicionales', max_length=500)


class ProgressResponse(ProgressBase):
    id: str = Field(..., title='ID del progreso')
    created_at: datetime = Field(..., title='Fecha de creación')
    updated_at: datetime = Field(..., title='Última actualización')

    class Config:
        orm_mode = True
