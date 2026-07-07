# Render 프론트엔드 Docker 배포 가이드

## 1. 목적

이 문서는 CareerFit AI의 React/Vite 프론트엔드를 Docker 기반 Render Web Service로 배포하는 방법을 설명합니다.

백엔드는 이미 Render Web Service에 Docker 기반으로 배포되어 있다고 가정합니다.

요리 비유로 보면, 백엔드는 주방이고 프론트엔드는 손님이 보는 홀입니다.  
이 문서는 Render 클라우드에서 홀과 주방이 서로 주문을 주고받도록 주소를 맞추는 안내서입니다.

---

## 2. 로컬 실행 방법

### 백엔드 실행

```bash
cd backend
uvicorn main:app --reload
```

백엔드 확인 주소:

```text
http://localhost:8000/health
http://localhost:8000/docs
```

### 프론트엔드 실행

```bash
cd frontend
npm install
npm run dev
```

프론트엔드 확인 주소:

```text
http://localhost:5173
```

---

## 3. 프론트엔드 환경변수 설정

프론트엔드는 API 주소를 `VITE_API_BASE_URL`로 관리합니다.

로컬 개발용 예시:

```bash
VITE_API_BASE_URL=http://localhost:8000
```

Render 배포용 예시:

```bash
VITE_API_BASE_URL=https://your-backend-service.onrender.com
```

주의:

- React/Vite 프론트엔드에는 API Key를 넣지 않습니다.
- `GEMINI_API_KEY`는 절대 `VITE_`로 시작하는 이름으로 만들지 않습니다.
- `VITE_` 환경변수는 브라우저에 노출될 수 있습니다.

---

## 4. 백엔드 CORS 환경변수 설정

백엔드는 `FRONTEND_ORIGINS` 환경변수로 허용할 프론트엔드 주소를 관리합니다.

로컬 + Render 예시:

```bash
FRONTEND_ORIGINS=http://localhost:5173,http://127.0.0.1:5173,https://your-frontend-service.onrender.com
```

기본 로컬 허용 주소:

```text
http://localhost:5173
http://127.0.0.1:5173
http://localhost:3000
http://127.0.0.1:3000
```

주의:

- `allow_origins=["*"]`로 대충 처리하지 않습니다.
- Render 프론트엔드 URL이 정해지면 정확한 URL을 `FRONTEND_ORIGINS`에 추가합니다.

---

## 5. 프론트엔드 Dockerfile 설명

프론트엔드 Dockerfile은 멀티 스테이지 빌드를 사용합니다.

1단계:

```text
node:20-alpine
```

React/Vite 앱을 빌드합니다.

2단계:

```text
nginx:1.27-alpine
```

빌드된 정적 파일을 Nginx로 서빙합니다.

핵심 구조:

```text
React/Vite source
→ npm run build
→ dist 생성
→ Nginx가 dist를 서빙
```

---

## 6. Render에서 프론트엔드 Docker Web Service 배포

### 1단계: 새 Web Service 생성

Render Dashboard에서 다음을 선택합니다.

```text
New
→ Web Service
→ GitHub Repository 선택
```

### 2단계: 기본 설정

```text
Name: careerfit-ai-frontend
Language: Docker
Branch: main
Root Directory: frontend
Dockerfile Path: Dockerfile
```

Root Directory를 `frontend`로 잡았다면 Dockerfile Path는 `Dockerfile`입니다.

Root Directory를 비워둔다면 Dockerfile Path는 아래처럼 입력합니다.

```text
frontend/Dockerfile
```

둘 중 하나만 선택하세요. 중복으로 `frontend/frontend/Dockerfile`처럼 잡히면 안 됩니다.

### 3단계: 프론트엔드 환경변수 등록

Render 프론트엔드 서비스의 Environment Variables에 아래 값을 추가합니다.

```bash
VITE_API_BASE_URL=https://your-backend-service.onrender.com
```

주의:

- 끝에 `/`를 붙이지 않아도 됩니다.
- 코드에서 자동으로 마지막 `/`를 제거합니다.

### 4단계: 배포 실행

```text
Create Web Service
→ Deploy
```

배포가 완료되면 Render가 프론트엔드 URL을 제공합니다.

예시:

```text
https://your-frontend-service.onrender.com
```

---

## 7. 백엔드 Render 환경변수 설정

백엔드 Render 서비스에 아래 값을 등록합니다.

```bash
GEMINI_API_KEY=실제_Gemini_API_Key
MOCK_MODE=false
LLM_MODEL=gemini-2.5-flash-lite
FRONTEND_ORIGINS=http://localhost:5173,http://127.0.0.1:5173,https://your-frontend-service.onrender.com
```

주의:

- `GEMINI_API_KEY`는 GitHub에 올리지 않습니다.
- `.env` 파일도 GitHub에 올리지 않습니다.
- 실제 키는 Render Environment Variables에만 입력합니다.

---

## 8. 배포 후 확인 방법

### 백엔드 확인

```text
https://your-backend-service.onrender.com/health
```

정상 예시:

```json
{"status":"ok"}
```

API 문서:

```text
https://your-backend-service.onrender.com/docs
```

### 프론트엔드 확인

```text
https://your-frontend-service.onrender.com
```

화면에서 다음 값을 입력해 테스트합니다.

```text
전공: 경영학부
스킬: Python, SQL
관심 직무: 데이터 분석
```

정상 결과:

- AI 분석 결과 카드 표시
- sources 카드 표시
- confidence 표시
- 콘솔에 CORS 오류 없음

---

## 9. CORS 오류 해결 방법

브라우저 콘솔에 CORS 오류가 뜨면 아래를 확인합니다.

### 1. 백엔드 FRONTEND_ORIGINS 확인

백엔드 Render 환경변수에 실제 프론트엔드 주소가 들어 있어야 합니다.

```bash
FRONTEND_ORIGINS=https://your-frontend-service.onrender.com
```

로컬도 함께 허용하려면:

```bash
FRONTEND_ORIGINS=http://localhost:5173,http://127.0.0.1:5173,https://your-frontend-service.onrender.com
```

### 2. 프론트엔드 VITE_API_BASE_URL 확인

프론트엔드 Render 환경변수에 실제 백엔드 주소가 들어 있어야 합니다.

```bash
VITE_API_BASE_URL=https://your-backend-service.onrender.com
```

### 3. 두 서비스 재배포

환경변수를 바꾼 뒤에는 관련 서비스를 다시 배포합니다.

```text
Manual Deploy
→ Deploy latest commit
```

---

## 10. Git에 올리면 안 되는 파일 목록

아래 파일은 GitHub에 올리지 않습니다.

```text
.env
.env.*
backend/.env
frontend/.env
node_modules/
dist/
venv/
.venv/
__pycache__/
*api*키*.txt
*key*.txt
*token*.txt
```

예외적으로 아래 파일은 올릴 수 있습니다.

```text
.env.example
.env.production.example
```

단, 예시 파일에는 실제 API Key를 넣지 않습니다.

---

## 11. 최종 체크리스트

- [ ] 프론트엔드에서 `localhost:8000` 하드코딩 제거
- [ ] `VITE_API_BASE_URL`로 API 주소 관리
- [ ] 백엔드 CORS가 `FRONTEND_ORIGINS` 기반으로 동작
- [ ] `allow_origins=["*"]` 사용하지 않음
- [ ] `frontend/Dockerfile` 생성
- [ ] `frontend/.dockerignore` 생성
- [ ] `frontend/nginx.conf` 생성
- [ ] Render 프론트엔드 환경변수 등록
- [ ] Render 백엔드 환경변수 등록
- [ ] `.env`, API Key, Token 파일이 GitHub에 올라가지 않음