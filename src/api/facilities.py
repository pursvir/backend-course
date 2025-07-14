from fastapi import APIRouter
from fastapi_cache.decorator import cache

from src.api.dependencies import DBDep
from src.schemas.facilities import FacilityAdd


router = APIRouter(prefix="/facilities", tags=["Удобства"])


@router.get("")
@cache(expire=10)
async def get_facilities(db: DBDep):
    return await db.facilities.get_all()


@router.post("")
async def add_facility(db: DBDep, data: FacilityAdd):
    new_facility_data = await db.facilities.add(data)
    await db.commit()
    return {"status": "OK", "data": new_facility_data}
