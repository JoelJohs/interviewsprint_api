from pydantic import BaseModel, Field
from typing import Optional


class TopicBase(BaseModel):
    title: str = Field(..., 'Titulo del tema', max_length=100)
    category_id: str = Field(..., 'ID de la categoria', max_length=50)
    details: list[str] = Field(default_factory=list, title='Detalles del tema')


class TopicCreate(TopicBase):
    pass


class TopicResponse(TopicBase):
    id: str = Field(..., title='ID del tema', examples=['js-tipos-de-datos'])

    class Config:
        orm_mode = True
