from sqlalchemy.orm import Session, joinedload
from models import (
    User,
    UserBadge,
    MentoringStatus,
    MentoringStatusEnum,
    Mentorship,
    Task,
    Company,
)
from schemas import (
    BadgeData,
    UserCreate,
    TaskData,
)
from typing import List


def get_community_users(db: Session):
    return (
        db.query(User)
        .options(joinedload(User.badges), joinedload(User.interest))
        .all()
    )


def get_mentoring_status(user_id: int, db: Session):
    user = db.query(User).get(user_id)
    if not user:
        return None

    mentoring_status = []

    # 요청중 (사용자가 보낸 요청)
    sent_requests = (
        db.query(MentoringStatus)
        .filter_by(requester_id=user_id, status=MentoringStatusEnum.requesting)
        .all()
    )
    for request in sent_requests:
        receiver = request.receiver
        status = {
            'id': receiver.id,
            'name': receiver.name,
            'interest': receiver.interest.name
            if receiver.interest
            else None,
            'status': '요청중',
            'badgeData': [
                {'badgeType': badge.badge_type, 'count': badge.count}
                for badge in receiver.badges
            ],
        }
        mentoring_status.append(status)

    # 요청받음 (사용자가 받은 요청)
    received_requests = (
        db.query(MentoringStatus)
        .filter_by(receiver_id=user_id, status=MentoringStatusEnum.requesting)
        .all()
    )
    for request in received_requests:
        requester = request.requester
        status = {
            'id': requester.id,
            'name': requester.name,
            'interest': requester.interest.name
            if requester.interest
            else None,
            'status': '요청받음',
            'badgeData': [
                {'badgeType': badge.badge_type, 'count': badge.count}
                for badge in requester.badges
            ],
        }
        mentoring_status.append(status)

    return mentoring_status


def get_profile(user_id: int, db: Session):
    user = (
        db.query(User)
        .options(joinedload(User.badges), joinedload(User.interest))
        .filter(User.id == user_id)
        .first()
    )
    return user


def get_user_mentoring_data(user_id: int, db: Session):
    user = db.query(User).get(user_id)
    if not user:
        return None

    results = []

    # 멘토 (내가 멘티인 경우)
    mentor_relations = db.query(Mentorship).filter_by(mentee_id=user_id).all()
    for relation in mentor_relations:
        mentor = relation.mentor
        data = {
            'id': mentor.id,
            'name': mentor.name,
            'mentoring': '멘토',
            'badgeData': [
                {'badgeType': badge.badge_type, 'count': badge.count}
                for badge in mentor.badges
            ],
            'email': mentor.email,
        }
        results.append(data)

    # 멘티 (내가 멘토인 경우)
    mentee_relations = db.query(Mentorship).filter_by(mentor_id=user_id).all()
    for relation in mentee_relations:
        mentee = relation.mentee
        data = {
            'id': mentee.id,
            'name': mentee.name,
            'mentoring': '멘티',
            'badgeData': [
                {'badgeType': badge.badge_type, 'count': badge.count}
                for badge in mentee.badges
            ],
            'email': mentee.email,
        }
        results.append(data)

    return results


def get_user_tasks(user_id: int, db: Session):
    user = db.query(User).get(user_id)
    if not user:
        return None
    tasks = user.tasks
    task_data_list = []
    for task in tasks:
        task_data = {
            'id': task.id,
            'image': task.image,
            'company': task.company.name,
            'title': task.title,
            'description': task.description,
            'badgeType': task.badge_type,
        }
        task_data_list.append(task_data)
    return task_data_list
