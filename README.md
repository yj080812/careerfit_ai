# CareerFit AI

> 취업·공모전 데이터 기반 맞춤형 AI 포트폴리오 코치



## 프로젝트 개요



[본인이 작성한 문제 정의 한 단락]

취업 준비생들은 채용 공고와 공모전 정보를 바탕으로 어떤 역량을 준비해야 하는지, 자신의 경험을 어떻게 포트폴리오로 정리해야 하는지 어려움을 겪습니다.

CareerFit AI는 취업·공모전 데이터를 분석하고 AI를 활용하여 사용자 맞춤형 커리어 및 포트폴리오 방향을 추천하는 서비스입니다.


## 기술 스택



| 영역 | 기술 |

|---|---|

| 백엔드 | Python, FastAPI |

| AI API | Gemini 2.5 Flash-Lite |

| 데이터 | Pandas, SQLite, ChromaDB |

| 프론트엔드 | React, Vite |

| 실행 환경 | Docker |

# 로컬 실행 방법

## 사전 요구 사항

- Python 3.11 이상
- Gemini API Key

## 백엔드 실행

```bash
cd backend
python -m venv venv
```

### Windows

```bash
venv\Scripts\activate
```

### macOS / Linux

```bash
source venv/bin/activate
```

### 패키지 설치

```bash
pip install -r requirements.txt
```

### 서버 실행

```bash
uvicorn main:app --reload
```

---

# 구현 기능

## FastAPI 서버

- FastAPI 프로젝트 구성
- Router 분리
- CORS 설정

### Health API

- `/health`
- 서버 상태 확인

### Jobs API

- `/jobs`
- `/jobs/{id}`
- 채용 공고 조회

### Analyze API

- `/analyze`
- Gemini API 기반 커리어 분석

---

# 데이터 파이프라인

## 취업·공모전 데이터 구조 설계

- CSV 데이터 구조 설계
- 채용 공고 및 공모전 데이터 관리

## 데이터 전처리

- 결측치 확인 및 처리
- 중복 데이터 제거
- 데이터 품질 검증

## 스킬 키워드 표준화

- Python, SQL 등 기술 스택 표준화
- 동일 의미의 스킬명 통일

## SQLite 저장

- 전처리 데이터 저장
- SQL 조회 테스트

## RAG 문서 생성

- 채용 공고를 자연어 문서로 변환
- JSON 형태의 RAG 문서 생성
- ChromaDB 저장을 위한 데이터 준비

---

---

# 4일차 구현 내용: RAG 기반 서비스 + React UI

## RAG 기반 `/analyze` API 구현

4일차에는 사용자의 전공, 보유 스킬, 관심 직무를 입력받아 관련 공고 데이터를 검색하고, Gemini API를 통해 맞춤형 분석 결과를 생성하는 RAG 기반 분석 기능을 구현했습니다.

처리 흐름은 다음과 같습니다.

```text
사용자 입력
→ FastAPI /analyze API
→ ChromaDB에서 관련 공고 문서 검색
→ 검색 결과를 Gemini 프롬프트에 포함
→ AI 분석 답변 생성
→ answer, sources, confidence 반환
→ React UI에서 결과 표시
```

## ChromaDB 문서 검색

`rag_service.py`에서 ChromaDB에 저장된 RAG 문서를 검색하도록 구성했습니다.

주요 구현 내용:

- 사용자 입력을 기반으로 관련 공고 문서 검색
- distance 값을 활용한 검색 결과 필터링
- 취업·공모전 범위를 벗어난 질문 차단
- 검색 결과를 Gemini 프롬프트에 전달할 수 있는 문서 형태로 변환

## Gemini RAG 답변 생성

`llm_service.py`에서 검색된 공고 데이터를 Gemini 프롬프트에 포함하여 답변을 생성하도록 구성했습니다.

주요 구현 내용:

- RAG context 기반 프롬프트 생성
- 제공된 공고 데이터에 근거한 답변 생성
- 없는 회사명, 공고명, 스킬을 지어내지 않도록 지침 추가
- 응답 결과에 `answer`, `sources`, `confidence` 포함
- API 오류 및 응답 실패 상황 처리

## React UI 구현

React + Vite 기반으로 CareerFit AI의 프론트엔드 화면을 구현했습니다.

구성 컴포넌트:

- `App.jsx`: 전체 상태 관리 및 `/analyze` API 요청
- `InputForm.jsx`: 전공, 보유 스킬, 관심 직무 입력 폼
- `ResultCard.jsx`: AI 분석 결과 표시
- `SourceCard.jsx`: 참고한 공고 데이터 출처 표시

## 프론트엔드 실행 방법

```bash
cd frontend
npm install
npm run dev
```

프론트엔드 화면:

```text
http://localhost:5173
```

백엔드 API 문서:

```text
http://localhost:8000/docs
```

## 4일차 보안 점검

- React 코드에 API Key를 넣지 않음
- Gemini API Key는 `backend/.env`에서만 관리
- `.env` 파일은 GitHub에 올리지 않도록 `.gitignore`에 포함
- 프론트엔드는 사용자 입력만 FastAPI에 전달
- 실제 LLM 호출은 백엔드에서만 수행

## 4일차 결과 요약

4일차 결과물은 사용자가 자신의 전공, 스킬, 관심 직무를 입력하면 CareerFit AI가 관련 공고 데이터를 검색하고, Gemini API를 통해 맞춤형 커리어 분석 결과를 제공하는 웹 UI입니다.

이 과정에서 RAG 검색 결과를 `sources`로 함께 표시하여 AI 답변의 근거를 확인할 수 있도록 했고, `confidence`를 통해 추천 결과의 신뢰도를 사용자에게 보여주도록 구성했습니다.

---


## 진행 현황



- [x] 1일차: 프로젝트 기획 및 개발 환경 세팅

- [x] 2일차: FastAPI 서버 구축 및 Gemini API 연결

- [x] 3일차: 데이터 파이프라인 구축

- [x] 4일차: RAG 기반 서비스 + React UI

- [ ] 5일차: Docker + 포트폴리오 완성