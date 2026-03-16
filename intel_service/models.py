from pydantic import BaseModel, field_validator


class IntelSignal(BaseModel):
    timestamp: str
    signal_id: str
    entity_id: str
    reported_lat: str
    reported_lon: str
    signal_type: str
    priority_level: int

    @field_validator("priority_level")
    @classmethod
    def priority_valid(cls, validation: int):
        if validation not in range(1, 6) and validation != 99:
            raise ValueError("priority level not in 1-5 or 99")
        return validation
