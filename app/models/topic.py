from pydantic import BaseModel, Field, field_validator


class TopicBase(BaseModel):
    title: str = Field(..., title='Titulo del tema', max_length=100)
    category_id: str = Field(..., title='ID de la categoria',
                             max_length=50, pattern=r'^[a-z0-9-]+$')
    details: list[str] = Field(..., title='Detalles del tema', min_length=1)

    @field_validator('details')
    def validate_details_not_empty(cls, v):
        if not v or all(not item.strip() for item in v):
            raise ValueError(
                'Details debe contener al menos un elemento válido')
        return v


class TopicCreate(TopicBase):
    pass


class TopicResponse(TopicBase):
    id: str = Field(..., title='ID del tema', examples=['js-tipos-de-datos'])

    class Config:
        orm_mode = True
