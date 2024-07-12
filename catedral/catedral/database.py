from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine


engine = create_async_engine('postgresql+psycopg://local_user:local_password@dbpilar:5432/local_db')

async def get_session():
    async with AsyncSession(engine) as session:
        yield session