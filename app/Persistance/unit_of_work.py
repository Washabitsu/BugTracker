from app.Persistance.Repositories.user_repository import UserRepository
from app.Persistance.Repositories.project_repository import ProjectRepository
from app.Persistance.Repositories.bug_repository import BugRepository
from sqlalchemy.ext.asyncio import AsyncSession
class UnitOfWork:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.user_repository = UserRepository(session)
        self.project_repository = ProjectRepository(session)
        self.bug_repository = BugRepository(session)
        self.new_objects = []
        self.dirty_objects = []
        self.deleted_objects = []

    async def add(self, obj):
        self.new_objects.append(obj)

    async def mark_dirty(self, obj):
        self.dirty_objects.append(obj)

    async def mark_deleted(self, obj):
        self.deleted_objects.append(obj)

    async def commit(self):
        for obj in self.new_objects:
            self.session.add(obj)

        for obj in self.dirty_objects:
            self.session.add(obj)

        for obj in self.deleted_objects:
            self.session.delete(obj)

        await self.session.commit()
