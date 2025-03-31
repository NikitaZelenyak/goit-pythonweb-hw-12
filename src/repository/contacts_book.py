import logging
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.entity.models import Contact_Book, User
from src.schemas.contact_book import ContactBookSchema, ContactBookUpdateSchema, ContactBookResponse

logger = logging.getLogger("uvicorn.error")


class ContactBookRepository:
    def __init__(self, session: AsyncSession):
        self.db = session

    async def get_contact(self, limit: int, offset: int, user: User) -> Sequence[Contact_Book]:
        stmt = select(Contact_Book).filter_by(user_id = user.id).offset(offset).limit(limit)
        contact = await self.db.execute(stmt)
        return contact.scalars().all()

    async def get_contact_by_id(self, contact_id: int, user: User) -> Contact_Book | None:
        stmt = select(Contact_Book).filter_by(id=contact_id, user_id = user.id)
        contact = await self.db.execute(stmt)
        return contact.scalar_one_or_none()

    async def create_contact(self, body: ContactBookSchema, user: User) -> Contact_Book:
        contact = Contact_Book(**body.model_dump(), user=user)
        self.db.add(contact)
        await self.db.commit()
        await self.db.refresh(contact)
        return contact

    async def remove_contact(self, contact_id: int ,user: User) -> Contact_Book | None:
        contact = await self.get_contact_by_id(contact_id, user)
        if contact:
            await self.db.delete(contact)
            await self.db.commit()
        return contact

    async def update_contact(
            self, contact_id: int, body: ContactBookUpdateSchema,user: User
    ) -> Contact_Book:
        contact = await self.get_contact_by_id(contact_id, user)
        if contact:
            update_data = body.model_dump(exclude_unset=True)

            for key, value in update_data.items():
                setattr(contact, key, value)

            await self.db.commit()
            await self.db.refresh(contact)

        return contact
