from pydantic import BaseModel


class OrganizationOut(BaseModel):
    # id: int
    name: str
    phones: list[str]
    # building_id: int

    class Config:
        from_attributes = True


class OrganizationActivityOut(BaseModel):
    organization: str
    activity: str
    phones: list[str] | None
