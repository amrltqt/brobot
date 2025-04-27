from typing import Annotated
from pydantic import BaseModel, HttpUrl, StringConstraints


class ImportRequestDTO(BaseModel):
    slug: Annotated[
        str,
        StringConstraints(strip_whitespace=True, pattern=r"^[A-Za-z-]+$"),
    ]
    url: HttpUrl
