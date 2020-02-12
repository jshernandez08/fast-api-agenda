from typing import List
from bson import ObjectId
from .utils import _get_paginator
from ..core.config import database_name, contacts_collection_name
from ..db.mongodb import AsyncIOMotorClient
from ..schemas.contact import ContactCreate, ContactInDb, ContactUpdate


async def get_contact(
    conn: AsyncIOMotorClient, _id: str
) -> ContactInDb:
    contact_db = await conn[database_name][contacts_collection_name].find_one({
        '_id': ObjectId(_id)
    })

    if not contact_db:
        return None

    return ContactInDb(**contact_db)


async def get_contacts(
    conn: AsyncIOMotorClient,
    page: int = 1,
    per_page: int = 12
) -> List[ContactInDb]:
    contacts: List[ContactInDb] = []
    start, limit = _get_paginator(page, per_page)
    contacts_db = conn[database_name][contacts_collection_name].find(
        {}, skip=start, limit=limit
    )

    async for row in contacts_db:
        contacts.append(ContactInDb(**row))

    return contacts


async def create_contact(
    conn: AsyncIOMotorClient,
    contact: ContactCreate
) -> ContactInDb:
    contact_data = contact.dict()
    await conn[database_name][contacts_collection_name].insert_one(contact_data)
    return ContactInDb(**contact_data)


async def on_update_contact(
    conn: AsyncIOMotorClient,
    _id: str,
    contact: ContactUpdate,
    contact_db: ContactInDb
) -> ContactInDb:
    contact_data_update = contact.dict()
    contact_db = contact_db.dict()

    # update contact db data
    for field in contact_data_update.keys():
        if contact_data_update.get(field):
            contact_db[field] = contact_data_update[field]

    await conn[database_name][contacts_collection_name].replace_one({
        '_id': ObjectId(_id)
    }, contact_db)
    return ContactInDb(**contact_db)


async def delete_contact(
    conn: AsyncIOMotorClient, _id: str
):
    await conn[database_name][contacts_collection_name].delete_many({
        '_id': ObjectId(_id)
    })