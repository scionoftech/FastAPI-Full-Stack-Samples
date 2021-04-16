from pydantic import BaseModel


# Request body classes
class RedisRq(BaseModel):
    range_value: int
