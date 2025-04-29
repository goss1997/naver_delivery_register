# README.md
# 📦 naver_delivery_register

네이버 스마트스토어에 자동으로 택배사 정보를 등록해주는 FastAPI 기반 백엔드 서비스입니다.  
Selenium을 사용해 실제 스마트스토어 UI를 자동 조작하며, JSON 형식의 요청으로 등록 요청을 처리합니다.

---

## ✅ 기능 요약

- 네이버 스마트스토어 로그인 (셀러 계정)
- 택배사 계약정보 자동 입력 및 등록
- 발송지 정보 입력
- 계약 요금 입력
- FastAPI + Selenium 기반 자동화

---

## 🛠 프로젝트 구조

```
naver_delivery_register/
├── app/                 # FastAPI 엔트리 포인트
├── models/              # Pydantic 데이터 모델 정의
│   ├── __init__.py
│   └── schemas.py
├── services/            # 비즈니스 로직 (자동화 수행)
│   ├── __init__.py
│   └── delivery_service.py
├── utils/               # 공통 유틸리티, 드라이버 설정
│   ├── __init__.py
│   ├── driver.py
│   └── utils.py
├── main.py
├── pyproject.toml       # Poetry 설정 파일
└── README.md
```

---

## 🚀 실행 방법

### 1. Poetry 설치 (최초 1회)
```bash
pip install poetry
```

### 2. 프로젝트 설치
```bash
poetry install
```

### 3. 서버 실행
```bash
# FastAPI 서버 실행
poetry run uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

---

## 📡 API 명세

### POST `/register-delivery`

> 네이버 로그인 및 택배사 등록을 자동화합니다.

#### ✅ Request Body (타입 명시)
```json
{
  "login_id": "string",
  "login_pw": "string",
  "mall_name": "string",
  "manager_name": "string",
  "phone_number": "string",
  "delivery_company": "string",
  "biz_number": "string",
  "contract_number": "string",
  "origin_name": "string",
  "origin_zipcode": "string",
  "origin_address1": "string",
  "origin_address2": "string",
  "origin_phone": "string"
}
```

#### 🔁 Response 예시
```json
{
  "success": true,
  "message": "택배사 등록 완료"
}
```

---

## 🧱 기술 스택

- **Python 3.10+**
- **FastAPI** - API 서버
- **Selenium** - 웹 브라우저 자동화
- **Poetry** - 의존성 및 프로젝트 관리
- **uvicorn** - ASGI 서버

---

## 🔐 보안 주의사항

- `login_pw`와 같은 민감 정보는 `.env` 파일 또는 환경 변수로 분리 관리하는 것을 권장합니다.
  
---

## 📬 문의

프로젝트나 자동화 과정에서 궁금한 사항이 있으면 언제든지 피드백 주세요 🙌
