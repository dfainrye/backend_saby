from pydantic import BaseModel, Field, ConfigDict


class ServiceCreate(BaseModel):
    categoryId: int = Field(gt=0)
    title: str = Field(min_length=1, max_length=100)
    desc: str = Field(min_length=1, max_length=100)
    duration: int = Field(ge=30, le=180)
    price: float = Field(gt=0)


class ServiceResponse(BaseModel):
    id: int
    category_id: int
    title: str
    desc: str
    duration: int
    price: float

    model_config = ConfigDict(from_attributes=True)
