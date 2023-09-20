from fastapi import APIRouter, HTTPException, Query
from typing import List
from models.owner import Owner, OwnerUpdate

owner_router = APIRouter()


@owner_router.post("/create_owner/", response_model=Owner)
async def create_owner(owner: Owner):
    created_owner = Owner(**owner.dict())
    await created_owner.insert()
    return created_owner


@owner_router.patch("/update_owner/v/{owner_id}", response_model=Owner)
async def update_owner(owner_id: str, owner: OwnerUpdate):
    existing_owner = await Owner.get(owner_id)
    if not existing_owner or (not existing_owner.is_active and not 'is_active' in owner.dict()):
        raise HTTPException(status_code=404, detail="Owner not found")
    update_query = {"$set": owner.dict(exclude_unset=True)}
    await existing_owner.update(update_query)
    return existing_owner


@owner_router.post("/deactivate_owner/v/{owner_id}")
async def deactivating_owner(owner_id: str):
    deactivated_owner = await Owner.get(owner_id)
    if not deactivated_owner or not deactivated_owner.is_active:
        raise HTTPException(status_code=404, detail="Owner not found")
    update_query = {"$set": {"is_active": False}}
    await deactivated_owner.update(update_query)
    return {"message": "The account has been deactivated successfully."}


@owner_router.get("/get_owner/v/{owner_id}", response_model=Owner)
async def owner_detail(owner_id: str):
    owner_detail = await Owner.get(owner_id)
    if not owner_detail or not owner_detail.is_active:
        raise HTTPException(status_code=404, detail="Owner not found")
    return owner_detail


@owner_router.get("/get_owners/", response_model=List[Owner])
async def get_owners():
    owners = await Owner.all().to_list()
    return owners
