from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate

class UserService:

    async def get_by_id(
            self, db: AsyncSession, user_id: int
    ) -> User | None:
        result = await db.execute(
            select(User).where(User.id == user_id)
        )
        
        return result.scalar_one_or_none()

    async def get_by_email(
            self, db: AsyncSession, email: str
    ) -> User | None:
        result = await db.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()


    async def get_all(
            self, db: AsyncSession
    ) -> list[User]:

        result = await db.execute(select(User))
        return list(result.scalars().all())
    async def create(
            self, db: AsyncSession, data: UserCreate
    ) -> User:
        
        # Check existing email
        existing = await self.get_by_email(db, data.email)
        if existing:
            raise ValueError("This email is already used")
        
        user = User(
            name=data.name,
            email=data.email,
            hashed_password=data.password,
        )

        db.add(user)
        await db.flush() # get id without commit
        return user
    
    async def update(
            self, db: AsyncSession, user_id: int, data: UserUpdate
    ) -> User:
        user = await self.get_by_id(db, user_id)
        if not user:
            raise ValueError(f"{user_id} not found")
        
        # update only fields that've been submitted
        update_data = data.model_dump(exclude_none=True)
        for field, value in update_data.items():
            setattr(user, field, value)

        return user
    
    async def delete(
            self, db: AsyncSession, user_id: int
    ) -> None:
        user = await self.get_by_id(db, user_id)
        if not user:
            raise ValueError(f"{user_id} is not found")
        await db.delete(user)

user_service = UserService()