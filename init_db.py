import time
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models

# 데이터베이스 연결 시도
while True:
    try:
        # 데이터베이스에 연결 가능한지 테스트
        db = SessionLocal()
        db.execute('SELECT 1')
        break
    except Exception as e:
        print("데이터베이스에 연결할 수 없습니다. 5초 후 다시 시도합니다.")
        time.sleep(5)

# 기존 테이블 삭제 (데이터 손실에 주의)
models.Base.metadata.drop_all(bind=engine)

# 새로운 테이블 생성
models.Base.metadata.create_all(bind=engine)

db = SessionLocal()

# 관심 분야 생성
interests = ['마케팅', '프로그래밍', '경영']
for interest_name in interests:
    interest = models.Interest(name=interest_name)
    db.add(interest)
db.commit()

# 유저 생성
users_data = [
    {'name': '홍길동', 'email': 'hong@example.com', 'interest': '마케팅'},
    {'name': '김철수', 'email': 'kim@example.com', 'interest': '프로그래밍'},
    {'name': '이영희', 'email': 'lee@example.com', 'interest': '프로그래밍'},
    {'name': '박민수', 'email': 'park@example.com', 'interest': '경영'},
    {'name': '김미영', 'email': 'mi@example.com', 'interest': '경영'},
]

for user_data in users_data:
    interest = (
        db.query(models.Interest)
        .filter_by(name=user_data['interest'])
        .first()
    )
    user = models.User(
        name=user_data['name'],
        email=user_data['email'],
        interest=interest,
    )
    db.add(user)
db.commit()

# 뱃지 데이터 추가
badges_data = [
    {'user_name': '홍길동', 'badge_type': 'Green', 'count': 3},
    {'user_name': '홍길동', 'badge_type': 'Yellow', 'count': 2},
    {'user_name': '홍길동', 'badge_type': 'Red', 'count': 1},
    {'user_name': '김철수', 'badge_type': 'Green', 'count': 1},
    {'user_name': '이영희', 'badge_type': 'Green', 'count': 2},
    {'user_name': '이영희', 'badge_type': 'Yellow', 'count': 1},
    {'user_name': '이영희', 'badge_type': 'Orange', 'count': 1},
    {'user_name': '김미영', 'badge_type': 'Green', 'count': 1},
]

for badge_data in badges_data:
    user = (
        db.query(models.User)
        .filter_by(name=badge_data['user_name'])
        .first()
    )
    badge = models.UserBadge(
        user=user,
        badge_type=badge_data['badge_type'],
        count=badge_data['count'],
    )
    db.add(badge)
db.commit()

db.close()
