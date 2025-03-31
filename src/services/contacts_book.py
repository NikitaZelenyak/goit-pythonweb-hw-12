from sqlalchemy.ext.asyncio import AsyncSession

from src.entity.models import User
from src.repository.contacts_book import ContactBookRepository
from src.schemas.contact_book import ContactBookSchema, ContactBookUpdateSchema , ContactBookResponse


class ContactBookService:
    def __init__(self, db: AsyncSession):
        self.todo_repository = ContactBookRepository(db)

    async def create_contact(self, body: ContactBookSchema, user: User):
        return await self.todo_repository.create_contact(body, user)

    async def get_contacts(self, limit: int, offset: int, user: User):
        return await self.todo_repository.get_contact(limit, offset, user)

    async def get_contact(self, contact_id: int, user: User):
        return await self.todo_repository.get_contact_by_id(contact_id, user)

    async def update_contact(self, contact_id: int, body: ContactBookUpdateSchema, user: User):
        return await self.todo_repository.update_contact(contact_id, body, user)


    async def remove_contact(self, contact_id: int, user: User):
        return await self.todo_repository.remove_contact(contact_id, user)
