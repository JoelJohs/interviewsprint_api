from pydantic import BaseModel, Field
from datetime import datetime


class SessionRequest(BaseModel):
    user_id: str = Field(..., title='ID del usuario', max_length=100)
    topic_ids: list[str] = Field(..., title='IDs de los temas para la sesión')


class SessionItem(BaseModel):
    topic_id: str = Field(..., title='ID del tema', max_length=100)
    title: str = Field(..., title='Título del tema', max_length=200)
    category_id: str = Field(..., title='ID de la categoría', max_length=100)
    details: list[str] = Field(default_factory=list, title='Detalles del tema')


class SessionResponse(BaseModel):
    session_id: str = Field(..., title='ID de la sesión')
    user_id: str = Field(..., title='ID del usuario')
    created_at: datetime = Field(..., title='Fecha de creación')
    topics: list[SessionItem] = Field(
        default_factory=list, title='Temas de la sesión')

    class Config:
        orm_mode = True
