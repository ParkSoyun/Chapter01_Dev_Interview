# Dev_Interview

---

## Get Start

- pycharm에서 flask, pymongo, python-dotenv 설치
- .env, .gitignore 파일 생성
- app.py 파일 run

## Dev_Interview란

- 개발자 면접 질문에 대한 답변을 서로 공유하고 이를 토대로 기술면접을 성공적으로 준비할 수 있게 해주는 서비스입니다. 

## Dev_Interview 구현 목록

### 회원가입
- 이름
- 아이디
    - 이메일 형식인지 확인
- 비밀번호
    - 특수문자, 영어, 숫자 중 2개 이상
- 비밀번호 확인
    - 비밀번호란과 동일한지 확인
- 관심 분야 카테고리 (선택사항)
### 로그인
- 아이디
    - 공란이 아닌지 확인
    - 이메일 형식인지 확인
- 비밀번호
    - 공란이 아닌지 확인
### PW 찾기
- 이름, 아이디
    - 해당 회원이 존재하고 정보가 일치하면 새 비밀번호 설정 페이지로
- 새 비밀번호 설정
### 메인페이지
- 질문
    - 다음 버튼으로 다른 질문을 볼 수 있음.
- 답변 작성 및 등록
    - 등록이 되어야만 다른 사람 답변 조회 가능
    - 답변 수정
    - 좋아요 기능
- 답변 정렬
    - 좋아요순 (Default)
    - 최신순
- 추후 고려사항
    - 저장하기 기능
    - 질문 등록
### 마이페이지
- 내 정보 수정
    - 비밀번호 다시 한 번 확인 후 맞는 경우 수정 페이지로
    - 아이디는 변경 불가
- 내 답변 모아보기
    - 카드 형태로 질문 및 답변 출력
    - 클릭 시 상세 보기 모달창
- 내 답변 상세보기
    - 답변 수정 기능