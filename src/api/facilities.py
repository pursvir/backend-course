from fastapi import APIRouter
from fastapi_cache.decorator import cache

from src.api.dependencies import DBDep
from src.exceptions import FacilityAlreadyExistsException, FacilityAlreadyExistsHTTPException
from src.schemas.facilities import FacilityAdd
from src.services.facilities import FacilitiesService

router = APIRouter(prefix="/facilities", tags=["Удобства"])


@router.get("")
@cache(expire=10)
async def get_facilities(db: DBDep):
    return await FacilitiesService(db).get_all_facilities()


@router.post("")
async def add_facility(db: DBDep, facility_data: FacilityAdd):
    try:
        new_facility_data = await FacilitiesService(db).add_facility(facility_data)
    except FacilityAlreadyExistsException:
        raise FacilityAlreadyExistsHTTPException
    return {"status": "OK", "data": new_facility_data}
