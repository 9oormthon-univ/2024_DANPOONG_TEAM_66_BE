from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Enum,
    Table,
)
from sqlalchemy.orm import relationship
from database import Base
import enum


class BadgeTypeEnum(enum.Enum):
    Green = 'Green'
    Yellow = 'Yellow'
    Orange = 'Orange'
    Red = 'Red'


class TaskBadgeTypeEnum(enum.Enum):
    Normal = 'Normal'
    Gold = 'Gold'
    Silver = 'Silver'
    Bronze = 'Bronze'


class MentoringStatusEnum(enum.Enum):
    requesting = '요청중'
    requested = '요청받음'
    accepted = '수락됨'
    rejected = '거절됨'


class Interest(Base):
    __tablename__ = 'interests'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True)


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    email = Column(String(50))
    profile = Column(String(255))  # 프로필 이미지 URL
    interest_id = Column(Integer, ForeignKey('interests.id'))
    interest = relationship('Interest')
    badges = relationship('UserBadge', back_populates='user')
    mentoring_requests_sent = relationship(
        'MentoringStatus',
        back_populates='requester',
        foreign_keys='MentoringStatus.requester_id',
    )
    mentoring_requests_received = relationship(
        'MentoringStatus',
        back_populates='receiver',
        foreign_keys='MentoringStatus.receiver_id',
    )
    tasks = relationship(
        'Task', secondary='user_tasks', back_populates='users'
    )

    # 멘토와 멘티 관계
    mentors = relationship(
        'Mentorship',
        foreign_keys='Mentorship.mentee_id',
        back_populates='mentee',
        cascade='all, delete-orphan'
    )
    mentees = relationship(
        'Mentorship',
        foreign_keys='Mentorship.mentor_id',
        back_populates='mentor',
        cascade='all, delete-orphan'
    )


class UserBadge(Base):
    __tablename__ = 'user_badges'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    badge_type = Column(Enum(BadgeTypeEnum))
    count = Column(Integer)
    user = relationship('User', back_populates='badges')


class MentoringStatus(Base):
    __tablename__ = 'mentoring_statuses'
    id = Column(Integer, primary_key=True)
    requester_id = Column(Integer, ForeignKey('users.id'))
    receiver_id = Column(Integer, ForeignKey('users.id'))
    status = Column(Enum(MentoringStatusEnum))
    requester = relationship(
        'User',
        back_populates='mentoring_requests_sent',
        foreign_keys=[requester_id],
    )
    receiver = relationship(
        'User',
        back_populates='mentoring_requests_received',
        foreign_keys=[receiver_id],
    )


class Mentorship(Base):
    __tablename__ = 'mentorships'
    id = Column(Integer, primary_key=True)
    mentor_id = Column(Integer, ForeignKey('users.id'))
    mentee_id = Column(Integer, ForeignKey('users.id'))
    mentor = relationship(
        'User',
        foreign_keys=[mentor_id],
        back_populates='mentees'
    )
    mentee = relationship(
        'User',
        foreign_keys=[mentee_id],
        back_populates='mentors'
    )


class Company(Base):
    __tablename__ = 'companies'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    tasks = relationship('Task', back_populates='company')


class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True)
    image = Column(String(255))
    company_id = Column(Integer, ForeignKey('companies.id'))
    title = Column(String(100))
    description = Column(String(255))
    badge_type = Column(Enum(TaskBadgeTypeEnum))
    company = relationship('Company', back_populates='tasks')
    users = relationship(
        'User', secondary='user_tasks', back_populates='tasks'
    )


user_tasks = Table(
    'user_tasks',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('task_id', Integer, ForeignKey('tasks.id')),
)
