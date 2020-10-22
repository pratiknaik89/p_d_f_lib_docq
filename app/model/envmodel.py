
from pydantic import BaseModel
from typing import Optional
class EnvResp(BaseModel):
    AWS_ACCESS_KEY_ID: Optional[str] = None
    AWS_SECRET_ACCESS_KEY: Optional[str] = None
    AWS_SQS_REGION: Optional[str] = None
    AWS_SQS_URL: Optional[str] = None
    AWS_BUCKET_PREFIX: Optional[str] = None

    class Config:
        arbitrary_types_allowed = True