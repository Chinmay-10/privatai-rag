from pydantic import BaseModel


class TenantOut(BaseModel):
    id: str
    name: str
