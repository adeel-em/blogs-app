from typing import Any
from sqlalchemy import select

from fastapi import APIRouter, Depends, HTTPException


class Base():
    async def save(self, db_session):
        """
        Save the object to the database.
        """
        db_session.add(self)
        db_session.commit()
        db_session.refresh(self)
        return self
    
    @classmethod
    async def get_by_id(cls, db_session, id: int):
        query = select().where(cls.id == id).first()
        result = await db_session.execute(query)
        return result.scalar().first()
