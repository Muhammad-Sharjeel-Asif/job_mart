from typing import Annotated

from fastapi import Depends, Query


def pagination(
    skip: int = Query(0, ge=0), limit: int = Query(10, ge=0, le=100)
) -> dict[str, int]:
    return {"skip": skip, "limit": limit}


PaginationDep = Annotated[dict, Depends(pagination)]
