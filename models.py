from sqlalchemy import Column, Integer, String, Enum
from database import Base
import enum

class BadgeTypeEnum(str, enum.Enum):
    Normal = "Normal"
    Gold = "Gold"
    Silver = "Silver"
    Bronze = "Bronze"

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    image = Column(String(255), nullable=False)
    company = Column(String(100), nullable=False)
    title = Column(String(100), nullable=False)
    description = Column(String, nullable=False)
    badgeType = Column(Enum(BadgeTypeEnum), nullable=False)
