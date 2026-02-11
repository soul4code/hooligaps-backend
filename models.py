import uuid6
from sqlalchemy import Uuid, Date, Column, String, Index
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import declarative_base, Mapped, mapped_column

Base = declarative_base(cls=AsyncAttrs)


class History(Base):
    __tablename__ = 'hooligaps_history'

    id: Mapped[uuid6.UUID] = mapped_column(Uuid, primary_key=True, default=uuid6.uuid7)

    date = Column(Date, nullable=False, index=True)
    first_name = Column(String(150), nullable=False, index=True)
    last_name = Column(String(150), nullable=False, index=True)

    __table_args__ = (Index('idx_name', 'first_name', 'last_name'),)

    def __repr__(self):
        return (
            f'<History(date={self.date}, first_name={self.first_name}, last_name={self.last_name})>'
        )
