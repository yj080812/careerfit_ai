# CareerFit AI

> 취업·공모전 데이터 기반 맞춤형 AI 포트폴리오 코치

---

## 📌 프로젝트 개요

취업 준비생과 대학생은 채용 공고와 공모전 정보를 보면서도 어떤 역량을 우선적으로 준비해야 하는지, 자신의 전공과 스킬을 어떻게 포트폴리오로 연결해야 하는지 어려움을 겪습니다.

CareerFit AI는 취업·공모전 데이터를 기반으로 사용자의 전공, 보유 스킬, 관심 직무를 분석하고 맞춤형 커리어 및 포트폴리오 방향을 추천하는 AI 서비스입니다.

이 프로젝트는 RAG 구조를 활용하여 ChromaDB에서 관련 공고 데이터를 검색하고, 검색된 근거를 Gemini API 프롬프트에 함께 전달하여 답변의 신뢰도를 높였습니다. 또한 React UI에서 분석 결과, 참고 공고 sources, confidence를 함께 표시하여 사용자가 AI 답변의 근거를 확인할 수 있도록 구성했습니다.

---

## 🛠 기술 스택

| 영역 | 기술 |
|---|---|
| 백엔드 | Python 3.11, FastAPI |
| AI API | Gemini 2.5 Flash-Lite |
| 데이터 | Pandas, SQLite, ChromaDB |
| 프론트엔드 | React, Vite, Tailwind CSS |
| 실행 환경 | Docker |
| 배포 | Render Web Service |
| 개발 도구 | VS Code / Cursor, GitHub |

---

## 🏗 아키텍처

```text
사용자
  ↓
React / Vite Frontend
  ↓ fetch
FastAPI Backend
  ↓
ChromaDB 검색
  ↓
관련 공고 문서 추출
  ↓
Gemini API
  ↓
answer + sources + confidence 반환
  ↓
React UI 결과 표시
```

---

## 🚀 실행 방법

### 1. Docker로 백엔드 실행

```bash
docker build -t careerfit-ai ./backend
docker run -p 8000:8000 --env-file backend/.env careerfit-ai
```

백엔드 API 문서:

```text
http://localhost:8000/docs
```

Health Check:

```text
http://localhost:8000/health
```

---

### 2. 로컬에서 백엔드 실행

```bash
cd backend
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

macOS / Linux:

```bash
source venv/bin/activate
```

패키지 설치:

```bash
pip install -r requirements.txt
```

서버 실행:

```bash
uvicorn main:app --reload --port 8000
```

---

### 3. 로컬에서 프론트엔드 실행

```bash
cd frontend
npm install
npm run dev
```

프론트엔드 화면:

```text
http://localhost:5173
```

---

## 🔐 환경변수 설정

### backend/.env 예시

```bash
GEMINI_API_KEY=your_gemini_api_key_here
MOCK_MODE=false
LLM_MODEL=gemini-2.5-flash-lite
FRONTEND_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
```

### frontend/.env 예시

```bash
VITE_API_BASE_URL=http://localhost:8000
```

주의 사항:

- 실제 API Key는 GitHub에 올리지 않습니다.
- `.env` 파일은 GitHub에 커밋하지 않습니다.
- React 코드에는 Gemini API Key를 절대 넣지 않습니다.
- 프론트엔드는 사용자 입력만 백엔드로 전달하고, 실제 LLM 호출은 백엔드에서 수행합니다.
- Render 배포 시 실제 환경변수는 Render Dashboard의 Environment Variables에 직접 등록합니다.

---

## 📊 데이터 파이프라인

```text
CSV
→ Pandas 전처리
→ SQLite 구조화 저장
→ RAG 문서 생성
→ ChromaDB 벡터 검색
→ Gemini RAG 답변 생성
```

전처리 실행:

```bash
cd backend
python data/preprocess.py
```

### 데이터 처리 내용

- CSV 데이터 구조 설계
- 결측치 확인 및 처리
- 중복 데이터 제거
- Python, SQL 등 스킬 키워드 표준화
- SQLite 저장 및 SQL 조회 테스트
- 채용 공고를 자연어 기반 RAG 문서로 변환
- ChromaDB 저장을 위한 JSON 문서 생성

---

## 💡 데이터 관련 설명

### 왜 이 데이터를 선택했는가?

CareerFit AI는 대학생이 취업과 공모전을 준비할 때 자신의 전공, 보유 스킬, 관심 직무를 기준으로 어떤 역량을 보완해야 하는지 알려주는 서비스입니다.

따라서 실제 서비스 흐름과 가장 직접적으로 연결되는 채용 공고 및 공모전 데이터를 선택했습니다. 이 데이터에는 회사명, 직무명, 요구 스킬, 우대 스킬, 주요 업무, 마감일 등이 포함되어 있어 사용자의 입력값과 비교하기에 적합합니다.

### SQLite와 ChromaDB에 같은 데이터를 저장하는 이유는 무엇인가?

SQLite와 ChromaDB는 같은 데이터를 저장하더라도 목적이 다릅니다.

SQLite는 회사명, 직무명, 마감일, 요구 스킬처럼 구조화된 정보를 표 형태로 저장하고 조회하는 데 사용합니다.

ChromaDB는 채용 공고 내용을 자연어 문서로 변환해 저장한 뒤, 사용자의 질문과 의미적으로 비슷한 공고를 찾는 데 사용합니다.

즉, SQLite는 정확한 조건 조회와 데이터 관리용이고, ChromaDB는 RAG 검색을 위한 의미 기반 검색용입니다.

CareerFit AI에서는 SQLite로 원본 데이터를 안정적으로 관리하고, ChromaDB로 관련 공고를 찾아 Gemini가 근거 있는 답변을 생성하도록 구성했습니다.

---

## ✨ 주요 기능

### 1. RAG 기반 역량 분석

사용자의 전공, 보유 스킬, 관심 직무를 입력받아 관련 공고 데이터를 검색하고 맞춤형 분석 결과를 제공합니다.

### 2. 출처 표시

AI 답변이 어떤 공고 데이터를 참고했는지 `sources`로 함께 반환합니다.

### 3. 신뢰도 표시

RAG 검색 결과를 기반으로 `confidence`를 표시하여 사용자가 답변의 신뢰도를 참고할 수 있도록 했습니다.

### 4. Mock Mode

API 한도 초과 또는 실습 환경 문제 발생 시 `MOCK_MODE=true`로 설정하여 백엔드 흐름을 테스트할 수 있습니다.

### 5. React UI

사용자가 전공, 스킬, 관심 직무를 입력하고 분석 결과와 출처 공고를 한 화면에서 확인할 수 있습니다.

### 6. Docker 기반 실행

FastAPI 백엔드를 Docker 이미지로 빌드하고 실행할 수 있도록 구성했습니다.

### 7. Render 배포 준비

백엔드와 프론트엔드를 각각 Render Web Service로 배포할 수 있도록 환경변수, CORS, Docker 설정을 정리했습니다.

---

## 🔎 주요 API

### Health API

```text
GET /health
```

서버 상태를 확인합니다.

### Jobs API

```text
GET /jobs
GET /jobs/{id}
```

채용 공고 데이터를 조회합니다.

### Analyze API

```text
POST /analyze
```

사용자의 전공, 스킬, 관심 직무를 기반으로 RAG 분석 결과를 반환합니다.

요청 예시:

```json
{
  "major": "경영학부",
  "skills": ["Python", "SQL"],
  "job_type": "데이터 분석"
}
```

응답 예시:

```json
{
  "answer": "입력한 전공과 스킬을 기준으로 데이터 분석 직무와 관련성이 높습니다.",
  "sources": [
    {
      "company": "예시회사",
      "title": "데이터 분석가",
      "required_skills": "Python, SQL",
      "distance": 0.91
    }
  ],
  "confidence": "medium"
}
```

---

## 🧩 4일차 구현 내용: RAG 기반 서비스 + React UI

### RAG 기반 `/analyze` API 구현

4일차에는 사용자의 전공, 보유 스킬, 관심 직무를 입력받아 관련 공고 데이터를 검색하고, Gemini API를 통해 맞춤형 분석 결과를 생성하는 RAG 기반 분석 기능을 구현했습니다.

처리 흐름:

```text
사용자 입력
→ FastAPI /analyze API
→ ChromaDB에서 관련 공고 문서 검색
→ 검색 결과를 Gemini 프롬프트에 포함
→ AI 분석 답변 생성
→ answer, sources, confidence 반환
→ React UI에서 결과 표시
```

### ChromaDB 문서 검색

`rag_service.py`에서 ChromaDB에 저장된 RAG 문서를 검색하도록 구성했습니다.

주요 구현 내용:

- 사용자 입력을 기반으로 관련 공고 문서 검색
- distance 값을 활용한 검색 결과 필터링
- 취업·공모전 범위를 벗어난 질문 차단
- 검색 결과를 Gemini 프롬프트에 전달할 수 있는 문서 형태로 변환

### Gemini RAG 답변 생성

`llm_service.py`에서 검색된 공고 데이터를 Gemini 프롬프트에 포함하여 답변을 생성하도록 구성했습니다.

주요 구현 내용:

- RAG context 기반 프롬프트 생성
- 제공된 공고 데이터에 근거한 답변 생성
- 없는 회사명, 공고명, 스킬을 지어내지 않도록 지침 추가
- 응답 결과에 `answer`, `sources`, `confidence` 포함
- API 오류 및 응답 실패 상황 처리

### React UI 구현

React + Vite 기반으로 CareerFit AI의 프론트엔드 화면을 구현했습니다.

구성 컴포넌트:

- `App.jsx`: 전체 상태 관리 및 `/analyze` API 요청
- `InputForm.jsx`: 전공, 보유 스킬, 관심 직무 입력 폼
- `ResultCard.jsx`: AI 분석 결과 표시
- `SourceCard.jsx`: 참고한 공고 데이터 출처 표시

### 4일차 보안 점검

- React 코드에 API Key를 넣지 않음
- Gemini API Key는 `backend/.env`에서만 관리
- `.env` 파일은 GitHub에 올리지 않도록 `.gitignore`에 포함
- 프론트엔드는 사용자 입력만 FastAPI에 전달
- 실제 LLM 호출은 백엔드에서만 수행

---

## 🐳 5일차 구현 내용: Docker + Render 배포 준비

### Docker 적용 목적

Docker는 개발 환경 차이로 인해 발생하는 실행 오류를 줄이기 위해 사용했습니다.  
FastAPI 백엔드 서버와 필요한 Python 패키지를 하나의 컨테이너 이미지로 묶어, 로컬과 클라우드 환경에서 동일한 방식으로 실행할 수 있도록 구성했습니다.

요리 비유로 보면 Docker는 도시락 통입니다. 내 컴퓨터 주방에서 만든 FastAPI 서비스를 필요한 재료와 함께 포장해 Render 클라우드 주방에서도 같은 방식으로 실행할 수 있게 합니다.

### 백엔드 Dockerfile 구성

`backend/Dockerfile`은 Python 3.11 slim 이미지를 기반으로 FastAPI 서버를 실행하도록 구성했습니다.

주요 구성:

```text
python:3.11-slim
→ /app 작업 디렉토리 설정
→ requirements.txt 복사
→ pip install
→ backend 코드 복사
→ 8000 포트 노출
→ uvicorn main:app 실행
```

실행 명령:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

### 프론트엔드 Dockerfile 구성

프론트엔드는 React/Vite 빌드 결과물을 Nginx로 서빙하는 멀티 스테이지 Dockerfile로 구성했습니다.

처리 흐름:

```text
node:20-alpine
→ npm install
→ npm run build
→ dist 생성
→ nginx:alpine
→ dist 정적 파일 서빙
```

프론트엔드는 `VITE_API_BASE_URL` 환경변수를 통해 백엔드 API 주소를 관리합니다.

### Render 배포 구조

CareerFit AI는 Render에서 백엔드와 프론트엔드를 각각 별도의 Web Service로 배포할 수 있도록 구성했습니다.

```text
Render Frontend Web Service
  ↓ VITE_API_BASE_URL
Render Backend Web Service
  ↓
Gemini API + ChromaDB
```

### Render 환경변수

프론트엔드 Render 서비스:

```bash
VITE_API_BASE_URL=https://your-backend-service.onrender.com
```

백엔드 Render 서비스:

```bash
GEMINI_API_KEY=your_gemini_api_key_here
MOCK_MODE=false
LLM_MODEL=gemini-2.5-flash-lite
FRONTEND_ORIGINS=http://localhost:5173,http://127.0.0.1:5173,https://your-frontend-service.onrender.com
```

### CORS 설정

백엔드는 `FRONTEND_ORIGINS` 환경변수로 허용할 프론트엔드 주소를 관리합니다.

기본 로컬 허용 주소:

```text
http://localhost:5173
http://127.0.0.1:5173
http://localhost:3000
http://127.0.0.1:3000
```

Render 프론트엔드 URL이 생기면 `FRONTEND_ORIGINS`에 추가합니다.

주의:

- `allow_origins=["*"]`로 처리하지 않습니다.
- 실제 프론트엔드 주소만 명시적으로 허용합니다.

### Git 보안 점검

5일차에는 GitHub Push Protection 오류를 통해 API Key와 Token 파일이 Git에 포함되면 안 된다는 점을 확인했습니다.

보안 점검 항목:

- `.env` 파일 GitHub 업로드 금지
- API Key가 들어간 `.txt` 파일 업로드 금지
- Gemini API Key 재발급 필요 여부 확인
- Hugging Face Token 재발급 필요 여부 확인
- `.gitignore`에 민감 파일 패턴 추가
- 실제 비밀값은 Render Environment Variables에서만 관리

`.gitignore` 주요 항목:

```gitignore
.env
.env.*
!.env.example
!.env.production.example
node_modules/
dist/
__pycache__/
*.pyc
.venv/
venv/
backend/.env
frontend/.env
backend/chroma_db/
*api*키*.txt
*key*.txt
*token*.txt
```

---

## ☁️ Render 배포 방법

### 1. 백엔드 배포

Render에서 백엔드 Web Service를 생성합니다.

설정 예시:

```text
Runtime: Docker
Root Directory: backend
Dockerfile Path: Dockerfile
```

백엔드 환경변수:

```bash
GEMINI_API_KEY=your_gemini_api_key_here
MOCK_MODE=false
LLM_MODEL=gemini-2.5-flash-lite
FRONTEND_ORIGINS=http://localhost:5173,http://127.0.0.1:5173,https://your-frontend-service.onrender.com
```

배포 후 확인:

```text
https://your-backend-service.onrender.com/health
https://your-backend-service.onrender.com/docs
```

---

### 2. 프론트엔드 배포

Render에서 프론트엔드 Web Service를 새로 생성합니다.

설정 예시:

```text
Runtime: Docker
Root Directory: frontend
Dockerfile Path: Dockerfile
```

프론트엔드 환경변수:

```bash
VITE_API_BASE_URL=https://your-backend-service.onrender.com
```

배포 후 확인:

```text
https://your-frontend-service.onrender.com
```

프론트엔드 배포 URL이 생기면 백엔드 Render 서비스의 `FRONTEND_ORIGINS`에 해당 URL을 추가한 뒤 백엔드를 다시 배포합니다.

---

## 🧪 최종 확인 체크리스트

- [ ] `/health`가 정상 응답한다.
- [ ] `/analyze` 응답에 `sources`가 포함된다.
- [ ] `/analyze` 응답에 `confidence`가 포함된다.
- [ ] React UI에서 분석 결과 카드가 표시된다.
- [ ] React UI에서 출처 공고 카드가 표시된다.
- [ ] 브라우저 콘솔에 CORS 오류가 없다.
- [ ] Docker로 백엔드가 실행된다.
- [ ] Render 백엔드 URL에서 `/docs` 접속이 가능하다.
- [ ] Render 프론트엔드에서 백엔드 API 호출이 가능하다.
- [ ] `.env`, API Key, Token 파일이 GitHub에 올라가지 않는다.
- [ ] `git status`에서 민감 파일이 보이지 않는다.

---

## 📁 프로젝트 구조

```text
careerfit_ai/
├── backend/
│   ├── main.py
│   ├── routers/
│   │   └── analyze.py
│   ├── services/
│   │   ├── rag_service.py
│   │   └── llm_service.py
│   ├── data/
│   │   ├── preprocess.py
│   │   ├── rag_documents.json
│   │   └── test_search.py
│   ├── requirements.txt
│   ├── .env.example
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   ├── config/
│   │   │   └── api.js
│   │   └── components/
│   │       ├── InputForm.jsx
│   │       ├── ResultCard.jsx
│   │       └── SourceCard.jsx
│   ├── package.json
│   ├── .env.example
│   ├── .dockerignore
│   ├── nginx.conf
│   └── Dockerfile
├── docs/
│   ├── design-skill.md
│   └── render-frontend-deploy.md
├── harness/
└── README.md
```

---

## 📈 진행 현황

- [x] 1일차: 프로젝트 기획 및 개발 환경 세팅
- [x] 2일차: FastAPI 서버 구축 및 Gemini API 연결
- [x] 3일차: 데이터 파이프라인 구축
- [x] 4일차: RAG 기반 서비스 + React UI
- [x] 5일차: Docker + Render 배포 준비 + 포트폴리오 정리

---

## 🔮 향후 개선

- [ ] 이력서 PDF 업로드 후 자동 역량 추출
- [ ] 공모전 마감일 알림 기능
- [ ] RAG 검색 품질 평가 지표 추가
- [ ] 사용자별 분석 결과 저장 기능
- [ ] 프론트엔드 배포 URL과 백엔드 Render URL 연결 안정화
- [ ] 실제 사용자 피드백 기반 추천 문구 개선

---

## 📝 개발 과정

이번 프로젝트에서 가장 어려웠던 부분은 ChromaDB 검색 결과를 Gemini 답변에 연결하고, 그 근거를 `sources`로 함께 반환하는 과정이었습니다.

처음에는 검색 결과가 비어 있거나 관련성이 낮은 문서가 반환되었지만, RAG 문서의 자연어 설명을 보강하고 distance 기준을 조정하면서 더 안정적인 분석 결과를 만들 수 있었습니다.

또한 5일차에는 Docker와 Render 배포를 준비하면서 로컬 환경과 클라우드 환경의 차이를 줄이는 방법을 학습했습니다. 특히 `.env`, API Key, Token 파일이 GitHub에 올라가지 않도록 관리하는 보안 점검의 중요성을 확인했습니다.

---

## 🌐 Demo

- Live Demo: 배포 후 Render 프론트엔드 URL 추가 예정
- Backend API Docs: 배포 후 Render 백엔드 `/docs` URL 추가 예정

---

## 👩‍💻 Developer

- Name: 본인 이름
- Role: Backend / AI Service / Frontend UI / Docker Deployment
- GitHub: 본인 GitHub 계정
- Email: 본인 이메일