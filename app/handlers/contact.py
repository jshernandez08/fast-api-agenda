from typing import List
from bson import ObjectId
from ..core.config import database_name, contacts_collection_name
from ..schemas.contact import ContactCreate, ContactInDb, ContactUpdate
from ..db.mongodb import AsyncIOMotorClient, get_database
from ..models.contact import (
    get_contact, get_contacts, create_contact,
    on_update_contact, delete_contact
)
from starlette.exceptions import HTTPException
from starlette.status import (
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_422_UNPROCESSABLE_ENTITY,
)
from fastapi import APIRouter, Depends, Query, Path

router = APIRouter()

@router.get("/contacts/", response_model=List[ContactInDb], tags=["contacts"])
async def read_contacts(
    page: int = Query(1, ge=1),
    per_page: int = Query(12, gt=0),
    db: AsyncIOMotorClient = Depends(get_database)
):
    contacts_db = await get_contacts(db, page, per_page)
    return contacts_db


@router.get("/contacts/{_id}", response_model=ContactInDb, tags=["contacts"])
async def read_contact(
    _id: str = Path(..., regex="^[a-fA-F0-9]{24}$"),
    db: AsyncIOMotorClient = Depends(get_database)
):
    contact_db = await get_contact(db, _id)

    # check if get contact
    if not contact_db:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=f"Contact not found",
        )

    return contact_db


@router.post("/contacts", response_model=ContactInDb, tags=["contacts"])
async def create_new_contact(
    contact: ContactCreate,
    db: AsyncIOMotorClient = Depends(get_database)
):
    new_contact = await create_contact(db, contact)
    return new_contact


@router.post("/contacts/{_id}", response_model=ContactInDb, tags=["contacts"])
async def update_contact(
    *,
    _id: str = Path(..., regex="^[a-fA-F0-9]{24}$"),
    db: AsyncIOMotorClient = Depends(get_database),
    contact: ContactUpdate
):
    # check if exists contact
    contact_db = await get_contact(db, _id)
    if not contact_db:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=f"Contact not found",
        )

    updated_contact = await on_update_contact(db, _id, contact, contact_db)
    return updated_contact


@router.delete("/contacts/{_id}", tags=["contacts"])
async def remove_contact(
    _id: str = Path(..., regex="^[a-fA-F0-9]{24}$"),
    db: AsyncIOMotorClient = Depends(get_database)
):
    # check if exists contact
    contact_db = await get_contact(db, _id)
    if not contact_db:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=f"Contact not found",
        )

    await delete_contact(db, _id)