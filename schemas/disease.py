from pydantic import BaseModel

class DiseaseSchemaPost(BaseModel):
    name: str

class DiseaseSchemaGet(BaseModel):
    id: int
    name: str
