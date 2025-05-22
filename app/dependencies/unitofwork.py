from typing import Annotated

from fastapi import Depends

from app.abstractions.unitofwork import UnitOfWork

UOWDep = Annotated[UnitOfWork, Depends(UnitOfWork)]
