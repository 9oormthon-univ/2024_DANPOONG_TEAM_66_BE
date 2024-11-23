#!/bin/bash

# 서버 주소 설정
BASE_URL="http://13.124.201.233:57515"

echo "=== API 테스트 시작 ==="

# 1. 커뮤니티 유저 목록 불러오기
echo -e "\n1. 커뮤니티 유저 목록 불러오기"
curl -X GET "$BASE_URL/community/users"
echo -e "\n------------------------"

# 2. 멘토링 상태 정보 불러오기
echo -e "\n2. 멘토링 상태 정보 불러오기 (user_id=1)"
curl -X GET "$BASE_URL/mentoring/status/1"
echo -e "\n------------------------"

# 3. 멘토링 요청 보내기
echo -e "\n3. 멘토링 요청 보내기 (requester_id=1, receiver_id=2)"
curl -X POST "$BASE_URL/mentoring/request" \
     -F 'requester_id=1' \
     -F 'receiver_id=2'
echo -e "\n------------------------"

# 4. 멘토링 요청 수락하기
echo -e "\n4. 멘토링 요청 수락하기 (requester_id=1, receiver_id=2)"
curl -X POST "$BASE_URL/mentoring/accept" \
     -F 'requester_id=1' \
     -F 'receiver_id=2'
echo -e "\n------------------------"

# 5. 프로필 데이터 불러오기
echo -e "\n5. 프로필 데이터 불러오기 (user_id=1)"
curl -X GET "$BASE_URL/profile/1"
echo -e "\n------------------------"

# 6. 멘토/멘티 불러오기
echo -e "\n6. 멘토/멘티 불러오기 (user_id=1)"
curl -X GET "$BASE_URL/mentoring/users/1"
echo -e "\n------------------------"

# 7. 유저 과제 목록 불러오기
echo -e "\n7. 유저 과제 목록 불러오기 (user_id=1)"
curl -X GET "$BASE_URL/user/1/tasks"
echo -e "\n------------------------"

# 8. 기업이 과제 등록하기
# 실제 이미지 파일 경로를 지정해야 합니다.
IMAGE_PATH="https://avatars.githubusercontent.com/u/81866624?v=4"  # 이 부분을 실제 이미지 파일 경로로 수정하세요.

if [ -f "$IMAGE_PATH" ]; then
    echo -e "\n8. 기업이 과제 등록하기 (company_id=1)"
    curl -X POST "$BASE_URL/company/1/tasks" \
         -F 'title=데이터 분석 과제' \
         -F 'description=데이터 분석을 수행하는 과제입니다.' \
         -F "image=@${IMAGE_PATH}"
    echo -e "\n------------------------"
else
    echo -e "\n8. 기업이 과제 등록하기: 이미지 파일이 존재하지 않습니다. IMAGE_PATH를 확인하세요."
fi

echo "=== API 테스트 완료 ==="
