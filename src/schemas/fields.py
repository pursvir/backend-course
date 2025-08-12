from typing import Annotated

from pydantic import Field

pk = Annotated[int, Field(gt=0)]

str_not_null = Annotated[str, Field(min_length=1)]
