from fastapi import (
    FastAPI,
    Depends,
    HTTPException,
    File,
    UploadFile,
    Form,
)
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models
import crud
from schemas import (
    UserRead,
    MentoringStatusRead,
    UserMentoringData,
    TaskData,
)
from typing import List
import os
import shutil

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# 의존성 주입: 데이터베이스 세션
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 이미지 저장 함수
async def save_image(image: UploadFile):
    upload_dir = 'uploads/images'
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
    image_path = os.path.join(upload_dir, image.filename)
    with open(image_path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)
    image_url = f"/static/images/{image.filename}"
    return image_url


# API 엔드포인트 구현

# 커뮤니티 유저 목록 불러오기
@app.get("/community/users", response_model=List[UserRead])
def get_community_users(db: Session = Depends(get_db)):
    users = crud.get_community_users(db)
    return users


# 멘토링 상태 정보 불러오기
@app.get("/mentoring/status/{user_id}", response_model=List[MentoringStatusRead])
def get_mentoring_status(user_id: int, db: Session = Depends(get_db)):
    mentoring_status = crud.get_mentoring_status(user_id, db)
    if mentoring_status is None:
        raise HTTPException(status_code=404, detail="User not found")
    return mentoring_status


# 멘토링 요청 보내기
@app.post("/mentoring/request")
def send_mentoring_request(
    requester_id: int = Form(...),
    receiver_id: int = Form(...),
    db: Session = Depends(get_db),
):
    existing_request = (
        db.query(models.MentoringStatus)
        .filter_by(requester_id=requester_id, receiver_id=receiver_id)
        .first()
    )
    if existing_request:
        raise HTTPException(status_code=400, detail="이미 요청이 존재합니다.")
    mentoring_request = models.MentoringStatus(
        requester_id=requester_id,
        receiver_id=receiver_id,
        status=models.MentoringStatusEnum.requesting,
    )
    db.add(mentoring_request)
    db.commit()
    db.refresh(mentoring_request)
    return {"message": "멘토링 요청을 보냈습니다."}


# 멘토링 요청 수락하기
@app.post("/mentoring/accept")
def accept_mentoring_request(
    requester_id: int = Form(...),
    receiver_id: int = Form(...),
    db: Session = Depends(get_db),
):
    mentoring_request = (
        db.query(models.MentoringStatus)
        .filter_by(requester_id=requester_id, receiver_id=receiver_id)
        .first()
    )
    if not mentoring_request:
        raise HTTPException(status_code=404, detail="멘토링 요청을 찾을 수 없습니다.")
    mentoring_request.status = models.MentoringStatusEnum.accepted

    # 멘토십 관계 생성
    mentorship = models.Mentorship(
        mentor_id=receiver_id,
        mentee_id=requester_id,
    )
    db.add(mentorship)

    db.commit()
    return {"message": "멘토링 요청을 수락했습니다."}


# 멘토링 요청 거절하기
@app.post("/mentoring/reject")
def reject_mentoring_request(
    requester_id: int = Form(...),
    receiver_id: int = Form(...),
    db: Session = Depends(get_db),
):
    mentoring_request = (
        db.query(models.MentoringStatus)
        .filter_by(requester_id=requester_id, receiver_id=receiver_id)
        .first()
    )
    if not mentoring_request:
        raise HTTPException(status_code=404, detail="멘토링 요청을 찾을 수 없습니다.")
    mentoring_request.status = models.MentoringStatusEnum.rejected
    db.commit()
    return {"message": "멘토링 요청을 거절했습니다."}


# 프로필 데이터 불러오기
@app.get("/profile/{user_id}", response_model=UserRead)
def get_profile(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_profile(user_id, db)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# 멘토/멘티 불러오기
@app.get("/mentoring/users/{user_id}", response_model=List[UserMentoringData])
def get_user_mentoring_data(user_id: int, db: Session = Depends(get_db)):
    data = crud.get_user_mentoring_data(user_id, db)
    if data is None:
        raise HTTPException(status_code=404, detail="User not found")
    return data


# 유저 과제 목록 불러오기
@app.get("/user/{user_id}/tasks", response_model=List[TaskData])
def get_user_tasks(user_id: int, db: Session = Depends(get_db)):
    tasks = crud.get_user_tasks(user_id, db)
    if tasks is None:
        raise HTTPException(status_code=404, detail="User not found")
    return tasks


# 기업이 과제 등록
@app.post("/company/{company_id}/tasks")
async def create_task_for_company(
    company_id: int,
    title: str = Form(...),
    description: str = Form(...),
    image: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    company = db.query(models.Company).get(company_id)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    image_url = await save_image(image)
    task = models.Task(
        title=title,
        description=description,
        image=image_url,
        company_id=company_id,
        badge_type=models.TaskBadgeTypeEnum.Normal,
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return {"message": "과제가 등록되었습니다.", "task_id": task.id}
